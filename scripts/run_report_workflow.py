#!/usr/bin/env python3
"""Entry point for the full Love & Pies report generation workflow."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from workflow.report_workflow import ReportWorkflow, ResearchInputs

DEFAULT_RESEARCH_PROMPT_PATH = Path("prompts/deep_research_prompt.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the report generation workflow.")
    prompt_group = parser.add_mutually_exclusive_group(required=False)
    prompt_group.add_argument(
        "--research-prompt",
        help="Inline prompt text for the deep research step.",
    )
    prompt_group.add_argument(
        "--research-prompt-file",
        type=Path,
        help="Path to a file containing the deep research prompt.",
    )
    prompt_group.add_argument(
        "--use-default-research-prompt",
        action="store_true",
        help="Use prompts/deep_research_prompt.md as the deep research prompt.",
    )
    parser.add_argument(
        "--research-output",
        type=Path,
        help="Optional path to store the deep research output (defaults to report_txt_sections/deep_research.md).",
    )
    parser.add_argument(
        "--text-dir",
        type=Path,
        default=Path("report_txt_sections"),
        help="Directory containing section markdown files (default: report_txt_sections).",
    )
    parser.add_argument(
        "--generated-dir",
        type=Path,
        default=Path("generated_sections"),
        help="Directory for LLM generated JSON (default: generated_sections).",
    )
    parser.add_argument(
        "--report-source",
        type=Path,
        default=Path("report.txt"),
        help="Path to the consolidated research report text (default: report.txt).",
    )
    parser.add_argument(
        "--channel-id",
        default="UCo20o67CyQtq7CJKoiDixEw",
        help="YouTube channel ID for DB-driven metrics (default: Love & Pies channel).",
    )
    parser.add_argument(
        "--channel-handle",
        help="Optional channel handle (e.g. @loveandpiesgame) to store for reference.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )
    parser.add_argument("--ip-type", help="IP type descriptor for template prompt.")
    parser.add_argument("--creator", help="Creator or entity name for template prompt.")
    parser.add_argument("--title", help="Title of the IP for template prompt.")
    parser.add_argument("--primary-url", help="Primary canonical URL.")
    parser.add_argument(
        "--secondary-url",
        action="append",
        help="Secondary/official hub URL (can be provided multiple times).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    workflow = ReportWorkflow(
        text_dir=args.text_dir,
        generated_dir=args.generated_dir,
        love_and_pies_dir=Path("report_output"),
        report_source=args.report_source,
        youtube_channel_id=args.channel_id,
    )

    research_inputs = None
    if args.ip_type and args.creator and args.title and args.primary_url:
        research_inputs = ResearchInputs(
            ip_type=args.ip_type,
            creator_entity=args.creator,
            title=args.title,
            primary_url=args.primary_url,
            secondary_urls=args.secondary_url or [],
        )

    prompt_path = args.research_prompt_file
    if args.use_default_research_prompt:
        prompt_path = DEFAULT_RESEARCH_PROMPT_PATH

    workflow.run(
        research_prompt=args.research_prompt,
        research_prompt_path=prompt_path,
        research_prompt_inputs=research_inputs,
        research_output_path=args.research_output,
        report_source_path=args.report_source,
        channel_id=args.channel_id,
        channel_handle=args.channel_handle,
    )


if __name__ == "__main__":
    main()

