import asyncio
import json
import os
import sys
from contextlib import AsyncExitStack
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI


INSTRUCTIONS = """
You are an inventory assistant. Use the available MCP tools to retrieve inventory
and weekly sales data, then provide useful recommendations. Do not invent data.
"""


def _schema_as_dict(schema):
    if isinstance(schema, dict):
        return schema
    if hasattr(schema, "model_dump"):
        return schema.model_dump(exclude_none=True)
    return dict(schema)


def _openai_tools(mcp_tools):
    return [
        {
            "type": "function",
            "name": tool.name,
            "description": tool.description or "MCP tool",
            "parameters": _schema_as_dict(tool.inputSchema),
            "strict": True,
        }
        for tool in mcp_tools
    ]


def _tool_result_text(result):
    parts = []
    for content in result.content:
        text = getattr(content, "text", None)
        if text is not None:
            parts.append(text)
        elif hasattr(content, "model_dump"):
            parts.append(json.dumps(content.model_dump()))
        else:
            parts.append(str(content))
    return "\n".join(parts)


async def connect_to_server(exit_stack: AsyncExitStack):
    server_path = Path(__file__).with_name("server.py")
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
        env=None,
    )
    stdio, write = await exit_stack.enter_async_context(
        stdio_client(server_params)
    )
    session = await exit_stack.enter_async_context(ClientSession(stdio, write))
    await session.initialize()
    return session


async def run_turn(client: OpenAI, model: str, session: ClientSession, tools, request: str):
    response = client.responses.create(
        model=model,
        instructions=INSTRUCTIONS,
        tools=tools,
        input=request,
    )

    while True:
        function_calls = [
            item for item in response.output if item.type == "function_call"
        ]
        if not function_calls:
            print(f"AGENT: {response.output_text}")
            return

        function_outputs = []
        for item in function_calls:
            print(f"Model requested MCP tool: {item.name}")
            arguments = json.loads(item.arguments)
            result = await session.call_tool(item.name, arguments)
            print("MCP tool executed successfully")
            function_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": _tool_result_text(result),
                }
            )

        response = client.responses.create(
            model=model,
            tools=tools,
            previous_response_id=response.id,
            input=function_outputs,
        )


async def main():
    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    async with AsyncExitStack() as exit_stack:
        session = await connect_to_server(exit_stack)
        response = await session.list_tools()
        mcp_tools = response.tools
        tool_names = [tool.name for tool in mcp_tools]
        print(f"MCP tools discovered: {tool_names}")
        tools = _openai_tools(mcp_tools)

        while True:
            request = input(
                "Enter a prompt for the inventory agent. Use 'quit' to exit.\nUSER: "
            ).strip()
            if request.lower() == "quit":
                print("Exiting chat.")
                return
            await run_turn(client, model, session, tools, request)


if __name__ == "__main__":
    asyncio.run(main())
