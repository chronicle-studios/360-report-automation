# Ghost Tequila 360 Report — Methodology

## Context

This methodology defines how we produce a 360 analysis report for Ghost Tequila (ghosttequila.com). The existing workflow was built for IP/creator subjects with owned YouTube channels. Ghost Tequila is a consumer spirits brand with no owned channel and no presence in the Chronicle database.

There is no database-backed evidence layer. The report is entirely research-driven, which means methodology rigor — source assembly, cross-verification, coverage auditing, provenance — matters more, not less. No new infrastructure is introduced. The existing extraction pipeline is reused in a brand mode that replaces the database-driven YouTube step with research-driven primary platform extraction through the same LLM path used by every other section.

## 1. Entity Resolution

Before any research runs, the subject identity must be locked down. This is the brand equivalent of resolving a canonical channel ID.

A verified entity definition document must include:

| Field | Purpose |
|---|---|
| Canonical name and parent entity | Anchors all searches |
| Product lines and SKUs | Defines what counts as "the brand" |
| Search aliases | What to look for ("ghost tequila", "ghost pepper tequila") |
| Exclusion terms | What to filter out ("Ghost" alone, Ghost protein, Ghost energy, Ghost lifestyle brand) |
| Handle inventory | Confirmed social handles per platform |
| Competitor set | For qualitative positioning context (Tanteo, Ancho Reyes, etc.) |
| Scope | US-primary, trailing 12 months emphasis, English primary |

**Gate:** This document must be manually verified against the actual brand website and social profiles before any research step runs. Unverified entity definitions produce garbage downstream.

## 2. Mention Detection and Validation Rules

Because "Ghost" is a high-collision term, the entity definition alone is not sufficient. The methodology requires explicit rules for how brand mentions are detected and validated throughout the research and extraction process.

**Positive match rules:**

- "Ghost Tequila" as a phrase — always valid
- "Ghost" when co-occurring with any of: tequila, blanco, reposado, pepper, spirits, cocktail, Drizly, bar, bottle, proof — within the same paragraph or context block
- @ghosttequila handle on any platform — always valid
- ghosttequila.com domain — always valid

**Rejection rules:**

- "Ghost" alone in gaming, fitness, supplement, or lifestyle contexts — reject
- Ghost protein, Ghost energy, Ghost lifestyle, Ghost brand (the lifestyle company) — reject
- Ghost (the band), Ghost (film/TV references) — reject
- Any mention where the surrounding context has zero overlap with spirits, beverages, cocktails, bars, or food — reject

**Ambiguous cases:** Flag for manual review. Do not auto-include or auto-exclude. The coverage audit (section 3) must note how many ambiguous mentions were encountered and how they were resolved.

These rules apply at every stage: during research prompt construction, during source pack review, during LLM extraction, and during QA.

## 3. Source Pack Assembly

The benchmark workflow used five or more source documents cross-referenced against each other. A single deep-research pass is a weaker evidence base. For Ghost Tequila, we assemble a source pack from multiple independent inputs.

| Document | Source | Purpose |
|---|---|---|
| Brand Background | Manual — scraped from ghosttequila.com, about pages, press kit if available | Ground truth about the brand's self-presentation |
| Instagram Snapshot | Manual — captured from public IG profile: follower count, bio, recent post metrics, tagged content samples | Baseline social metrics that research must match |
| Retail Presence | Manual — check Drizly, ReserveBar, Total Wine, etc. for availability, pricing, ratings | Commercial evidence the research agent might miss |
| Research Report A | LLM deep research via primary model | Full 8-section narrative |
| Research Report B | LLM deep research via second model (Gemini or Grok) | Independent verification of the same 8 sections |

The multi-model approach is not about averaging outputs. It is about catching hallucinations and coverage gaps. Where Report A and Report B agree on a fact, confidence is higher. Where they diverge, that claim needs manual verification or gets downgraded.

**Gate:** Source pack must be assembled and reviewed before any extraction runs.

## 4. Coverage Audit

After source pack assembly, explicitly document what evidence exists and what is missing — before making any claims.

| Section | Evidence available | Evidence quality | Gaps |
|---|---|---|---|
| The Hook | IG profile, website, research reports | Moderate — no DB metrics | No hero stat from DB; must use research-sourced number |
| Instagram and Social | IG snapshot (manual), research reports | Good if IG is public | Engagement rate is estimated from visible post sample |
| Community | Research reports, Reddit search | Variable — depends on what exists | Ghost Tequila may have thin community presence |
| Sentiment | Research reports, review site scrapes | Medium — review sites are strongest | Social comment sentiment is LLM-inferred |
| Creative and Cultural | Research reports | Likely thin — spirits brands don't generate fan art | May need to reframe as "brand content ecosystem" |
| Commercial | Retail snapshot (manual), research reports | Good for distribution, weak for revenue | No sales data; competition medals may or may not exist |
| Geographic | Research reports, retailer listings | Weak — mostly inferred from availability | No audience geo data without owned channel analytics |
| Opportunities | Derived from gaps in other sections | Analytical, not factual | Quality depends on all other sections |

Sections with sparse evidence get explicit caveats, not padding.

**Gate:** Coverage audit must be completed before extraction. Sections flagged as thin get pre-written data-gap notes.

## 5. Provenance System

Every quantitative claim in the final report carries a provenance class. This is the core control layer that keeps the report defensible.

| Value | Meaning | Example |
|---|---|---|
| Confirmed | Directly visible on a public URL right now, independently verified | IG follower count visible on profile |
| Estimated | Derived from confirmed values, or agreed across multiple sources | Avg likes per post computed from 20 visible posts |
| Inferred | LLM classification, single-source claim, or heuristic | Sentiment classified from comment samples |
| Sparse | Weak signal, low confidence, or contradicted across sources | "Available in roughly 30 states" based on 2 retailer listings |

**Cross-source verification rule:** If a metric appears in both Research Report A and Research Report B with the same value (within 10%), it qualifies as confirmed. If only one source has it, it is estimated at best. If they contradict, it is sparse until manually resolved.

## 6. Section Adaptation

The 8-section structure is retained but each section's semantics are translated for a spirits brand, not mechanically copied from channel-based reports.

| Section | Channel-based (existing) | Brand-based (Ghost Tequila) |
|---|---|---|
| The Hook | Channel overview and hero stat | Brand positioning and strongest earned signal |
| Primary Platform | Owned YouTube deep dive | Instagram and Social deep dive (research-driven, manual-verified) |
| Community | Discord, Reddit, social nodes | r/tequila, r/cocktails, cocktail blogs, spirits forums, IG cocktail community, bartender networks |
| Sentiment | Per-platform audience feeling | Taste, value, heat level, packaging, mixability, authenticity — across review sites and social |
| Creative and Cultural | Fan art, cosplay, memes | Cocktail recipes, brand photography, bartender features, influencer integrations, UGC |
| The Proof | App store ratings, Patreon, crowdfunding | Retail distribution, menu and on-premise presence, competition medals, press features, DTC |
| The Reach | Languages, regions, comment geo | On-premise vs off-premise, state and regional availability, international distribution |
| Opportunities | Platform gaps, collabs | Distribution gaps, untapped creator partnerships, seasonal and event plays, category positioning |

Share-of-voice is explicitly dropped as a quantitative metric. It requires a consistent denominator across competitors that research-only data cannot provide. It is replaced with qualitative competitive positioning.

## 7. Reconciliation Loop

The report is not produced in a single pass. When new evidence surfaces or errors are found, the methodology defines how to update without redoing everything.

**Triggers:**

- Research is re-run with an improved prompt
- Manual review finds errors in extracted data
- A source-pack document is updated
- Cross-source verification reveals a contradiction

**Process:**

1. **Diff** — Compare new source against previous. Flag sections where claims changed more than 10% or new platforms and sources appeared.
2. **Targeted re-extraction** — Re-run extraction for affected sections only, not all sections.
3. **Cross-section consistency** — Verify numbers in overview hero stats still match the detail sections they came from.
4. **Provenance update** — Update research date metadata. Note if sections were extracted at different times.
5. **Re-QA** — Only changed sections need full QA; unchanged sections get a spot-check.

## 8. QA and Finalization

**Data integrity checklist:**

- Every stat in overview traces to a cited source in the source pack
- Spot-check five or more URLs from research output for validity
- Instagram metrics match what is currently visible on the actual profile
- No section makes claims exceeding what the coverage audit supports
- Entity disambiguation clean in every section (no false-positive brand mentions)
- Mention validation rules from section 2 were applied consistently across all sections
- Geographic section does not overclaim distribution from sparse signals
- Confidence tags distributed realistically (not everything confirmed)
- Data Gaps section honestly states there are no DB-backed metrics and the report is entirely research-driven
- Data Gaps includes confidence class distribution across all sections

**Output quality checklist:**

- Visual density matches the benchmark: each section has substantive content, not placeholder text or single-sentence summaries
- Modular clarity: each section stands alone and can be read independently without requiring context from other sections
- Stakeholder readability: language is accessible to non-technical readers; jargon is defined or avoided; key takeaways are front-loaded in each section
- Final output bundle generates without errors
