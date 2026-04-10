# Ghost Tequila 360 Report — Methodology & Implementation Plan

## Context

We need to produce a 360 analysis report for Ghost Tequila (ghosttequila.com) by April 15. The existing pipeline in this repo was built for IP/creator subjects with owned YouTube channels (e.g., Love & Pies). Ghost Tequila is a consumer spirits brand — no owned YouTube channel, no presence in the Chronicle DB (YouTube-only: `channels` + `videos` tables).

An earlier plan was reviewed against the benchmark methodology from `chronicle-studios/chronicle-360-reports` (which used multi-model source packs, iterative reconciliation, and explicit provenance). That review found 8 critical gaps. This methodology addresses all 8.

**The core constraint:** The Chronicle DB provides nothing for Ghost Tequila. There is no DB-backed evidence layer. The report is entirely research-driven, which means methodology rigor — source assembly, cross-verification, coverage auditing, provenance — matters more, not less.

---

## Part 1: Methodology

This section defines HOW the report is researched, verified, and quality-controlled. Code changes (Part 2) are implementation details that serve this methodology.

### 1.1 Entity Resolution

Before any research runs, the subject identity must be locked down. This is the brand equivalent of resolving a canonical `channel_id`.

**Deliverable:** `ghost_tequila/ENTITY_DEFINITION.md`

| Field | Purpose |
|---|---|
| Canonical name + parent entity | Anchors all searches |
| Product lines / SKUs | Defines what counts as "the brand" |
| Search aliases | What to look for ("ghost tequila", "ghost pepper tequila") |
| Exclusion terms | What to filter out ("Ghost" alone, Ghost protein, Ghost energy, Ghost lifestyle brand) |
| Handle inventory | Confirmed social handles per platform |
| Competitor set | For qualitative positioning context (Tanteo, Ancho Reyes, etc.) |
| Scope | US-primary, trailing 12 months emphasis, English primary |

**Gate:** This document must be manually verified against the actual brand website and social profiles before any research step runs. Unverified entity definitions produce garbage downstream.

### 1.2 Source Pack Assembly

The benchmark workflow used 5+ source documents cross-referenced against each other (background doc, YouTube stats, GPT report, Gemini report, Grok report). A single deep-research pass is a weaker evidence base. For Ghost Tequila, we assemble a source pack from multiple independent inputs.

**Deliverable:** `ghost_tequila/source_pack/` directory containing:

| Document | Source | Purpose |
|---|---|---|
| `BRAND_BACKGROUND.md` | Manual — scraped from ghosttequila.com, about pages, press kit if available | Ground truth about the brand's self-presentation |
| `INSTAGRAM_SNAPSHOT.md` | Manual — captured from public IG profile: follower count, bio, recent post metrics, tagged content samples | Baseline social metrics that research must match |
| `RETAIL_PRESENCE.md` | Manual — check Drizly, ReserveBar, Total Wine, etc. for availability, pricing, ratings | Commercial evidence the research agent might miss |
| `RESEARCH_REPORT_A.md` | LLM deep research (primary model via `DeepResearchClient`) | Full 8-section narrative |
| `RESEARCH_REPORT_B.md` | LLM deep research (second model — Gemini or Grok via separate API call) | Independent verification of the same 8 sections |

The multi-model approach isn't about averaging outputs. It's about **catching hallucinations and coverage gaps**. Where Report A and Report B agree on a fact, confidence is higher. Where they diverge, that claim needs manual verification or gets downgraded to `estimated`/`sparse`.

**Gate:** Source pack must be assembled and reviewed before the extraction pipeline runs.

### 1.3 Coverage Audit

After source pack assembly, explicitly document what evidence exists and what's missing — BEFORE making any claims.

**Deliverable:** `ghost_tequila/COVERAGE_AUDIT.md`

For each section of the report, answer:

| Section | Evidence available | Evidence quality | Gaps |
|---|---|---|---|
| The Hook | IG profile, website, research reports | Moderate — no DB metrics | No hero stat from DB; must use research-sourced number |
| Instagram & Social | IG snapshot (manual), research reports | Good if IG is public | Engagement rate is estimated from visible post sample |
| Community | Research reports, Reddit search | Variable — depends on what exists | Ghost Tequila may have thin community presence |
| Sentiment | Research reports, review site scrapes | Medium — review sites are strongest | IG/TikTok comment sentiment is LLM-inferred |
| Creative/Cultural | Research reports | Likely thin — spirits brands don't generate fan art | May need to reframe as "brand content ecosystem" |
| Commercial/Proof | Retail snapshot (manual), research reports | Good for distribution, weak for revenue | No sales data; competition medals may or may not exist |
| Geographic | Research reports, retailer listings | Weak — mostly inferred from availability | No audience geo data without owned channel analytics |
| Opportunities | Derived from gaps in other sections | N/A — analytical, not factual | Quality depends on all other sections |

This audit determines which sections can make strong claims and which must be honest about limitations. **Sections with sparse evidence get explicit caveats, not padding.**

**Gate:** Coverage audit must be completed before extraction. Sections flagged as "thin" get pre-written data-gap notes.

### 1.4 Provenance System

Every quantitative claim in the final report carries a provenance class. This is not optional decoration — it's the core control layer that keeps the report defensible.

**Standardized confidence values (used in all schemas):**

| Value | Meaning | Example |
|---|---|---|
| `"confirmed"` | Directly visible on a public URL right now, independently verified | IG follower count visible on profile |
| `"estimated"` | Derived/computed from confirmed values, or agreed across multiple sources | Avg likes/post computed from 20 visible posts |
| `"inferred"` | LLM classification, single-source claim, or heuristic | Sentiment classified from comment samples |
| `"sparse"` | Weak signal, low confidence, or contradicted across sources | "Available in ~30 states" based on 2 retailer listings |

**Cross-source verification rule:** If a metric appears in both Research Report A and Research Report B with the same value (within 10%), it can be `confirmed`. If only one source has it, it's `estimated` at best. If they contradict, it's `sparse` until manually resolved.

### 1.5 Section Adaptation

The 8-section structure survives but each section's semantics must be translated for a spirits brand, not mechanically copied from channel-based reports.

| Section | Channel-based (existing) | Brand-based (Ghost Tequila) |
|---|---|---|
| The Hook | Channel overview + hero stat | Brand positioning + strongest earned signal |
| Primary Platform | Owned YouTube deep dive (DB-driven) | Instagram & Social Deep Dive (research-driven, manual-verified) |
| Community | Discord, Reddit, social nodes | r/tequila, r/cocktails, cocktail blogs, spirits forums, IG cocktail community, bartender networks |
| Sentiment | Per-platform audience feeling | Taste, value, heat level, packaging, mixability, authenticity — across review sites + social |
| Creative/Cultural | Fan art, cosplay, memes, AMVs | Cocktail recipes, brand photography, bartender features, influencer integrations, UGC |
| The Proof | App store ratings, Patreon, crowdfunding | Retail distribution, menu/on-premise presence, competition medals, press features, DTC |
| The Reach | Languages, regions, comment geo | On-premise vs off-premise, state/regional availability, international distribution |
| Opportunities | Platform gaps, collabs | Distribution gaps, untapped creator partnerships, seasonal/event plays, category positioning |

**Share-of-voice is explicitly dropped** as a quantitative metric. It requires a consistent denominator across competitors that research-only data can't provide. Replace with qualitative competitive positioning: "Ghost Tequila is frequently compared to Tanteo in spicy tequila reviews but occupies a different price tier."

### 1.6 Reconciliation Loop

The report is not produced in a single pass. When new evidence surfaces or errors are found, the methodology defines how to update without redoing everything.

**Triggers:**

- Research is re-run with an improved prompt
- Manual review finds errors in extracted JSON
- A source-pack document is updated (e.g., IG follower count changed)
- Cross-source verification reveals a contradiction

**Process:**

1. **Diff** — compare new source against previous. Flag sections where claims changed >10% or new platforms/sources appeared.
2. **Targeted re-split** — only overwrite changed section `.md` files.
3. **Targeted re-extract** — re-run LLM extraction for affected sections only (not all).
4. **Cross-section consistency** — verify numbers in `overview` (hero stats) still match the detail sections they came from.
5. **Provenance update** — update `data_gaps.metadata.researchDate`. Note if sections were extracted at different times.
6. **Re-QA** — only the changed sections need full QA; unchanged sections get a spot-check.

### 1.7 QA & Finalization

**Pre-delivery checklist:**

- [ ] Every stat in overview traces to a cited source in the source pack
- [ ] Spot-check 5+ URLs from research output (are they real and current?)
- [ ] Instagram metrics match what's currently visible on the actual profile
- [ ] No section makes claims exceeding what the coverage audit supports
- [ ] Entity disambiguation clean in every section (no false-positive brand mentions)
- [ ] Geographic section doesn't overclaim distribution from sparse signals
- [ ] Confidence tags distributed realistically (not everything `confirmed`)
- [ ] Data Gaps section honestly states: no DB-backed metrics, entirely research-driven
- [ ] Data Gaps includes confidence class distribution across all sections
- [ ] TypeScript bundle generates without errors

---

## Part 2: Code Changes

These implement the methodology above within the existing pipeline.

### 2.1 New files

| File | Purpose |
|---|---|
| `ghost_tequila/ENTITY_DEFINITION.md` | Entity identity (Step 1.1) |
| `ghost_tequila/source_pack/` | Source pack directory (Step 1.2) |
| `ghost_tequila/COVERAGE_AUDIT.md` | Coverage audit (Step 1.3) |
| `prompts/ghost_tequila_research_prompt.md` | Brand-adapted research prompt, forked from `prompts/deep_research_prompt.md` |

### 2.2 Research prompt adaptation

`prompts/ghost_tequila_research_prompt.md` — forked from `prompts/deep_research_prompt.md`:

- TARGET SCOPE: add `brand` as IP type, add product-line/competitor/exclusion fields from Entity Definition
- Primary platform: override to Instagram
- Surface enumeration: add spirits-specific (Distiller, Drizly, r/tequila, Punch/Imbibe/VinePair, competition medals); remove irrelevant (comics, gaming, cosplay, fan wikis)
- Section 2: "Instagram & Social Deep Dive"
- Section 5: cocktail recipes / brand photography / influencer content
- Section 6: retail distribution / competition medals / press
- Remove Part-2 caveat
- Add competitive positioning instruction (qualitative, not quantitative)

### 2.3 Schema changes

**`prompts/section_schemas.py`:**

Add `instagram_social` schema (replaces `youtube` for brand mode):

```
earnedMediaOverview:
  totalMentions: str           + confidence
  uniquePlatforms: str         + confidence
  estimatedEarnedImpressions: str + confidence
  dateRange: str
  coverageNote: str            # explicit provenance statement

platformOverview:
  platform: str                # "Instagram"
  handle: str
  followers: str               + confidence
  following: str               + confidence
  postCount: str               + confidence
  bio: str
  verified: bool

contentAnalysis:
  postCadence: str             + confidence
  contentThemes: [str]
  formatMix: str               # "Reels vs static vs carousel"
  hashtagStrategy: str

engagementMetrics:
  avgLikesPerPost: str         + confidence
  avgCommentsPerPost: str      + confidence
  engagementRateEstimate: str  + confidence
  sampleSize: str              # how many posts this was computed from
  sampleNote: str              # "Based on 20 most recent public posts"

crossPlatformPresence:
  platforms: [{
    name: str
    handle: str
    followers: str             + confidence
    description: str
  }]

topContent: [{
  rank: int
  platform: str
  description: str
  metric: str                  # "12.4K likes" or "847 comments"
  type: str                    # "Reel", "Post", "TikTok", "YouTube mention"
  confidence: str
}]

keyInsights:
  strengths: [str]
  patterns: [str]
  gaps: [str]
```

Additional schema modifications:

- Add `confidence` field to existing schemas where missing:
  - `community.platforms[].stats[]`
  - `geographic.primaryMarkets` / `emergingMarkets` (top-level confidence)
- Modify `commercial` schema: replace `supercellInvestment` with generic `notableHighlight` (same shape: title, amount/value, description, impact)

### 2.4 Prompt changes

**`prompts/section_prompts.py`:**

- Add `instagram_social` prompt — instructs LLM to extract IG metrics, cross-platform presence, earned content from research text, preserving confidence tags
- Add brand-mode variants for: `community`, `sentiment`, `creative`, `commercial`, `geographic` (new keys like `community_brand`, or parameterized prompts)

### 2.5 Pipeline changes

**`workflow/report_splitter.py`:**

Add patterns to `primary_platform` SectionDefinition:

```python
SectionDefinition("primary_platform", "youtube.md", (
    "^#+\\s*youtube",
    "^#+\\s*primary\\s+platform",
    "^#+\\s*instagram",          # NEW
    "^#+\\s*social.*deep\\s*dive", # NEW
))
```

**`llm/section_generator.py`:**

Add `instagram_social` to `_build_configs` section map:

```python
section_map = {
    # ... existing entries ...
    "instagram_social": ("Instagram & Social", "instagram_social.md"),  # NEW
}
```

**`workflow/report_workflow.py`:**

Add a `mode` parameter:

```python
def run(self, *, mode: str = "channel", ...):
    # ... existing steps ...
    self._split_report(report_path)
    self._generate_llm_sections()
    if mode == "channel":
        self._generate_youtube_sections(...)
    # brand mode: primary platform already handled by _generate_llm_sections()
    self._build_typescript_bundle()
```

- `mode="channel"` (default): existing behavior, runs `_generate_youtube_sections()`
- `mode="brand"`: skips `_generate_youtube_sections()`, primary platform section is LLM-extracted like all other sections

**`scripts/run_report_workflow.py`:**

- Add `--mode` CLI arg (`channel` | `brand`, default `channel`)
- Add `--section` CLI arg (optional, for targeted single-section re-extraction — enables reconciliation loop from 1.6)

**`scripts/build_report_data_ts.py`:**

Add `instagram_social.json` as a candidate for primary platform data export:

```python
SECTION_FILE_CANDIDATES = [
    # ...
    ("youtubeData", ["youtube.json", "youtube_db.json", "instagram_social.json"]),  # added
    # ...
]
```

Note: naming it `youtubeData` in the TS export when it's Instagram data is awkward. Consider renaming to `primaryPlatformData` if the frontend can handle it, otherwise keep as-is for compatibility.

### 2.6 Existing code reused (unchanged)

- `DeepResearchClient` (`workflow/deep_research.py`) — receives different prompt, no code change
- `ReportSplitter` (`workflow/report_splitter.py`) — same splitting logic, just new patterns added
- `SectionJsonGenerator` (`llm/section_generator.py`) — same extraction architecture, new section key
- `OpenAIJsonExtractor` (`llm/openai_json_extractor.py`) — unchanged
- `build_report()` (`scripts/build_report_data_ts.py`) — same TS bundling, new candidate file

---

## Part 3: Verification

1. **Source pack completeness** — before pipeline runs, verify all source pack documents exist and pass the coverage audit
2. **Splitter test** — run `ReportSplitter` on a sample Ghost Tequila research output, verify it splits correctly including `instagram_social.md`
3. **Pipeline integration** — run full pipeline with `--mode brand`, verify:
   - YouTube DB step is skipped (no DB connection attempted)
   - `instagram_social.json` generated in `generated_sections/`
   - `reportData.ts` generated with primary platform data from `instagram_social.json`
4. **Schema validation** — all generated JSON files pass their schema definitions
5. **Cross-source check** — where Research Report A and B both claim a number, verify they agree; flag divergences
6. **Manual spot-check** — open `reportData.ts`, verify data is reasonable, confidence tags present, no hallucinated content
7. **Live comparison** — compare key IG metrics in report against actual IG profile at delivery time

---

## Appendix: Traceability to Review Feedback

| Criticism | Where addressed |
|---|---|
| 1. Plan doesn't match benchmark workflow (iterative, not pipeline) | 1.2 (source pack), 1.3 (coverage audit), 1.6 (reconciliation loop), 1.7 (QA) |
| 2. Invents architecture that doesn't exist | 2.5 — no new builder class; primary platform goes through existing LLM extraction path |
| 3. Provenance discipline missing | 1.4 (provenance system), 2.3 (confidence fields in all quantitative schemas) |
| 4. Retrieval logic too naive | N/A — DB retrieval eliminated; equivalent rigor via entity resolution (1.1) and cross-source verification (1.2, 1.4) |
| 5. Sentiment/share-of-voice treated as plug-and-play | 1.5 — sentiment axes redefined for spirits brand; share-of-voice explicitly dropped, replaced with qualitative positioning |
| 6. "Same 8 sections" too literal | 1.5 — full section-by-section semantic redesign |
| 7. Refresh/reconciliation loop missing | 1.6 — defined trigger conditions and 6-step process |
| 8. Stale model reference | 1.2 — multi-model source pack; no hardcoded model names; uses whatever `DeepResearchClient` is configured for |
