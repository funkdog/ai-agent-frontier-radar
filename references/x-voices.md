# X Frontier Voices Registry

Use this layer to catch original ideas, engineering field notes, and informed
counterpoints before they become papers or formal blog posts. It is not a popularity
feed and does not turn social claims into facts.

## Access and evidence rules

Use the first available path:

1. Run `python3 scripts/fetch_x_frontier.py`, passing the report's UTC window through
   `--start-time` and `--end-time`. It queries all X1 voices plus one deterministic X2
   rotation through the official X Search API, excludes replies and retweets, and
   outputs canonical URLs. Configure `X_BEARER_TOKEN` only in the scheduler's secret
   environment. Never put the token in this Skill, a repository, a command-line
   argument, logs, or chat.
2. If the official collector is unavailable, use a signed-in browser only when the
   runtime actually exposes that persistent browser session. Browser storage state and
   cookies are credentials: keep them outside the repository, never print them, and
   expect periodic reauthentication.
3. Use a date-scoped search restricted to `x.com/{handle}/status`, then open the
   canonical post URL.
4. Check the author's canonical blog, newsletter, GitHub, paper page, or employer blog
   for the same idea.

If the full timeline cannot be read, mark X coverage `degraded`; search results are not
proof of absence. Third-party mirrors may reveal a candidate URL but are never the cited
source. Do not quote a screenshot or repost when the original is unavailable.

Do not make RSSHub, twscrape, gallery-dl, Nitter, or another unofficial GraphQL/Web API
client the scheduled primary path. RSSHub, twscrape, and gallery-dl require an X account
session cookie and can break when X changes private endpoints; if explicitly enabled,
use them only for discovery and still open the canonical post. Nitter is not an available
fallback: its upstream repository was archived on 2026-08-26 after X demanded permanent
takedown of the project and its instances.

The official API is pay-per-resource. The collector reports observed Post and expanded
User resource counts and defaults to at most three 100-result pages per query batch. If
that cap is reached, it returns `degraded`; do not raise the cap silently. The recent
endpoint covers seven days. Older windows automatically use full-archive search and may
require additional account access and spend.

An original post is primary evidence for the author's own thesis or firsthand report.
For benchmarks, releases, causal claims, incidents, or comparisons, open the linked
artifact and apply the normal source audit. Record relevant affiliations even when the
post is technically correct.

## X1 — Check every scheduled run

| Voice | Focus | Canonical fallback | Interest to disclose |
|---|---|---|---|
| Andrej Karpathy `@karpathy` | model intuition, coding agents, AI education | `https://karpathy.ai/` | Anthropic |
| Simon Willison `@simonw` | LLM tooling, security, open-source releases | `https://simonwillison.net/` | independent builder / Datasette |
| Hamel Husain `@HamelHusain` | evals, coding agents, production debugging | `https://hamel.dev/` | independent consultant and course author |
| Chip Huyen `@chipro` | AI systems, production engineering, evaluation | `https://huyenchip.com/` | author and tool builder |
| Sebastian Raschka `@rasbt` | open models, architecture, code-first explainers | `https://sebastianraschka.com/blog/` | author / Ahead of AI |
| Nathan Lambert `@natolambert` | open models, post-training, Chinese labs | `https://www.interconnects.ai/` | Interconnects and model-ecosystem projects |
| François Chollet `@fchollet` | generalization, intelligence, eval design | `https://arcprize.org/` | ARC Prize / NDEA |
| Shunyu Yao `@ShunyuYao12` | language agents, RL, harness and eval design | `https://ysymyth.github.io/` | Tencent Hunyuan |
| Lilian Weng `@lilianweng` | harness engineering, RL, scaling and safety | `https://lilianweng.github.io/` | disclose current affiliation when known |
| Jim Fan `@DrJimFan` | embodied and virtual agents, robotics, simulation | `https://jimfan.me/` | NVIDIA |
| Ethan Mollick `@emollick` | applied AI, work, education, human-agent use | `https://www.oneusefulthing.org/` | Wharton / paid newsletter |
| swyx `@swyx` | AI engineering ecosystem, agents, infrastructure | `https://www.latent.space/` | Latent.Space / AI Engineer events |
| Boris Cherny `@bcherny` | coding-agent workflows and Claude Code practice | `https://borischerny.com/` | Anthropic / Claude Code |
| Peter Steinberger `@steipete` | open-source Agent runtimes and personal agents | `https://steipete.me/` | OpenAI / OpenClaw |
| Mario Zechner `@badlogicgames` | coding-agent runtime, tools, memory and recovery | `https://mariozechner.at/` | pi maintainer |
| 宝玉 `@dotey` | Chinese technical translation, prompts, coding practice | `https://baoyu.io/` | curator and AI engineer |

## X2 — Rotate across seven days

| Voice | Focus | Treatment |
|---|---|---|
| 歸藏 `@op7418` | multimodal products, model demos, design workflows | useful discovery; verify vendor claims and demos |
| 李继刚 `@lijigang` | prompt language, interface concepts, human-AI expression | prefer original conceptual posts; label opinion |
| 向阳乔木 `@vista8` | AI products and industry interpretation | trace news and commercial claims to originals |
| 数字生命卡兹克 `@Khazix0918` | Chinese model and product testing | inspect protocol before repeating comparisons |
| Orange AI `@oran_ge` | Agent-native products and business theses | treat forecasts as opinion; audit market numbers |

## Promotion and removal

Promote an X2 voice to X1 only after at least three useful items in 30 days that survive
source tracing. Add a new voice only when it closes a topic or geographic blind spot and
has a stable identity plus an original-work trail.

Demote or remove an account after repeated unattributed reposting, fabricated or
uncorrected claims, undisclosed promotion, engagement bait dominating technical output,
or 60 days without relevant original work. Review the registry quarterly; follower
count is never a promotion criterion.
