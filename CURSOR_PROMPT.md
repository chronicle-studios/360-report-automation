# Ghost Tequila 360 Report — Cursor Execution Guide

## What This Is

A pipeline that produces a 360-degree audience analysis report for Ghost Tequila (ghosttequila.com), a ghost pepper-infused tequila brand. The pipeline uses OpenAI's o3-deep-research model for live web research and gpt-5 for structured JSON extraction.

## What's Already Done

All code changes are complete on branch `claude/360-analysis-ghost-tequila-x4FZG`. No code needs to be written. You just need to run it.

### Files changed from main:
- `ghost_tequila/GHOST_TEQUILA_METHODOLOGY.md` — methodology document (reference only, not used by pipeline)
- `ghost_tequila/ghost_tequila_research_prompt.md` — the research prompt sent to o3-deep-research
- `workflow/report_splitter.py` — added Instagram/Social header patterns
- `workflow/report_workflow.py` — added `mode` parameter ("channel" or "brand")
- `llm/section_generator.py` — added `instagram_social` section config
- `prompts/section_schemas.py` — added `instagram_social` schema, replaced `supercellInvestment` with `notableHighlight`
- `prompts/section_prompts.py` — added `instagram_social` extraction prompt, updated commercial prompt
- `scripts/run_report_workflow.py` — added `--mode` CLI flag
- `scripts/build_report_data_ts.py` — added `instagram_social.json` as TS bundle candidate
- `Dockerfile` — container definition
- `run_ghost_tequila.sh` — convenience script

## How to Run (Container — Recommended)

### Prerequisites
- Docker installed
- `OPENAI_API_KEY` environment variable set (or in `.env` file at repo root)

### Option A: Shell script
```bash
# Create .env if needed
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# Run
./run_ghost_tequila.sh
```

### Option B: Manual docker commands
```bash
docker build -t ghost-tequila-360 .

docker run --rm \
    -e OPENAI_API_KEY="$OPENAI_API_KEY" \
    -v ./ghost_tequila:/app/ghost_tequila \
    -v ./generated_sections:/app/generated_sections \
    -v ./report_txt_sections:/app/report_txt_sections \
    -v ./report_output:/app/report_output \
    ghost-tequila-360
```

### Option C: Run locally without Docker
```bash
pip install -r requirements.txt

# Create .env
echo "OPENAI_API_KEY=sk-your-key-here" > .env

python scripts/run_report_workflow.py \
    --mode brand \
    --research-prompt-file ghost_tequila/ghost_tequila_research_prompt.md \
    --research-output ghost_tequila/report.txt \
    --report-source ghost_tequila/report.txt \
    --verbose
```

## What the Pipeline Does (Step by Step)

```
Step 1: Deep Research (10-30 minutes)
  └── Sends ghost_tequila_research_prompt.md to OpenAI o3-deep-research
  └── Model performs live web searches across Instagram, Drizly, Reddit, review sites, etc.
  └── Outputs: ghost_tequila/report.txt (large markdown file)

Step 2: Report Splitting (instant)
  └── Regex-based parser splits report.txt into 10 section .md files
  └── Outputs: report_txt_sections/{metadata,overview,youtube,community,sentiment,...}.md
  └── NOTE: the Instagram section lands in youtube.md (legacy filename, content is Instagram)

Step 3: LLM Extraction (2-5 minutes)
  └── For each section: sends text + JSON schema to gpt-5
  └── gpt-5 returns strict JSON matching the schema
  └── Runs 4 sections in parallel (ThreadPoolExecutor)
  └── Outputs: generated_sections/{metadata,overview,instagram_social,community,...}.json

Step 4: YouTube DB — SKIPPED in brand mode
  └── --mode brand skips this entirely (Ghost Tequila has no YouTube channel)

Step 5: TypeScript Bundle (instant)
  └── Converts all JSON files into report_output/reportData.ts
  └── Exports: reportMetadata, platformStats, chapters, overviewData, youtubeData, etc.
```

## Outputs

| File | What it is |
|------|-----------|
| `ghost_tequila/report.txt` | Raw research markdown from o3-deep-research |
| `report_txt_sections/*.md` | Split section files (10 files) |
| `generated_sections/*.json` | Extracted structured JSON (9 files) |
| `report_output/reportData.ts` | Final TypeScript bundle for frontend |

## Pipeline Architecture

```
Technologies:
  - OpenAI o3-deep-research — live web research with web_search_preview tool
  - OpenAI gpt-5 — structured JSON extraction via Responses API (json_schema mode)
  - Python 3.12 — orchestration, regex splitting, threading
  - No database needed for brand mode (PostgreSQL is only for YouTube channel reports)

Key files:
  workflow/deep_research.py    — OpenAI deep research API wrapper
  workflow/report_splitter.py  — regex markdown parser
  workflow/report_workflow.py  — orchestrator (the run() method)
  llm/openai_json_extractor.py — gpt-5 JSON extraction
  llm/section_generator.py     — parallel section processing
  prompts/section_schemas.py   — JSON Schema definitions
  prompts/section_prompts.py   — extraction instructions per section
```

## After the Pipeline Runs

### Manual review checklist (before delivering)
1. Open `ghost_tequila/report.txt` and verify:
   - Entity disambiguation is clean (no Ghost protein/energy contamination)
   - Instagram was found and metrics captured
   - Confidence tags are present and honest
   - No hallucinated URLs
2. Spot-check 5+ URLs from the research output
3. Compare Instagram follower count in report vs actual @ghosttequila profile
4. Open `generated_sections/instagram_social.json` and verify data looks reasonable
5. Open `report_output/reportData.ts` and verify it generated without errors

### If a section is thin or wrong
Re-run just that section's extraction:
```python
from llm.section_generator import SectionJsonGenerator
gen = SectionJsonGenerator()
gen.generate_section("instagram_social")  # or "community", "sentiment", etc.
```

Then rebuild the TS bundle:
```python
from scripts.build_report_data_ts import build_report
from pathlib import Path
build_report(Path("report_output"), Path("report_output/reportData.ts"), generated_dir=Path("generated_sections"))
```

## Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `OPENAI_API_KEY` | Yes | OpenAI API access for o3-deep-research and gpt-5 |
| `DB_USER` | No | Not needed for brand mode |
| `DB_PASSWORD` | No | Not needed for brand mode |
| `DB_NAME` | No | Not needed for brand mode |
| `DB_HOST` | No | Not needed for brand mode |

## Deadline

April 15, 2026. This is a one-time request (Linear ticket ENG-423).
