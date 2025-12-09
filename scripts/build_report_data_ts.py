#!/usr/bin/env python3
"""
Regenerate love_and_pies/reportData.ts from the JSON payloads in love_and_pies/*.json.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]


def read_first_json_object(path: Path):
    text = path.read_text(encoding="utf-8").lstrip()
    decoder = json.JSONDecoder()
    obj, _ = decoder.raw_decode(text)
    return obj


def json_to_ts_literal(obj) -> str:
    text = json.dumps(obj, indent=2, ensure_ascii=False)
    # Remove quotes around simple object keys to match TS style.
    text = re.sub(r'(?m)^(\s*)"([A-Za-z0-9_]+)":', r"\1\2:", text)
    # Convert confidence fields to literal types.
    text = re.sub(r'(confidence:\s*)"([^"]+)"', r'\1"\2" as const', text)
    return text


def export_block(const_name: str, value) -> str:
    ts_literal = json_to_ts_literal(value)
    return f"export const {const_name} = {ts_literal};\n"


SECTION_FILE_CANDIDATES = [
    ("overviewData", ["overview.json"]),
    ("youtubeData", ["youtube.json", "youtube_db.json"]),
    ("communityData", ["community.json"]),
    ("sentimentData", ["sentiment.json"]),
    ("creativeData", ["creative_impact.json", "creative.json"]),
    ("commercialData", ["commercial_success.json", "commercial.json"]),
    ("geographicData", ["geographic_reach.json", "geographic.json"]),
    ("dataGapsData", ["data_gaps.json"]),
]


def resolve_json_path(
    filename: str,
    canonical_dir: Path,
    generated_dir: Optional[Path] = None,
) -> Path:
    candidates = []
    if generated_dir is not None:
        candidates.append(generated_dir / filename)
    candidates.append(canonical_dir / filename)
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(
        f"Could not find {filename}; looked in {[str(p) for p in candidates]}"
    )


def resolve_section_path(
    canonical_dir: Path,
    generated_dir: Optional[Path],
    candidate_names,
) -> Path:
    candidates = []
    if generated_dir is not None:
        candidates.extend(generated_dir / name for name in candidate_names)
    candidates.extend(canonical_dir / name for name in candidate_names)
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(
        f"No JSON found for section; looked in {[str(p) for p in candidates]}"
    )


def build_report(
    canonical_dir: Path,
    output_file: Path,
    *,
    generated_dir: Optional[Path] = None,
):
    metadata_path = resolve_json_path(
        "metadata.json", canonical_dir, generated_dir=generated_dir
    )
    metadata = read_first_json_object(metadata_path)
    parts = ["// Love & Pies Report Data (auto-generated from love_and_pies JSONs)\n"]

    parts.append(export_block("reportMetadata", metadata.get("reportMetadata", {})))
    parts.append(export_block("platformStats", metadata.get("platformStats", [])))
    parts.append(export_block("chapters", metadata.get("chapters", [])))
    parts.append("\n")

    for const_name, candidates in SECTION_FILE_CANDIDATES:
        path = resolve_section_path(canonical_dir, generated_dir, candidates)
        section_obj = read_first_json_object(path)
        parts.append(export_block(const_name, section_obj))
        parts.append("\n")

    report_meta = metadata.get("reportMetadata", {})
    footer = {
        "title": f"{report_meta.get('title', 'Love & Pies')} {report_meta.get('subtitle', '')}".strip(),
        "snapshotDate": f"Snapshot captured {report_meta.get('date', '')} UTC".strip(),
        "disclaimer": "All data from publicly available sources",
    }
    parts.append(export_block("footerData", footer))

    output_file.write_text("".join(parts), encoding="utf-8")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Build reportData.ts from JSON sources.")
    parser.add_argument(
        "--source",
        type=Path,
        default=ROOT / "love_and_pies",
        help="Directory containing metadata.json and section JSON files.",
    )
    parser.add_argument(
        "--generated-source",
        type=Path,
        help="Optional directory containing freshly generated JSON files (checked first).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "love_and_pies" / "reportData.ts",
        help="Path to write the TypeScript output.",
    )
    args = parser.parse_args()

    build_report(args.source, args.output, generated_dir=args.generated_source)


if __name__ == "__main__":
    main()

