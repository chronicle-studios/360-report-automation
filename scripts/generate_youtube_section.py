#!/usr/bin/env python3
"""
Generate the full YouTube section JSON directly from the database for a channel.

This bypasses the LLM flow so we can rely on deterministic metrics for channels
where we already control the underlying data (e.g., Love & Pies).
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import statistics
from typing import Dict, Iterable, List, Optional

from dotenv import load_dotenv

load_dotenv(".env")

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from db import db_manager  # noqa: E402


DEFAULT_CHANNEL_ID = "UCo20o67CyQtq7CJKoiDixEw"
DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT / "generated_sections" / "youtube_from_db.json"
)


@dataclass
class ChannelRow:
    channel_id: str
    handle: Optional[str]
    creator_name: Optional[str]
    subscriber_count: Optional[int]
    total_views: Optional[int]
    video_count: Optional[int]
    created_at: Optional[datetime]
    collected_at: Optional[datetime]


@dataclass
class VideoRow:
    video_id: str
    title: str
    views: int
    likes: int
    comments: int
    length_seconds: Optional[int]
    date_posted: datetime
    post_type: Optional[str]

    @property
    def engagement(self) -> int:
        return (self.likes or 0) + (self.comments or 0)

    @property
    def content_type(self) -> str:
        if self.post_type:
            normalized = self.post_type.upper()
            if normalized == "SHORT":
                return "Shorts"
            if normalized == "VIDEO":
                return "Long-form"
            if normalized == "LIVE":
                return "Livestreams"
        if self.length_seconds is None:
            return "Long-form"
        return "Shorts" if self.length_seconds < 60 else "Long-form"

    @property
    def duration_bucket(self) -> str:
        if self.length_seconds is None:
            return "5+ min"
        if self.length_seconds < 60:
            return "< 1 min"
        if self.length_seconds < 300:
            return "1-5 min"
        return "5+ min"

    @property
    def duration_display(self) -> str:
        if self.length_seconds is None:
            return "—"
        seconds = self.length_seconds
        if seconds < 60:
            return f"{seconds}s"
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes}m"
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours}h {minutes}m"


def fetch_channel(channel_id: str) -> ChannelRow:
    with db_manager.get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT channel_id, handle, creator_name, subscriber_count, total_views,
                   video_count, created_at, collected_at
            FROM channels
            WHERE channel_id = %s
            """,
            (channel_id,),
        )
        row = cur.fetchone()
        if not row:
            raise SystemExit(f"Channel not found: {channel_id}")
        return ChannelRow(*row)


def fetch_videos(channel_id: str) -> List[VideoRow]:
    with db_manager.get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT video_id,
                   COALESCE(title, ''),
                   COALESCE(views, 0),
                   COALESCE(likes, 0),
                   COALESCE(num_comments, 0),
                   video_length,
                   date_posted,
                   post_type
            FROM videos
            WHERE channel_id = %s
              AND date_posted IS NOT NULL
            ORDER BY views DESC
            """,
            (channel_id,),
        )
        videos = []
        for row in cur.fetchall():
            date_posted = row[6]
            if date_posted is None:
                continue
            videos.append(
                VideoRow(
                    video_id=row[0],
                    title=row[1],
                    views=int(row[2] or 0),
                    likes=int(row[3] or 0),
                    comments=int(row[4] or 0),
                    length_seconds=row[5],
                    date_posted=date_posted,
                    post_type=row[7],
                )
            )
        if not videos:
            raise SystemExit(f"No videos found for channel {channel_id}")
        return videos


def format_human_number(value: Optional[float]) -> str:
    if value is None:
        return "0"
    abs_value = abs(value)
    suffix = ""
    divisor = 1
    if abs_value >= 1_000_000:
        suffix = "M"
        divisor = 1_000_000
    elif abs_value >= 1_000:
        suffix = "K"
        divisor = 1_000
    number = value / divisor
    if divisor == 1:
        return f"{number:,.0f}"
    return f"{number:.2f}".rstrip("0").rstrip(".") + suffix


def format_percent(value: Optional[float]) -> str:
    if value is None:
        return "0%"
    return f"{value * 100:.2f}%"


def safe_mean(values: Iterable[float]) -> float:
    values = list(values)
    if not values:
        return 0.0
    return statistics.mean(values)


def safe_median(values: Iterable[float]) -> float:
    values = list(values)
    if not values:
        return 0.0
    return statistics.median(values)


class YouTubeSectionBuilder:
    def __init__(self, channel: ChannelRow, videos: List[VideoRow]):
        self.channel = channel
        self.videos = videos
        self.total_views = sum(v.views for v in videos)
        self.total_likes = sum(v.likes for v in videos)
        self.total_comments = sum(v.comments for v in videos)
        self.engagement_total = self.total_likes + self.total_comments
        self.reference_date = max(v.date_posted for v in videos)
        self.channel_age_days = max(
            1,
            (self.reference_date.date() - channel.created_at.date()).days
            if channel.created_at
            else 365,
        )

    def build(self) -> Dict:
        """Return the trimmed schema expected by love_and_pies/youtube.json."""
        return {
            "channelOverview": self.channel_overview(),
            "performanceMetrics": self.performance_metrics(),
            "currentYearAnalysis": self.current_year_analysis(),
            "topVideos": self.top_videos_table(),
        }

    def channel_overview(self) -> Dict:
        subscribers = self.channel.subscriber_count or 0
        created_at_str = (
            self.channel.created_at.strftime("%b %d, %Y")
            if self.channel.created_at
            else "—"
        )
        channel_age_years = self.channel_age_days / 365
        return {
            "subscribers": format_human_number(subscribers),
            "totalViews": format_human_number(self.channel.total_views or self.total_views),
            "totalLikes": format_human_number(self.total_likes),
            "totalComments": format_human_number(self.total_comments),
            "channelName": self.channel.creator_name or "Unknown",
            "handle": self.channel.handle or "",
            "channelCreated": created_at_str,
            "channelAge": f"{channel_age_years:.1f} years",
            "videosInDataset": str(len(self.videos)),
        }

    def performance_metrics(self) -> Dict:
        avg_views = safe_mean(v.views for v in self.videos)
        avg_likes = safe_mean(v.likes for v in self.videos)
        avg_comments = safe_mean(v.comments for v in self.videos)
        median_views = safe_median(v.views for v in self.videos)
        like_ratio = (
            self.total_likes / self.total_views if self.total_views else 0.0
        )
        comment_ratio = (
            self.total_comments / self.total_views if self.total_views else 0.0
        )
        engagement_rate = (
            self.engagement_total / self.total_views if self.total_views else 0.0
        )
        return {
            "avgViewsPerVideo": format_human_number(avg_views),
            "avgLikesPerVideo": format_human_number(avg_likes),
            "avgCommentsPerVideo": format_human_number(avg_comments),
            "medianViews": format_human_number(median_views),
            "avgLikeViewRatio": format_percent(like_ratio),
            "avgCommentViewRatio": format_percent(comment_ratio),
            "avgEngagementRate": format_percent(engagement_rate),
        }

    def current_year_analysis(self) -> Dict:
        current_year = max(v.date_posted.year for v in self.videos)
        monthly: Dict[int, Dict[str, List[int]]] = defaultdict(
            lambda: {"views": [], "likes": [], "comments": []}
        )
        for v in self.videos:
            if v.date_posted.year != current_year:
                continue
            month = v.date_posted.month
            monthly[month]["views"].append(v.views)
            monthly[month]["likes"].append(v.likes)
            monthly[month]["comments"].append(v.comments)

        monthly_data = []
        for month in sorted(monthly.keys()):
            monthly_data.append(
                {
                    "month": datetime(1900, month, 1).strftime("%b"),
                    "views": round(safe_mean(monthly[month]["views"]), 2),
                    "likes": round(safe_mean(monthly[month]["likes"]), 2),
                    "comments": round(safe_mean(monthly[month]["comments"]), 2),
                }
            )

        best_month = max(monthly_data, key=lambda m: m["views"]) if monthly_data else None
        summary_cards = []
        if best_month:
            summary_cards.append(
                {
                    "label": "Best Month by Views",
                    "value": best_month["month"],
                    "detail": f"{format_human_number(best_month['views'])} avg views",
                }
            )
        if len(monthly_data) >= 2:
            trend = "Positive" if monthly_data[-1]["views"] >= monthly_data[0]["views"] else "Negative"
            summary_cards.append(
                {
                    "label": "Engagement Trend",
                    "value": trend,
                    "detail": f"{monthly_data[0]['month']} → {monthly_data[-1]['month']}",
                }
            )
        monthly_videos = sum(len(vals["views"]) for vals in monthly.values())
        summary_cards.append(
            {
                "label": "Publishing Frequency",
                "value": f"~{monthly_videos / max(1, len(monthly) or 1):.1f} videos/month",
                "detail": "Based on current year uploads",
            }
        )

        return {"monthlyData": monthly_data, "summaryCards": summary_cards}

    def top_videos_table(self) -> List[Dict]:
        top_videos = sorted(self.videos, key=lambda v: v.views, reverse=True)[:10]
        rows = []
        for idx, video in enumerate(top_videos, 1):
            engagement_rate = (
                (video.engagement / video.views) * 100 if video.views else 0
            )
            rows.append(
                {
                    "rank": idx,
                    "title": video.title,
                    "views": format_human_number(video.views),
                    "engagement": format_human_number(video.engagement),
                    "engagementRate": f"{engagement_rate:.2f}%",
                    "type": "Short" if video.content_type == "Shorts" else "Long",
                    "year": str(video.date_posted.year),
                    "duration": video.duration_display,
                }
            )
        return rows


def main():
    parser = argparse.ArgumentParser(description="Generate YouTube section JSON from DB.")
    parser.add_argument("--channel-id", default=DEFAULT_CHANNEL_ID)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Path to write the JSON payload.",
    )
    args = parser.parse_args()

    channel = fetch_channel(args.channel_id)
    videos = fetch_videos(args.channel_id)
    builder = YouTubeSectionBuilder(channel, videos)
    payload = builder.build()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

