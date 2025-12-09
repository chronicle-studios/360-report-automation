import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI

DEFAULT_MODEL = "gpt-5"


@dataclass
class JsonExtractionRequest:
    section_name: str
    section_text: str
    schema: Dict[str, Any]
    schema_description: Optional[str] = None


class OpenAIJsonExtractor:
    """Thin wrapper around OpenAI's Responses API geared toward JSON extraction."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        base_url: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAIJsonExtractor requires OPENAI_API_KEY env var or api_key argument."
            )
        self.model = model
        client_kwargs = {"api_key": self.api_key}
        if base_url:
            client_kwargs["base_url"] = base_url.rstrip("/")
        self.client = OpenAI(**client_kwargs)

    def extract_json(self, request: JsonExtractionRequest) -> str:
        schema = self._enforce_additional_properties(request.schema)

        response = self.client.responses.create(
            model=self.model,
            input=self._build_prompt(request),
            text={
                "format": {
                    "type": "json_schema",
                    "name": f"{request.section_name.replace(' ', '')}Extraction",
                    "schema": schema,
                }
            },
        )

        return self._extract_text_from_response(response)

    @staticmethod
    def _build_prompt(request: JsonExtractionRequest) -> str:
        schema_note = (
            f"Schema guidance: {request.schema_description}\n\n"
            if request.schema_description
            else ""
        )
        parts = [
            "You are an extraction model that produces strict JSON.",
            schema_note,
            f"Section Name: {request.section_name}",
            "Extract structured data that fits the provided schema from the following text.",
            "Return JSON only, no markdown or prose.",
            "-----",
            request.section_text.strip(),
        ]
        return "\n".join(filter(None, parts))

    @classmethod
    def _enforce_additional_properties(cls, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure every object type has additionalProperties: false (per Responses API requirement)."""

        def recurse(node: Any) -> Any:
            if isinstance(node, dict):
                new_node = {k: recurse(v) for k, v in node.items() if k not in ("properties", "items")}
                node_type = node.get("type")

                if node_type == "object":
                    props = node.get("properties", {})
                    new_node["properties"] = {k: recurse(v) for k, v in props.items()}
                    new_node.setdefault("additionalProperties", False)
                elif node_type == "array" and "items" in node:
                    new_node["items"] = recurse(node["items"])

                return new_node
            if isinstance(node, list):
                return [recurse(item) for item in node]
            return node

        return recurse(schema)

    @staticmethod
    def _extract_text_from_response(response: Any) -> str:
        """Find the first assistant message content containing text."""
        if not response or not getattr(response, "output", None):
            return ""

        for item in response.output:
            if getattr(item, "type", None) == "message" and getattr(item, "content", None):
                for part in item.content:
                    text = getattr(part, "text", None)
                    if text:
                        return text
        return ""


# def main() -> None:
#     """Simple demo without CLI args."""
#     sample_text = "Love & Pies has 245K Instagram followers and 201K on Facebook."
#     schema = {
#         "type": "object",
#         "properties": {
#             "platform": {"type": "string"},
#             "metric": {"type": "string"},
#         },
#         "required": ["platform", "metric"],
#     }

#     extractor = OpenAIJsonExtractor()
#     request = JsonExtractionRequest(
#         section_name="Demo",
#         section_text=sample_text,
#         schema=schema,
#         schema_description="Extract a single platform + metric mentioned in the text.",
#     )
#     print(extractor.extract_json(request))


# if __name__ == "__main__":
#     main()

