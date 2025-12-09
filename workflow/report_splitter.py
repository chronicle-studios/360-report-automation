from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass(frozen=True)
class SectionDefinition:
    key: str
    filename: str
    patterns: tuple[str, ...]


SECTION_DEFINITIONS: List[SectionDefinition] = [
    SectionDefinition("metadata", "metadata.md", ("^The Hook",)),
    SectionDefinition("overview", "overview.md", ("^Overview",)),
    SectionDefinition("primary_platform", "youtube.md", ("^YouTube", "^Primary Platform")),
    SectionDefinition("community", "community.md", ("^The Community",)),
    SectionDefinition("sentiment", "sentiment.md", ("^The Sentiment",)),
    SectionDefinition("creative", "creative_impact.md", ("^The Creative",)),
    SectionDefinition("proof", "commercial_success.md", ("^The Proof",)),
    SectionDefinition("reach", "geographic_reach.md", ("^The Reach",)),
    SectionDefinition("opportunities", "opportunities.md", ("^The Opportunities",)),
    SectionDefinition("data_gaps", "data_gaps.md", ("^Data Gaps", "^Subsection: DATA GAPS")),
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

        for definition in SECTION_DEFINITIONS:
            content = sections.get(definition.key)
            if not content:
                continue
            target = self.output_dir / definition.filename
            target.write_text(content.strip() + "\n", encoding="utf-8")

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

