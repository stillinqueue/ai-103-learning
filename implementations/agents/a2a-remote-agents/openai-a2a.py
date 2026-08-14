"""Local A2A-compatible workaround for the remote-agent exercise.

The Codespace does not have a2a-sdk installation, so this file mirrors the lab's
agent-card and message/send JSON-RPC shapes with the Python standard library.
OpenAI() is used only inside the remote Title and Outline agents.
"""

import json
import os
import threading
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable

from openai import OpenAI


MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
HOST = "127.0.0.1"
TITLE_PORT = 10007
OUTLINE_PORT = 10008

TOPIC = (
    "Create a short blog post about practical ways small teams can adopt "
    "responsible AI in everyday software projects."
)


class LocalA2AAgent:
    def __init__(
        self,
        name: str,
        description: str,
        skill_id: str,
        skill_name: str,
        handler: Callable[[str], str],
    ) -> None:
        self.card = {
            "name": name,
            "description": description,
            "url": "",
            "version": "1.0.0",
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text"],
            "capabilities": {"streaming": False},
            "skills": [
                {
                    "id": skill_id,
                    "name": skill_name,
                    "description": description,
                    "tags": [skill_id],
                    "examples": [],
                }
            ],
        }
        self.handler = handler

    def set_url(self, url: str) -> None:
        self.card["url"] = url

    def process(self, text: str) -> str:
        return self.handler(text)


class AgentRequestHandler(BaseHTTPRequestHandler):
    agent: LocalA2AAgent

    def log_message(self, format: str, *args: Any) -> None:
        return

    def do_GET(self) -> None:
        if self.path == "/.well-known/agent-card.json":
            self._send_json(200, self.agent.card)
        elif self.path == "/health":
            self._send_json(200, {"status": f"{self.agent.card['name']} is running"})
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self) -> None:
        if self.path not in {"/", "/message"}:
            self._send_json(404, {"error": "Not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            request = json.loads(self.rfile.read(length))
            if request.get("method") != "message/send":
                raise ValueError("Only the A2A message/send method is supported")

            message = request.get("params", {}).get("message", {})
            parts = message.get("parts", [])
            text = next(part["text"] for part in parts if part.get("kind") == "text")
            response_text = self.agent.process(text)
            task_id = str(uuid.uuid4())
            task = {
                "id": task_id,
                "contextId": message.get("messageId", task_id),
                "status": {
                    "state": "completed",
                    "message": {
                        "role": "agent",
                        "parts": [{"kind": "text", "text": response_text}],
                    },
                },
                "artifacts": [
                    {
                        "parts": [{"kind": "text", "text": response_text}],
                    }
                ],
            }
            self._send_json(
                200,
                {"jsonrpc": "2.0", "id": request.get("id"), "result": task},
            )
        except Exception as exc:
            self._send_json(
                200,
                {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32602, "message": str(exc)},
                },
            )

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def start_agent_server(agent: LocalA2AAgent, port: int) -> ThreadingHTTPServer:
    agent.set_url(f"http://{HOST}:{port}/")
    handler = type(f"{agent.card['name']}Handler", (AgentRequestHandler,), {"agent": agent})
    server = ThreadingHTTPServer((HOST, port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def create_title_agent() -> LocalA2AAgent:
    client = OpenAI()

    def generate_title(topic: str) -> str:
        response = client.responses.create(
            model=MODEL,
            instructions=(
                "You are the Title Agent. Suggest one clear, catchy blog post "
                "title for the supplied topic. Return only the title."
            ),
            input=topic,
        )
        return response.output_text.strip()

    return LocalA2AAgent(
        name="Local Title Agent",
        description="Generates a clear blog title from a topic.",
        skill_id="generate_blog_title",
        skill_name="Generate Blog Title",
        handler=generate_title,
    )


def create_outline_agent() -> LocalA2AAgent:
    client = OpenAI()

    def generate_outline(context: str) -> str:
        response = client.responses.create(
            model=MODEL,
            instructions=(
                "You are the Outline Agent. Based on the topic and title, write "
                "a concise outline with 4 to 6 numbered sections. Return only "
                "the outline."
            ),
            input=context,
        )
        return response.output_text.strip()

    return LocalA2AAgent(
        name="Local Outline Agent",
        description="Generates a concise outline from a topic and title.",
        skill_id="generate_outline",
        skill_name="Generate Outline",
        handler=generate_outline,
    )


class A2AHost:
    def __init__(self, agent_urls: list[str]) -> None:
        self.agent_urls = agent_urls
        self.cards: dict[str, dict[str, Any]] = {}

    def discover_agents(self) -> None:
        for base_url in self.agent_urls:
            with urllib.request.urlopen(
                f"{base_url}/.well-known/agent-card.json", timeout=10
            ) as response:
                card = json.load(response)
            self.cards[card["name"]] = card

    def send_task(self, agent_name: str, text: str) -> str:
        card = self.cards[agent_name]
        message_id = str(uuid.uuid4())
        payload = {
            "jsonrpc": "2.0",
            "id": message_id,
            "method": "message/send",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"kind": "text", "text": text}],
                    "messageId": message_id,
                }
            },
        }
        request = urllib.request.Request(
            card["url"],
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
        if "error" in result:
            raise RuntimeError(result["error"])
        task = result["result"]
        return task["artifacts"][0]["parts"][0]["text"]


def main() -> None:
    title_server = start_agent_server(create_title_agent(), TITLE_PORT)
    outline_server = start_agent_server(create_outline_agent(), OUTLINE_PORT)
    try:
        host = A2AHost(
            [f"http://{HOST}:{TITLE_PORT}", f"http://{HOST}:{OUTLINE_PORT}"]
        )
        host.discover_agents()
        title_agent_name = "Local Title Agent"
        outline_agent_name = "Local Outline Agent"
        title = host.send_task(title_agent_name, TOPIC)
        outline = host.send_task(
            outline_agent_name,
            f"Topic: {TOPIC}\nTitle Agent result: {title}",
        )
        print(f"Discovered agents: {', '.join(host.cards)}")
        print(f"Title endpoint contacted: {host.cards[title_agent_name]['url']}")
        print(f"Outline endpoint contacted: {host.cards[outline_agent_name]['url']}")
        print(f"Input request:\n{TOPIC}\n")
        print(f"Title-agent result:\n{title}\n")
        print(f"Outline-agent result:\n{outline}\n")
        print(f"Final combined result:\nTitle: {title}\n\nOutline:\n{outline}")
    finally:
        title_server.shutdown()
        outline_server.shutdown()
        title_server.server_close()
        outline_server.server_close()


if __name__ == "__main__":
    main()
