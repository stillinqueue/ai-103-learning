# AI-103-learning

Hands-on labs and notes for **Microsoft AI-103: Developing AI Apps and Agents on Azure**.

> **Current milestone: Learning Path 1 completed. Next: Develop AI agents on Azure.**

---

## Progress

| Learning Path | Progress | Status |
|---|---|---|
| [Develop generative AI apps in Azure](https://learn.microsoft.com/en-us/training/paths/develop-generative-ai-apps/) | 6 / 6 modules | ✅ Completed |
| [Develop AI agents on Azure](https://learn.microsoft.com/en-us/training/paths/develop-ai-agents-azure/) | 5 / 9 modules (Teams and M365 integration exercise complete) | 🟡 In progress |
| [Develop natural language solutions in Azure](https://learn.microsoft.com/en-us/training/paths/develop-language-solutions-azure-ai/) | 0 / 7 modules | ⬜ Not started |
| [Extract insights from visual data on Azure](https://learn.microsoft.com/en-us/training/paths/insight-visual-data/) | 0 / 8 modules | ⬜ Not started |

---

## Completed so far

**Learning Path 1 — Develop generative AI apps in Azure** was completed via Microsoft Learn. Hands-on
labs were adapted to run in GitHub Codespaces against the OpenAI Platform API because Azure Free Trial
quota limitations prevented the required Foundry model deployment (GPT-5.2). Core SDK concepts —
Responses API, streaming, tool use, RAG, and fine-tuning preparation — were all practised and are
documented here. See [comparisons/official-lab-vs-my-implementation.md](comparisons/official-lab-vs-my-implementation.md)
for a full breakdown of what was and was not reproduced on Azure.

| Area | Location |
|---|---|
| Responses API chat app (streaming, multi-turn) | [implementations/generative-ai/responses-api/](implementations/generative-ai/responses-api/) |
| RAG with file search and web search tools | [implementations/generative-ai/rag/](implementations/generative-ai/rag/) |
| Fine-tuning dataset, validation, and baseline | [implementations/generative-ai/fine-tuning/](implementations/generative-ai/fine-tuning/) |
| Official lab vs my implementation comparison | [comparisons/official-lab-vs-my-implementation.md](comparisons/official-lab-vs-my-implementation.md) |

---

## Next learning path

**[Develop AI agents on Azure](https://learn.microsoft.com/en-us/training/paths/develop-ai-agents-azure/) — 5 / 9 modules (Teams and M365 integration exercise complete)**

This is the current area of active work. The completed exercises are located under `implementations/agents/`. Additional modules will be added as the learning path progresses.

### Completed exercise

- `teams-notifications` agent exercise: completed
  - Foundry/agent configuration with `gpt-5-mini`
  - File Search grounding over `notification-policy.txt`
  - Code Interpreter over `system_performance.csv`
  - JSON notification schema with strict policy grounding
- `astronomy-custom-tools` custom-function exercise: completed
  - Official Foundry reference in `agent.py`
  - Codespaces/OpenAI implementation in `openai-agent.py`
  - Custom tools for event lookup, observation cost, and report generation
  - Application-side Python execution with iterative `function_call_output` handling
- `mcp-integration` MCP exercise: completed
  - FastMCP `Inventory` server over stdio
  - Dynamic discovery of `get_inventory_levels` and `get_weekly_sales`
  - OpenAI workaround using `session.call_tool(...)` and `function_call_output`
- `foundry-iq` approval-flow exercise: completed
  - Official Foundry client using `AIProjectClient` and `DefaultAzureCredential`
  - Foundry IQ approval handling with `mcp_approval_request` and `mcp_approval_response`
  - Codespaces/OpenAI approximation with explicit approval before local knowledge lookup
- `m365-teams-integration` exercise: completed
  - Local enterprise knowledge agent using OpenAI File Search
  - Verified grounding over IT security and remote-work policies
  - Official Teams and optional Microsoft 365 Copilot publishing flow documented
  - Azure/M365 publishing was not executed in the current environment

---

## Exam revision

[notes/exam-revision-checklist.md](notes/exam-revision-checklist.md) — a quick revision checklist for the AI-103 exam, covering the key concepts from the completed first learning path.
