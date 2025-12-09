#!/usr/bin/env python3
"""
Utility for running OpenAI's o3 Deep Research workflow.

Usage examples:
    python scripts/deep_research_client.py --prompt-file research_prompts/semaglutide.txt
    python scripts/deep_research_client.py --prompt "Research the XYZ market..."
"""

from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

from workflow.deep_research import DeepResearchClient


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run OpenAI deep research requests.")
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument(
        "--prompt",
        help="Inline prompt text.",
    )
    prompt_group.add_argument(
        "--prompt-file",
        type=Path,
        help="Path to a text file containing the prompt.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=3600,
        help="Request timeout in seconds (default: 3600).",
    )
    parser.add_argument(
        "--background",
        action="store_true",
        help="Run in background mode (returns immediately with job ID).",
    )
    parser.add_argument(
        "--no-web-search",
        action="store_true",
        help="Disable web search tool.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.prompt:
        prompt_text = args.prompt
    else:
        prompt_text = args.prompt_file.read_text(encoding="utf-8")

    prompt_text = textwrap.dedent(prompt_text).strip()
    if not prompt_text:
        raise SystemExit("Prompt text is empty.")

    client = DeepResearchClient(
        model=args.model,
        timeout=args.timeout,
        use_web_search=not args.no_web_search,
    )
    output = client.run(prompt_text, background=args.background)

    print(output)


if __name__ == "__main__":
    main()

