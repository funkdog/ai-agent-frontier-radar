---
name: ai-agent-frontier-radar
description: >
  Collect and curate a daily high-signal digest of AI and AI-agent papers, official
  lab research posts, engineering blogs, system cards, evals, and important open-source
  releases, plus original high-quality ideas and field notes from curated AI/agent voices
  on X. Use for “AI/Agent 前沿日报”, daily paper, lab-blog, open-source runtime, or expert-X
  monitoring, frontier radar, scheduled research digests, or checking what leading Chinese
  and international AI labs and builders published recently. Not for broad consumer-tech
  news, single-paper deep analysis, investment news, or unverified social-media roundups.
  Output: 5–8 deduplicated evidence items, optionally 0–3 Frontier Voices, primary-source
  links, caveats, and a source-coverage report. Read-only: never follow, subscribe,
  publish, or modify external systems.
---

# AI & Agent Frontier Radar

## Why This Is a Skill

Prevent three recurring failures in automated digests: treating search rank as quality,
repeating one release from several outlets, and silently missing official lab sources.
Optimize for decision value, not volume.

## Run Contract

1. Use the interval since the previous successful report; default to the last 36 hours.
   On a gap, extend only far enough to cover the gap and label the window.
2. Read [sources.md](references/sources.md) and [x-voices.md](references/x-voices.md)
   before collecting. Check every `Daily core` source and every X1 voice. Treat
   aggregators, engagement counts, and unverified social claims as discovery leads only.
3. Gather in parallel:
   - Hugging Face Daily Papers and relevant arXiv categories/searches.
   - Official research, engineering, news, model-card, system-card, and GitHub surfaces.
   - Stable releases from the open-source Agent runtime registry; route prereleases and
     commit-only activity according to [sources.md](references/sources.md).
   - Original posts and linked long-form work from curated X voices.
   - Curated secondary feeds only as a final “what did the direct scan miss?” pass.
4. Open the primary source for every candidate. A search result, feed summary, repost,
   screenshot, or AI-generated synopsis is not evidence. An original X post is primary
   only for what its author thinks or reports firsthand; open the linked paper, code,
   logs, or official announcement before repeating external factual claims.
5. Deduplicate by canonical URL, normalized title, paper ID, and underlying event. Merge
   a paper, lab post, model card, and repository into one item when they describe the
   same release.
6. When thread history is available, compare against the previous seven reports. Include
   an old topic only when there is a material new result, revision, code release, or
   independent evaluation; label it `follow-up`.
7. Score and select using the gate below. Do not fill quota on a quiet day.
8. Render the report using [output-contract.md](references/output-contract.md), with
   citations linking directly to the sources actually opened.

On a scheduled run, execute immediately without asking intake questions. Post the digest
to the task’s delivery thread. Do not create local files unless the user explicitly asks
for an archive.

## Quality Gate

Score each candidate from 0–2 on:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Agent relevance | peripheral | useful AI context | directly advances agents/LLMs |
| Material novelty | rehash | meaningful update | new method/result/capability |
| Evidence | unsupported | primary claim only | paper/code/eval or reproducible detail |
| Likely impact | little consequence | useful niche impact | changes research/engineering choices |
| Source trust | anonymous/aggregated | attributable secondary | official or original research source |

Include only scores ≥7, with `Evidence ≥1` and `Source trust ≥1`. Community votes, stars,
leaderboards, and vendor benchmarks may help discovery but never raise evidence strength
without checking methodology and comparison scope.

For numerical, benchmark, causal, trend, or model-comparison claims, invoke
`source-audit` when available. Otherwise apply the same five checks: primary source,
conflict of interest, peer-review status, date/model applicability, and independent
corroboration. Downgrade wording when evidence is weak.

## Frontier Voice Gate

Keep X commentary separate from `Must Read`; select 0–3 posts and do not fill quota.
Include a post only when it is original and supplies at least two of: a falsifiable
mechanism, concrete experiment or trace, linked artifact, novel synthesis, or a decision
consequence for Agent builders. Label it `idea`, `field-note`, `counterpoint`, or
`release-context`.

Never use follower count, likes, reposts, or virality as quality evidence. Disclose the
author's relevant employer, project, investment, or newsletter interest. Label an
unverified thesis as opinion. If X cannot be read comprehensively, follow the fallback in
[x-voices.md](references/x-voices.md) and report coverage as `degraded`.

## Positive, Negative, and Gray Examples

- Positive: “每天给我 AI Agent 前沿论文和实验室博客。”
- Positive: “今天 OpenAI、Anthropic、Qwen、DeepSeek 有什么值得读的更新？”
- Negative: “深入讲解这篇论文。” Use a paper-analysis/research workflow.
- Negative: “总结今天所有科技新闻。” Use a general news digest.
- Gray: “最近 AI 很火的东西。” Use this skill only after narrowing the request to
  research, engineering, models, evals, or agents.

## Common Mistakes

| Mistake | Consequence | Correction |
|---|---|---|
| Copy an aggregator’s AI summary | Upstream errors become our conclusion | Open the paper or official post |
| Count several reports as several advances | Repetitive, inflated digest | Cluster by underlying event |
| Rank by votes or stars alone | Popularity replaces quality | Apply the evidence and impact gate |
| Quote a vendor benchmark as neutral fact | Marketing claim gains false authority | Inspect methodology and label provenance |
| Treat a viral X thread as established fact | Influence becomes counterfeit evidence | Separate the idea from its linked factual claims |
| Hide an author's employer or project interest | Readers cannot judge incentives | Disclose affiliation beside the post |
| Ignore Chinese labs without RSS | Systematic geographic blind spot | Use official pages, GitHub/model hubs, and degraded coverage labels |
| Hide a blocked or stale source | False completeness | Report `degraded` with the attempted fallback |
| Force 5–8 items on a quiet day | Low-signal filler | Publish fewer items and say the day was quiet |

## Done When

- Every included item resolves to an opened primary source.
- Cross-source and seven-report deduplication is complete.
- No strong external claim lacks provenance or caveat.
- The coverage section accounts for every Daily core source as `updated`, `no update`,
  or `degraded`.
- X1 voices and rotating X2 voices are accounted for, including access degradation.
- A quiet day is reported honestly.
