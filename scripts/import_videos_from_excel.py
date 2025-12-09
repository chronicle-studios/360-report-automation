#!/usr/bin/env python3
"""
Load YouTube video metadata from an Excel export into the videos table.
"""

from __future__ import annotations

import argparse
import math
from datetime import datetime
from pathlib import Path

import pandas as pd

from db import db_manager


def parse_int(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return None


def parse_datetime(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    try:
        return pd.to_datetime(value, utc=True).to_pydatetime()
    except Exception:
        return None


def format_duration(seconds):
    if seconds is None:
        return None
    try:
        seconds = int(float(seconds))
    except (TypeError, ValueError):
        return None
    minutes, secs = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:d}:{secs:02d}"


def derive_post_type(row):
    post_type = row.get("post_type")
    if isinstance(post_type, str) and post_type.strip():
        label = post_type.strip().upper()
        if label in {"VIDEO", "SHORT"}:
            return label
    length = parse_int(row.get("video_length"))
    if length is not None and length < 60:
        return "SHORT"
    return "VIDEO"


INSERT_SQL = """
    INSERT INTO videos (
        video_id,
        title,
        url,
        video_length,
        duration_string,
        date_posted,
        views,
        likes,
        num_comments,
        description,
        channel_id,
        collected_at,
        source,
        post_type
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (video_id) DO UPDATE SET
        title = EXCLUDED.title,
        url = EXCLUDED.url,
        video_length = EXCLUDED.video_length,
        duration_string = EXCLUDED.duration_string,
        date_posted = EXCLUDED.date_posted,
        views = EXCLUDED.views,
        likes = EXCLUDED.likes,
        num_comments = EXCLUDED.num_comments,
        description = EXCLUDED.description,
        channel_id = EXCLUDED.channel_id,
        collected_at = EXCLUDED.collected_at,
        source = EXCLUDED.source,
        post_type = EXCLUDED.post_type;
"""


def import_excel(path: Path) -> int:
    df = pd.read_excel(path, sheet_name=0)
    df = df.fillna(value=pd.NA)

    inserted = 0
    with db_manager.get_connection() as conn:
        cur = conn.cursor()
        for _, row in df.iterrows():
            video_id = row.get("video_id")
            if not isinstance(video_id, str) or not video_id.strip():
                continue

            payload = (
                video_id.strip(),
                (row.get("title") or "").strip(),
                (row.get("url") or "").strip(),
                parse_int(row.get("video_length")),
                format_duration(row.get("video_length")),
                parse_datetime(row.get("date_posted")),
                parse_int(row.get("views")),
                parse_int(row.get("likes")),
                parse_int(row.get("num_comments")),
                row.get("description") if isinstance(row.get("description"), str) else None,
                (row.get("youtuber_id") or "").strip() or None,
        parse_datetime(row.get("timestamp")),
        "CHANNEL",
                derive_post_type(row),
            )
            cur.execute(INSERT_SQL, payload)
            inserted += 1
    return inserted


def main():
    parser = argparse.ArgumentParser(description="Import videos from Excel into the database.")
    parser.add_argument(
        "--file",
        type=Path,
        default=Path("VideosData.xlsx"),
        help="Path to the Excel workbook (default: VideosData.xlsx).",
    )
    args = parser.parse_args()

    if not args.file.exists():
        raise SystemExit(f"File not found: {args.file}")

    count = import_excel(args.file)
    print(f"Processed {count} rows from {args.file}")


if __name__ == "__main__":
    main()

