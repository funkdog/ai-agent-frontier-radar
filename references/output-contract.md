# Daily Output Contract

Keep the report compact enough to read in five minutes. Prefer 3 excellent items over 8
mediocre ones.

```markdown
# AI & Agent Frontier Radar — YYYY-MM-DD

Window: {start} → {end} · {timezone}
Today: {one-sentence synthesis, or “No high-signal update passed the gate.”}

## Must Read

### 1. {Title}
`paper|research|engineering|model|eval|system-card` · {organization} · {date}

- **What changed:** one factual sentence.
- **Why it matters:** concrete consequence for AI/agent research or engineering.
- **Evidence:** `strong|moderate|early` — explain in one sentence.
- **Caveat:** limitation, vendor interest, missing code/eval, or applicability boundary.
- **Primary:** [paper or official post](url)
- **Artifacts:** [code](url) · [model/system card](url) — include only verified links.

## Watchlist

- Items that are promising but too early, weakly evidenced, or awaiting code/evals.

## Frontier Voices

### @handle: {short thesis}
`idea|field-note|counterpoint|release-context` · {author / affiliation} · {date}

- **Thesis:** the author's idea, clearly attributed.
- **Why it matters:** the concrete decision or research direction it changes.
- **Basis:** firsthand build experience, trace, experiment, linked artifact, or `opinion`.
- **Boundary:** conflict of interest, missing evidence, or applicability limit.
- **Source:** [original post](url) · [supporting artifact](url) — only opened links.

## Coverage

- Papers: HF Daily Papers `{status}` · arXiv `{status}`
- International labs: `{updated/no update/degraded counts}`; name every degraded source.
- Chinese labs: `{updated/no update/degraded counts}`; name every degraded source.
- Open-source Agent runtimes: `{updated/no update/degraded counts}`; separate stable and prerelease activity.
- X Frontier Voices: `{X1 checked / X2 rotated / degraded counts}`; name every degraded access path.
- Secondary gap check: `{sources checked}`

## Provenance

`Primary sources: N · Independent corroborations: N · Rejected/merged candidates: N`
```

`Frontier Voices` is optional and contains 0–3 items. It does not count toward the 5–8
`Must Read` target. Omit the section on a quiet day rather than lowering its gate.

## Evidence Labels

- `strong`: primary paper/report plus code, model card, independent eval, or enough
  methodological detail to verify the central claim.
- `moderate`: credible primary source with concrete methodology but incomplete public
  artifacts or only internal evaluation.
- `early`: original announcement/preprint whose key claims are not yet independently
  validated. Keep only if potentially important and label it clearly.

## Style

- Write in Chinese unless the user requests another language.
- Preserve original English technical terms on first use.
- Lead with the contribution, not background or hype.
- Link titles and evidence near the supported claim.
- Do not quote long passages. Paraphrase and keep provenance.
- Never say “SOTA” without naming the benchmark, comparison set, model version, and
  source of the evaluation.
