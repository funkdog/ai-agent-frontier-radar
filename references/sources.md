# Source Registry

Use this registry as a minimum coverage contract, not as a claim that every site exposes
a stable RSS feed. Prefer the official index/feed. If it is blocked or JavaScript-only,
use a date-scoped `site:` search and the organization’s official GitHub/model hub, then
mark coverage `degraded`.

## Papers — Daily core

| Source | Primary surface | Use |
|---|---|---|
| Hugging Face Daily Papers | `https://huggingface.co/api/daily_papers` | Community-filtered discovery; open the paper |
| Hugging Face paper search | `https://huggingface.co/api/papers/search` | Topic recall for agent/LLM terms |
| arXiv | `https://export.arxiv.org/api/query` | Original metadata and revisions |
| arXiv HTML/PDF | `https://arxiv.org/` | Read methods, experiments, and limitations |

Default topic families: agents, tool use, computer use, coding agents, multi-agent,
planning, reasoning, reinforcement learning, post-training, memory, RAG, context
management, long context, evaluation, observability, safety, interpretability, model
inference, multimodal agents, and human-agent collaboration.

## International labs — Daily core

| Organization | Official surfaces |
|---|---|
| OpenAI | `https://openai.com/research/index/`, `https://openai.com/news/` |
| Anthropic | `https://www.anthropic.com/research/`, `https://www.anthropic.com/engineering`, `https://www.anthropic.com/news` |
| Google DeepMind | `https://deepmind.google/discover/blog/`, `https://deepmind.google/research/` |
| Meta AI | `https://ai.meta.com/blog/`, `https://ai.meta.com/research/` |
| Microsoft Research | `https://www.microsoft.com/en-us/research/blog/` |
| NVIDIA | `https://developer.nvidia.com/blog/`, `https://research.nvidia.com/` |
| Hugging Face | `https://huggingface.co/blog`, `https://huggingface.co/papers` |
| Mistral AI | `https://mistral.ai/news/`, `https://github.com/mistralai` |
| Cohere | `https://cohere.com/research`, `https://cohere.com/blog` |

## Chinese labs — Daily core

| Organization | Official surfaces and fallback |
|---|---|
| Qwen / Tongyi | `https://qwen.ai/blog/`, `https://qwenlm.github.io/blog/`, `https://github.com/QwenLM` |
| DeepSeek | `https://www.deepseek.com/`, `https://github.com/deepseek-ai` |
| ByteDance Seed | `https://seed.bytedance.com/research`, `https://seed.bytedance.com/blog/` |
| Tencent Hunyuan | `https://hunyuan.tencent.com/`, `https://github.com/Tencent-Hunyuan` |
| Baidu ERNIE | `https://ernie.baidu.com/blog/`, `https://github.com/PaddlePaddle/PaddleNLP` |
| Zhipu / Z.ai / GLM | `https://z.ai/` plus date-scoped `site:z.ai/blog`, `https://github.com/THUDM` |
| Moonshot / Kimi | `https://www.moonshot.cn/`, `https://github.com/MoonshotAI` |
| MiniMax | `https://www.minimax.io/`, `https://github.com/MiniMax-AI` |
| StepFun | `https://www.stepfun.com/`, `https://github.com/stepfun-ai` |

For organizations without a stable technical blog, official GitHub releases, model
cards, technical reports, and arXiv author/affiliation searches count as the direct-scan
fallback. Social accounts are leads, never final evidence.

## Open-source Agent runtimes — Daily core

The project's own release, repository, tests, security advisory, and maintainer-authored
technical note are primary sources for the software. Scan stable releases every day.

| Project | Official release surface |
|---|---|
| OpenAI Codex | `https://github.com/openai/codex/releases` |
| Anthropic Claude Code | `https://github.com/anthropics/claude-code/releases` |
| Gemini CLI | `https://github.com/google-gemini/gemini-cli/releases` |
| Google ADK Python / JS | `https://github.com/google/adk-python/releases`, `https://github.com/google/adk-js/releases` |
| Microsoft Agent Framework | `https://github.com/microsoft/agent-framework/releases` |
| Qwen Code | `https://github.com/QwenLM/qwen-code/releases` |
| Kimi Code | `https://github.com/MoonshotAI/kimi-code/releases` |
| DeepSeek Harness | `https://github.com/deepseek-ai/deepseek-harness/releases` |
| NVIDIA OpenShell | `https://github.com/NVIDIA/OpenShell/releases` |
| oh-my-pi | `https://github.com/can1357/oh-my-pi/releases` |
| AgentScope | `https://github.com/agentscope-ai/agentscope/releases` |
| GitHub Agentic Workflows | `https://github.com/github/gh-aw/releases` |

- Stable releases compete for `Must Read` under the normal quality gate.
- Prereleases default to `Watchlist`; promote only a material security, migration, or
  interoperability event and label maturity.
- Commit-only activity is not a release. Include it only for an official security
  advisory or for a project that intentionally has no release mechanism.
- Merge a runtime release with its lab post or paper when they describe the same event.

## Frontier voices on X — Monitored idea layer

Read [x-voices.md](x-voices.md) for the account registry, access fallback, conflict
labels, and promotion rules. Check every X1 account on each scheduled run and rotate X2
accounts across seven days. These posts feed the separate `Frontier Voices` section and
do not bypass the evidence gate for `Must Read`.

The primary collection path is `scripts/fetch_x_frontier.py`, backed by the official X
Search API and the scheduler secret `X_BEARER_TOKEN`. The collector is read-only, uses an
exact UTC window, excludes replies and retweets, and returns structured coverage. X API
pricing is pay-per-resource; keep the default three-page cap and disclose truncation
rather than silently increasing cost.

## Secondary recall — Never sufficient alone

| Source | Surface | Purpose |
|---|---|---|
| Agentic Brew | `https://www.agenticbrew.ai/feed/blog.xml`, `https://www.agenticbrew.ai/feed/paper.xml` | Catch missed blog/paper candidates |
| Hacker News | `https://hn.algolia.com/api` | Engineering impact signal |
| The Batch | `https://www.deeplearning.ai/the-batch/` | Cross-check notable releases |
| Import AI / technical newsletters | Original newsletter pages | Detect blind spots; trace claims upstream |

Do not treat a secondary source’s absence as proof that an official source had no update.
