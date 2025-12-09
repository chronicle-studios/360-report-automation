from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SectionDefinition:
    key: str
    filename: str
    patterns: tuple[str, ...]


SECTION_DEFINITIONS: List[SectionDefinition] = [
    SectionDefinition("metadata", "metadata.md", ("^#+\\s*(the\\s+)?hook",)),
    SectionDefinition("overview", "overview.md", ("^#+\\s*overview",)),
    SectionDefinition("primary_platform", "youtube.md", ("^#+\\s*youtube", "^#+\\s*primary\\s+platform")),
    SectionDefinition("community", "community.md", ("^#+\\s*(the\\s+)?community",)),
    SectionDefinition("sentiment", "sentiment.md", ("^#+\\s*(the\\s+)?sentiment",)),
    SectionDefinition("creative", "creative_impact.md", ("^#+\\s*(the\\s+)?creative",)),
    SectionDefinition("proof", "commercial_success.md", ("^#+\\s*(the\\s+)?proof",)),
    SectionDefinition("reach", "geographic_reach.md", ("^#+\\s*(the\\s+)?reach",)),
    SectionDefinition("opportunities", "opportunities.md", ("^#+\\s*(the\\s+)?opportunities",)),
    SectionDefinition("data_gaps", "data_gaps.md", ("^#+\\s*data\\s+gaps",)),
]


class ReportSplitter:
    """
    Splits a consolidated research report into section-specific markdown files.
    """

    def __init__(self, source_path: Path | str, output_dir: Path | str) -> None:
        self.source_path = Path(source_path)
        self.output_dir = Path(output_dir)

    def split(self) -> Dict[str, str]:
        text = self.source_path.read_text(encoding="utf-8")
        sections = self._extract_sections(text)
        if "overview" not in sections and "metadata" in sections:
            sections["overview"] = sections["metadata"]
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Track found and missing sections
        found_sections = []
        missing_sections = []
        
        for definition in SECTION_DEFINITIONS:
            content = sections.get(definition.key)
            if not content:
                missing_sections.append(definition.key)
                logger.warning(
                    f"Section '{definition.key}' not found in report. "
                    f"Expected patterns: {definition.patterns}"
                )
                continue
            found_sections.append(definition.key)
            target = self.output_dir / definition.filename
            target.write_text(content.strip() + "\n", encoding="utf-8")

        # Log summary
        logger.info(f"✓ Found {len(found_sections)} sections: {', '.join(found_sections)}")
        if missing_sections:
            logger.warning(f"⚠ Missing {len(missing_sections)} sections: {', '.join(missing_sections)}")
            
        # Error if critical sections are missing
        critical_sections = {"metadata", "primary_platform", "community"}
        missing_critical = critical_sections.intersection(missing_sections)
        if missing_critical:
            raise ValueError(
                f"Critical sections missing from report: {', '.join(missing_critical)}. "
                f"Report splitting failed. Check that your report.txt contains these sections "
                f"with proper headers (e.g., '# THE HOOK', '# YOUTUBE', '# THE COMMUNITY')."
            )

        return sections

    def _extract_sections(self, text: str) -> Dict[str, str]:
        current_key: str | None = None
        buffers: Dict[str, List[str]] = {definition.key: [] for definition in SECTION_DEFINITIONS}

        lines = text.splitlines()
        for line in lines:
            section_key = self._match_section(line)
            if section_key:
                current_key = section_key
                buffers[current_key].append(line)
                continue

            if current_key:
                buffers[current_key].append(line)

        return {key: "\n".join(buffer).strip() for key, buffer in buffers.items() if buffer}

    def _match_section(self, line: str) -> str | None:
        for definition in SECTION_DEFINITIONS:
            for pattern in definition.patterns:
                if re.match(pattern, line, flags=re.IGNORECASE):
                    return definition.key
        return None

