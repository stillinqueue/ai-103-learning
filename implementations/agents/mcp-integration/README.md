# mcp-integration

Completed Microsoft AI agents exercise: **Extend agents with Model Context Protocol (MCP) tools**.

## MCP concepts

- An MCP server exposes tools.
- An MCP client creates a `ClientSession`, initializes it, and discovers tools with `session.list_tools()`.
- Discovered tools are invoked through `session.call_tool(tool_name, arguments)`.
- Tool definitions can be discovered dynamically instead of being hard-coded into the client.
- The model requests a tool and JSON arguments; the application executes the MCP call and returns the result.
- The model never directly executes the MCP server's Python code.

## Local MCP implementation

- `server.py` uses FastMCP to create an `Inventory` server over stdio.
- `@mcp.tool()` exposes `get_inventory_levels` and `get_weekly_sales`.
- `client.py` launches the local server, initializes an MCP session, lists tools, and includes a simple inventory test call.
- `agent.py` remains the official Foundry reference scaffold for the Azure portion of the exercise.

Verified discovered tools:

```text
get_inventory_levels
get_weekly_sales
```

The `get_inventory_levels` tool was invoked successfully. It returned:

```json
{
  "Moisturizer": 6,
  "Shampoo": 8,
  "Body Spray": 28,
  "Hair Gel": 5,
  "Lip Balm": 12,
  "Skin Serum": 9,
  "Cleanser": 30,
  "Conditioner": 3,
  "Setting Powder": 17,
  "Dry Shampoo": 45
}
```

## OpenAI workaround

`openai-mcp-agent.py` is the Codespaces/OpenAI Platform implementation used because Azure authentication is blocked in this environment. It:

- uses `OpenAI()` and the Responses API
- connects to the local MCP server over stdio
- discovers MCP tools dynamically with `list_tools()`
- converts discovered MCP schemas into Responses API function tools
- handles model `function_call` items
- invokes MCP tools with `session.call_tool(...)`
- returns each result as `function_call_output` with the original `call_id`
- continues with `previous_response_id` until no more function calls remain

The current script does not print raw model arguments. The `{}` argument shown for `get_inventory_levels` was reconstructed from the zero-parameter schema and successful execution, not copied from runtime logs.

## Key lesson

MCP provides a standardized protocol boundary for tool discovery and invocation. The model chooses from the tools exposed to it, while the application owns the MCP session, executes the call, and returns the result for the model's final response.
