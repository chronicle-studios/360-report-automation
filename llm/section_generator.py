from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Iterable, Optional

from prompts.section_prompts import SECTION_PROMPTS
from prompts.section_schemas import SECTION_SCHEMAS
from .openai_json_extractor import JsonExtractionRequest, OpenAIJsonExtractor


@dataclass(frozen=True)
class SectionConfig:
    key: str
    label: str
    text_path: Path
    output_path: Path


class SectionJsonGenerator:
    """Coordinates prompt + schema + text extraction for each report section."""

    def __init__(
        self,
        *,
        extractor: Optional[OpenAIJsonExtractor] = None,
        text_dir: Path | str = "report_txt_sections",
        output_dir: Path | str = "generated_sections",
    ) -> None:
        self.extractor = extractor or OpenAIJsonExtractor()
        self.text_dir = Path(text_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self._configs = self._build_configs()

    def _build_configs(self) -> Dict[str, SectionConfig]:
        section_map = {
            "metadata": ("Metadata", "metadata.md"),
            "overview": ("Overview", "overview.md"),
            "community": ("Community", "community.md"),
            "sentiment": ("Sentiment", "sentiment.md"),
            "creative": ("Creative Impact", "creative_impact.md"),
            "commercial": ("Commercial Success", "commercial_success.md"),
            "geographic": ("Geographic Reach", "geographic_reach.md"),
            "data_gaps": ("Data Gaps", "data_gaps.md"),
        }

        configs: Dict[str, SectionConfig] = {}
        for key, (label, filename) in section_map.items():
            text_path = self.text_dir / filename
            output_path = self.output_dir / f"{key}.json"
            configs[key] = SectionConfig(
                key=key, label=label, text_path=text_path, output_path=output_path
            )
        return configs

    def available_sections(self) -> Iterable[str]:
        return self._configs.keys()

    def generate_section(self, key: str) -> str:
        if key not in self._configs:
            raise KeyError(f"Unknown section key '{key}'.")
        config = self._configs[key]
        if key not in SECTION_PROMPTS:
            raise KeyError(f"No prompt defined for section '{key}'.")
        if key not in SECTION_SCHEMAS:
            raise KeyError(f"No schema defined for section '{key}'.")

        section_text = config.text_path.read_text(encoding="utf-8")
        schema = SECTION_SCHEMAS[key]
        prompt = SECTION_PROMPTS[key]

        request = JsonExtractionRequest(
            section_name=config.label,
            section_text=section_text,
            schema=schema,
            schema_description=prompt,
        )
        result = self.extractor.extract_json(request)
        config.output_path.write_text(result, encoding="utf-8")
        return result

    def generate_all(self, max_workers: int = 4) -> Dict[str, str]:
        outputs: Dict[str, str] = {}

        def _task(key: str) -> tuple[str, str]:
            return key, self.generate_section(key)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_task, key): key for key in self.available_sections()}
            for future in as_completed(futures):
                key, result = future.result()
                outputs[key] = result

        return outputs

if __name__ == "__main__":

    generator = SectionJsonGenerator()
    print(generator.generate_all())