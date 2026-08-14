# A2A remote agents

Completed Microsoft Learn exercise: **Connect to remote agents with A2A protocol**.

## Official Foundry/A2A implementation

The completed reference implementation preserves the official roles:

- **Host/routing agent** in `routing_agent/`: discovers remote agents, creates the routing agent, exposes `send_message` as a function tool, and returns the final response to the caller.
- **Remote Title agent** in `title_agent/`: generates a single blog title and exposes it through an A2A server.
- **Remote Outline agent** in `outline_agent/`: generates a concise outline and exposes it through an A2A server.
- **A2A client/server communication**: `A2ACardResolver` and `A2AClient` discover and contact remote servers, while `A2AStarletteApplication`, `DefaultRequestHandler`, `AgentExecutor`, and `TaskUpdater` handle incoming A2A tasks.

The official implementation uses `a2a-sdk` for agent cards, message/task types, client requests, server request handling, and task updates. Communication between the host and remote agents is HTTP-based.

The official Foundry/A2A code was completed and syntax-validated. It was not executed in Codespaces because the environment lacks the `a2a-sdk`, `fastapi`, and `azure-ai-agents` modules, Azure CLI is unauthenticated, and execution also requires a valid Foundry project endpoint, model deployment, Azure agent resources, and credentials through `DefaultAzureCredential`. This is an environment and resource limitation, not a failure of the A2A protocol or Microsoft Foundry implementation.

The Azure dependencies are configured through `.env` and include:

- `PROJECT_ENDPOINT`: Foundry project endpoint.
- `MODEL_DEPLOYMENT_NAME`: deployed model used by the routing, Title, and Outline Foundry agents.
- `DefaultAzureCredential`: Azure authentication provider.
- Azure AI Agent resources created and accessed through `AgentsClient`.
- Local `SERVER_URL` and agent ports for the HTTP endpoints.

## Local runnable A2A implementation

[`openai-a2a.py`](openai-a2a.py) is a separate local workaround. Since `a2a-sdk` was not installed and package installation was not performed, it mirrors the lab's A2A-compatible protocol shapes with the Python standard library:

- local Title remote agent at `http://127.0.0.1:10007/`
- local Outline remote agent at `http://127.0.0.1:10008/`
- agent-card discovery at `/.well-known/agent-card.json`
- JSON-RPC `message/send` requests with A2A-style messages, tasks, status, and artifacts
- separate host logic that discovers and contacts agents only through HTTP

The host does not import or directly call either remote agent implementation. `OpenAI()` and the OpenAI Platform are used only for model inference inside the local Title and Outline agent handlers. The host sends the Title result as context in the subsequent Outline request.

## Verified runtime behavior

One official-lab-style request was run successfully:

```text
Create a short blog post about practical ways small teams can adopt responsible AI in everyday software projects.
```

Both remote HTTP endpoints started successfully. The host discovered both agent cards, reached the Title endpoint first, received its response, then included that result in the request sent to the Outline endpoint. The Outline response returned successfully, and the host produced the final combined result. No remote Python function was executed directly by the host, and no runtime errors occurred.

Captured Title result:

```text
Responsible AI for Small Teams: A Practical Playbook for Everyday Projects
```

Captured Outline result:

```text
1. Why responsible AI matters for small teams
2. Practical practices across the development lifecycle
3. Lightweight governance, roles, and artifacts
4. Tooling and templates for small teams
5. A quick-start playbook and next steps
```

The local workaround is a runnable A2A-compatible demonstration, not the Microsoft `a2a-sdk` implementation.
