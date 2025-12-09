from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv(".env")

try:
    from openai import OpenAI
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "openai package not installed. Install with `pip install openai`."
    ) from exc


DEFAULT_MODEL = "o3-deep-research"


@dataclass
class DeepResearchClient:
    """
    Thin wrapper around OpenAI's Deep Research API.

    Parameters
    ----------
    model:
        OpenAI model identifier (defaults to o3-deep-research).
    timeout:
        HTTP timeout (seconds) for the OpenAI client.
    use_web_search:
        Whether to attach the web_search_preview tool to requests by default.
    """

    model: str = DEFAULT_MODEL
    timeout: int = 3600
    use_web_search: bool = True

    def __post_init__(self) -> None:
        self._client = OpenAI(timeout=self.timeout)

    def _build_tools(self, use_web_search: Optional[bool]) -> list[dict]:
        enabled = self.use_web_search if use_web_search is None else use_web_search
        if not enabled:
            return []
        return [{"type": "web_search_preview"}]

    def run(
        self,
        prompt: str,
        *,
        background: bool = False,
        use_web_search: Optional[bool] = None,
        model: Optional[str] = None,
    ) -> str:
        """
        Execute a deep research request and return the formatted output.
        """

        response = self._client.responses.create(
            model=model or self.model,
            input=prompt,
            background=background,
            tools=self._build_tools(use_web_search),
        )

        if background:
            return (
                "Background job started. Response ID: "
                f"{getattr(response, 'id', '<unknown>')}"
            )

        if hasattr(response, "output_text"):
            return response.output_text  # type: ignore[attr-defined]

        return json.dumps(response.to_dict(), indent=2)

