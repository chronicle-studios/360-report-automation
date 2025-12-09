from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

from workflow.deep_research import DeepResearchClient
from workflow.report_splitter import ReportSplitter
from llm.section_generator import SectionJsonGenerator
from scripts.build_report_data_ts import build_report
from scripts.generate_youtube_section import (
    DEFAULT_CHANNEL_ID,
    YouTubeSectionBuilder,
    fetch_channel,
    fetch_videos,
)

DEEP_RESEARCH_PROMPT_BODY = """
You are a senior content researcher producing a comprehensive 360° snapshot of audience engagement, cultural resonance, and cross-platform presence for the target IP. This is not a forecast; it is a present-moment, evidence-based scan meant to surface patterns of community behavior, spread, and creative echo across the entire public web.

Use only publicly verifiable information. Cite canonical URLs for every claim that isn’t self-evident from the artifact itself. Do not fabricate or assume. NO HALLUCINATION — make no claims that are not directly supported by visible public evidence. If a signal cannot be confirmed, state that clearly and mark it as ⚠️ Estimated or ❔ Sparse.

All findings must be strictly descriptive and reproducible, not speculative or interpretive.. Tag confidence on key observations as:

✅ Confirmed — directly visible, verifiable on-platform.
⚠️ Estimated — inferred from secondary or partial data (explain method).
❔ Sparse — weak signal / limited evidence (state what’s missing).

Primary platform logic: Default to YouTube for the deep dive. If another platform is clearly the center of gravity (e.g., Webtoon for a comic, Steam/Itch for a game, Twitter/X for an artist), switch the deep dive to that platform, and treat YouTube as secondary.

 Part-2 Caveat: There will be a follow-up report (Part 2) with manual YouTube metrics (concrete numbers, creator-provided). Design this report to accommodate later insertion of those numbers without re-structuring.

RESEARCH RULES & REPRODUCIBILITY

Timestamp: Record exact UTC date/time of data collection.
Queries & Filters: Log all search queries, filters, advanced operators, and platform sorting modes used.
Canonicalization: Include canonical URLs for profiles, posts, videos, threads, galleries, servers, stores, databases, and media entries.
Platform Conditions: Note platform timezones, visibility (e.g., mature tags, login walls), and any missing/hidden metrics.
Entity Disambiguation: List aliases, handle variations, localization spellings, homonyms, and explicitly exclude unrelated accounts. Identify the canonical handle/name used on major platforms.
Languages: Scan multilingual surfaces; translate non-English comments when meaningful.
Data Integrity: If data is limited, say so explicitly and reallocate effort to stronger surfaces.

WHAT TO COLLECT (ALL SURFACES; NO SHORTLISTS)

Think “every possible place and crevice people could come from.” Explore broadly and exhaustively. Examples (expand beyond these as discovered):

Video & Short-form: YouTube (channels, videos, clips), Shorts, TikTok (uploads, duets, stitches, remixes, sounds), Snapchat (Spotlight, public stories), Twitch (VODs, clips), Vimeo.

Comics & Serials: Webtoon, Tapas, GlobalComix, MangaDex (if relevant), creator sites/hosts.

Social Graphs: Twitter/X, BlueSky, Threads, Mastodon, Facebook (pages, groups), Instagram (posts, Reels, stories/highlights).

Community & Forums: Reddit (all relevant subs), Discourse/Vanilla forums, Discord servers (public info only: member counts if visible, channel topics), Kbin/Lemmy, Stack Exchange/Stack Overflow (if dev-related), Quora.

Art & Creative: DeviantArt, ArtStation, Behance, Newgrounds, Pixiv, Sketchfab; cosplay communities; GIF hubs (GIPHY, Tenor) if memes/loops exist.

Music/Audio: SoundCloud, Bandcamp, Spotify (podcasts/OSTs), YouTube Music, TikTok sound pages.

Gaming & Interactive: Steam, Itch.io, GOG, Epic Store; Metacritic, OpenCritic; mod portals (Nexus), speedrun.com; community hubs (Steam discussions).

Reviews & Databases: IMDb (if narrative), MyAnimeList/Anilist (if relevant), MobyGames, Giant Bomb wiki, HowLongToBeat.

Knowledge & Fandom: Fandom/Wikia, TV Tropes, AO3, fan wikis, Wikidata, Wikipedia (lang variants).

Search & Trends: Google/Bing search SERPs, Google Images, YouTube suggestions/related, Google Trends, keyword autosuggests.

Commercial/Support: Patreon, Ko-fi, Buy Me a Coffee; merch stores (Shopify, Etsy, Gumroad, Redbubble, TeePublic, InPrnt); crowdfunding (Kickstarter, BackerKit, Indiegogo); creator portfolios/resumes.

Press & Industry: Games press, animation/film blogs, design mags, academic cites (Google Scholar), showcases/festivals/awards, conference talks, university labs.

Link Graph: Backlinks/embeds (major blogs/substacks/newsletters), newsletter mentions, curated lists.

Localization & Regions: Non-English platforms (Bilibili, Weibo, Niconico, VK, Douyin variants if accessible), regional forums/boards.

For each platform/surface discovered, capture:

Engagement Volume: views, plays, reads, likes, favorites, comments, shares/reposts, ratings, reviews, wishlists, followers/subscribers, server members (if visible).
Shareability Patterns: reposts, remixes, duets/stitches, memes, audio reuse, quotes, embeds, cross-posts.
Sentiment Quality: tone/emotion; representative comments; polarity and intensity (multilingual noted).
Creative Echoes: fan art, reaction videos, meme edits, lore, theorycrafting, AMVs/edits, mods, cosplay.
Platform Distribution: breadth and depth across major/minor sites; where activity clusters.
Confidence Tagging: mark observations as ✅ / ⚠️ / ❔ and explain estimation methods for ⚠️.

OUTPUT STRUCTURE (NARRATIVE 360)

1) THE [HOOK] — Concise Multi-Platform Snapshot (Hero Stat)
2) [PRIMARY PLATFORM] — Deep Dive (Switchable; Charts Encouraged)
3) THE COMMUNITY — Where & How People Gather (All-Encompassing)
4) THE SENTIMENT — How People Feel
5) THE [CREATIVE/CULTURAL IMPACT] — What People Made/Did
6) THE PROOF — Commercial/Tangible Results
7) THE REACH — Geographic/Demographic Spread
8) THE OPPORTUNITIES — Future Potential & Untapped Areas

Subsection: DATA GAPS, LIMITATIONS & METHOD NOTES

CITATION & EVIDENCE FORMAT
- Every claim that isn’t visually obvious must have a live public URL.
- For comment quotes, link the exact post/thread and timestamp when possible.
- For metrics captured from UI, log screenshot notes or UI path (e.g., “Steam > Store page > right rail > user reviews”).
- For Trends/suggested terms, record query strings, region settings, and date ranges.

DELIVERABLES
- Single 360° report following the 8-section structure above (with Data Gaps subsection).
- Appendix with snapshot metadata, entity disambiguation, platform inventory.
- Placeholder block: “YouTube Manual Metrics (Part 2 Insert)”.
"""


@dataclass
class ResearchInputs:
    ip_type: str
    creator_entity: str
    title: str
    primary_url: str
    secondary_urls: Sequence[str]

    def to_prompt(self) -> str:
        secondary = (
            "\n".join(f"- {url}" for url in self.secondary_urls)
            if self.secondary_urls
            else "None provided"
        )
        return f"""TARGET SCOPE

[INPUTS]
IP Type: {self.ip_type}
Creator/Entity: {self.creator_entity}
Title: {self.title}
Primary Canonical URL: {self.primary_url}
Secondary/Official Hubs (list all):
{secondary}

{DEEP_RESEARCH_PROMPT_BODY.strip()}
"""


class ReportWorkflow:
    """
    High-level orchestrator for the full report generation pipeline.

    Steps:
      1. (Optional) Run Deep Research and store the output in a markdown file.
      2. Run the LLM extractor across all text sections (`SectionJsonGenerator`).
      3. Regenerate the YouTube JSON directly from the database.
      4. Convert canonical JSON data into `love_and_pies/reportData.ts`.
    """

    def __init__(
        self,
        *,
        text_dir: Path | str = "report_txt_sections",
        generated_dir: Path | str = "generated_sections",
        love_and_pies_dir: Path | str = "report_output",
        report_source: Path | str = "report.txt",
        youtube_channel_id: str = DEFAULT_CHANNEL_ID,
    ) -> None:
        self.text_dir = Path(text_dir)
        self.generated_dir = Path(generated_dir)
        self.love_and_pies_dir = Path(love_and_pies_dir)
        self.report_source = Path(report_source)
        self.youtube_channel_id = youtube_channel_id

        self.generated_dir.mkdir(parents=True, exist_ok=True)

        self.deep_research = DeepResearchClient()
        self.section_generator = SectionJsonGenerator(
            text_dir=self.text_dir, output_dir=self.generated_dir
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def run(
        self,
        *,
        research_prompt: Optional[str] = None,
        research_prompt_path: Optional[Path] = None,
        research_prompt_inputs: Optional[ResearchInputs] = None,
        research_output_path: Optional[Path] = None,
        report_source_path: Optional[Path] = None,
        channel_id: Optional[str] = None,
        channel_handle: Optional[str] = None,
    ) -> None:
        """
        Execute the end-to-end pipeline.
        """
        report_path = Path(report_source_path or self.report_source)

        prompt_text = self._resolve_research_prompt(
            research_prompt, research_prompt_path, research_prompt_inputs
        )
        if prompt_text:
            target = research_output_path or report_path
            self._run_deep_research(prompt_text, target)
            report_path = target

        self._split_report(report_path)
        self._generate_llm_sections()
        self._generate_youtube_sections(channel_id=channel_id, channel_handle=channel_handle)
        self._build_typescript_bundle()

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #

    def _resolve_research_prompt(
        self,
        prompt: Optional[str],
        prompt_path: Optional[Path],
        template_inputs: Optional[ResearchInputs],
    ) -> Optional[str]:
        provided = [bool(prompt), bool(prompt_path), bool(template_inputs)]
        if sum(provided) > 1:
            raise ValueError("Provide either research_prompt or research_prompt_path.")
        if prompt:
            return prompt.strip()
        if prompt_path:
            return prompt_path.read_text(encoding="utf-8").strip()
        if template_inputs:
            return template_inputs.to_prompt().strip()
        return None

    def _run_deep_research(
        self,
        prompt_text: str,
        output_path: Path,
    ) -> None:
        self.logger.info("Starting deep research request...")
        output = self.deep_research.run(prompt_text)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
        self.logger.info("Deep research output written to %s", output_path)

    def _split_report(self, report_path: Path) -> None:
        self.logger.info("Splitting report '%s' into section files...", report_path)
        if not report_path.exists():
            raise FileNotFoundError(
                f"Report source '{report_path}' not found. Provide --report-source or run deep research output there."
            )
        splitter = ReportSplitter(report_path, self.text_dir)
        splitter.split()
        self.logger.info("Section files updated in %s", self.text_dir)

    def _generate_llm_sections(self) -> None:
        self.logger.info("Running LLM extraction for sections...")
        self.section_generator.generate_all()
        self.logger.info("LLM extraction complete. JSON written to %s", self.generated_dir)

    def _generate_youtube_sections(
        self, *, channel_id: Optional[str], channel_handle: Optional[str]
    ) -> None:
        youtube_id = channel_id or self.youtube_channel_id
        self.logger.info("Generating YouTube section from database for %s...", youtube_id)
        channel = fetch_channel(youtube_id)
        videos = fetch_videos(youtube_id)
        builder = YouTubeSectionBuilder(channel, videos)
        payload = builder.build()

        self._write_json(self.generated_dir / "youtube_db.json", payload)
        target = self.love_and_pies_dir / "youtube.json"
        if channel_handle:
            payload.setdefault("channelOverview", {})["handle"] = channel_handle
        self._write_json(target, payload)
        self.logger.info("YouTube JSON refreshed (expected + generated).")

    def _build_typescript_bundle(self) -> None:
        self.logger.info("Rebuilding TypeScript bundle...")
        build_report(
            self.love_and_pies_dir,
            self.love_and_pies_dir / "reportData.ts",
            generated_dir=self.generated_dir,
        )
        self.logger.info("TypeScript bundle updated at %s", self.love_and_pies_dir / "reportData.ts")

    def _write_json(self, path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

