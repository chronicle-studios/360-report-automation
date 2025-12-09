SECTION_PROMPTS = {
    "metadata": """
You must return valid JSON with keys reportMetadata, platformStats.
- reportMetadata: include date, title of channel, subtitle exactly as written. description must be a 1-line summary of what the report is.
- platformStats: array of { "platform": string, "followers": string } entries (limit 6).

Example structure (use it as a template, do NOT reuse the literal values):
{
  "reportMetadata": {
    "date": "November 13, 2025",
    "title": "Love & Pies",
    "subtitle": "360° Audience Snapshot",
    "description": "One-line summary."
  },
  "platformStats": [
    { "platform": "instagram", "followers": "245K" },
    { "platform": "facebook", "followers": "201K" }
  ]
}
""".strip(),
    "overview": """
Return JSON with introText, stats, closingText.
- introText / closingText: summarize the paragraph content into 1–2 concise sentences that capture the key message (do NOT copy the heading verbatim; closingText must read like a concluding summary).
- stats: array where each entry includes label, value, confidence (“confirmed”, “estimated”). Include up to 6 entries focusing on the most important platform metrics.
- The platform metrics must be numbers only. 
Example:
{
  "introText": "Love & Pies summary sentence.",
  "stats": [
    { "label": "Instagram Followers", "value": "245K", "confidence": "confirmed" },
    { "label": "Facebook Followers", "value": "201K", "confidence": "confirmed" }
  ],
  "closingText": "Concise concluding sentence."
}
""".strip(),
    "youtube": """
Produce JSON containing ONLY channelOverview, performanceMetrics, currentYearAnalysis, and topVideos.
- channelOverview: include subscribers, totalViews, totalLikes, totalComments, channelName, handle, channelCreated, channelAge, videosInDataset.
- performanceMetrics: avgViewsPerVideo, avgLikesPerVideo, avgCommentsPerVideo, medianViews, avgLikeViewRatio, avgCommentViewRatio, avgEngagementRate.
- currentYearAnalysis: monthlyData (array of { month, views, likes, comments }) and summaryCards (array of { label, value, detail }).
- topVideos: array of 10 entries with rank, title, views, engagement, engagementRate, type, year, duration.
- Preserve numeric formatting (e.g., "3.66M", "8,900").

Example:
{
  "channelOverview": { ... },
  "performanceMetrics": { ... },
  "currentYearAnalysis": {
    "monthlyData": [
      { "month": "Jan", "views": 2100, "likes": 65, "comments": 8 },
      { "month": "Feb", "views": 3200, "likes": 78, "comments": 12 }
    ],
    "summaryCards": [
      { "label": "Best Month by Views", "value": "June", "detail": "8,900 avg views" },
      { "label": "Publishing Frequency", "value": "~3 videos/month", "detail": "Consistent output" }
    ]
  },
  "topVideos": [
    { "rank": 1, "title": "Love & Pies: Amelia's Deep Dive! Part 2", "views": "1,029,612", "engagement": "7,931", "engagementRate": "0.84%", "type": "Long", "year": "2022", "duration": "19m" }
  ]
}
""".strip(),
    "community": """
Emit JSON with introText, platforms, quote, closingText.
- introText must summarize the section (do not reuse the heading).
- platforms: include at most FOUR entries. Each entry must have name, icon, color, description, and stats (stats array should contain only key/value metrics such as follower counts or membership numbers. Please only include numbers and not words, not narrative prose).
- quote must contain text, author, platform.

Example:
{
  "introText": "Community summary sentence.",
  "platforms": [
    {
      "name": "Facebook",
      "icon": "F",
      "color": "blue",
      "description": "Major community pillar...",
      "stats": [
        { "label": "Followers", "value": "201K" },
        { "label": "Group Members", "value": "7.5K" }
      ]
    }
  ],
  "quote": { "text": "Quote here", "author": "Reddit user", "platform": "Reddit" },
  "closingText": "Closing summary sentence."
}
""".strip(),
    "sentiment": """
Return JSON containing overall, platformSentiments, quotes, closingText.
- overall: { title, subtitle }.
- platformSentiments: array of { emoji, title, description }.
- quotes: array of { text, platform }, return 5-6 most striking quotes.

Example:
{
  "overall": { "title": "Strongly Positive", "subtitle": "With constructive feedback pockets" },
  "platformSentiments": [
    { "emoji": "❤️", "title": "Facebook/Instagram", "description": "Cheerful, affectionate comments." }
  ],
  "quotes": [
    { "text": "I love this game so much!", "platform": "Instagram" }
  ],
  "closingText": "Concluding sentiment summary."
}
""".strip(),
    "creative": """
Output JSON with introText, stats, highlights, closingText.
- introText: 1–2 sentence summary (no headings).
- stats: include only the key metrics mentioned (label, value, trend, confidence). Keep them concise; include up to 6 entries (or fewer if content is unavailable).
- highlights: limit to 5 entries (title, description) focusing on major themes (e.g., Fan Art, Professional Art, Media Coverage). Titles should be short (1–2 words) and descriptions 1–2 sentences.
- closingText: short concluding summary (1–2 sentences).

Example format (illustrative – don’t copy values verbatim):
{
  "introText": "Despite being a young mobile IP, Love & Pies drives meaningful creative output.",
  "stats": [
    { "label": "Fan Art Presence", "value": "Active", "trend": "Tumblr, Pinterest", "confidence": "confirmed" },
    { "label": "Fan Fiction", "value": "Rare", "trend": "Yuletide 2022", "confidence": "confirmed" },
    { "label": "Industry Recognition", "value": "Featured", "trend": "ArtStation, Behance", "confidence": "confirmed" }
  ],
  "highlights": [
    { "title": "Fan Art", "description": "Character art shared across Tumblr and Pinterest." },
    { "title": "Professional Art", "description": "Official designs showcased on ArtStation and Behance." },
    { "title": "Media Coverage", "description": "Pocket Gamer praised inclusivity and storytelling." }
  ],
  "closingText": "The IP punches above its weight culturally, with fan art, professional showcases, and media attention."
}

Return JSON only.
""".strip(),
    "commercial": """
Return JSON with introText, stats, closingText.
- stats: array of { label, value, trend, confidence } (up to 6 entries).
- use 2 words max for the value

Example:
{
  "introText": "Commercial summary sentence.",
  "stats": [
    { "label": "Google Play rating", "value": "4.4★", "trend": "stable", "confidence": "confirmed" }
  ],
  "supercellInvestment": {
    "title": "Supercell Investment",
    "amount": "$60 million",
    "description": "Summary line.",
    "impact": "Impact line."
  },
  "closingText": "Concluding sentence."
}
""".strip(),
    "geographic": """
Produce JSON with introText, primaryMarkets, emergingMarkets, languages, closingText.
- introText / closingText: concise summaries (1–2 sentences).
- primaryMarkets / emergingMarkets: arrays of strings (include descriptors like "(soft launch market)"). Provide an equal count for both arrays.
- languages: object with primary [] and secondary [] arrays.

Example:
{
  "introText": "Geographic summary sentence.",
  "primaryMarkets": ["United Kingdom (soft launch market)", "United States"],
  "emergingMarkets": ["Philippines", "Brazil"],
  "languages": {
    "primary": ["English"],
    "secondary": ["Portuguese", "Spanish"]
  },
  "closingText": "Closing summary sentence."
}
""".strip(),
    "data_gaps": """
Return JSON with introText, confidenceLevels, limitations, metadata, closingText.
- confidenceLevels: array of { symbol, label, description }.
- limitations: array of { title, description }.
- metadata: { researchDate, method, note }.

Example:
{
  "introText": "Data gap intro sentence.",
  "confidenceLevels": [
    { "symbol": "✅", "label": "Confirmed", "description": "..." }
  ],
  "limitations": [
    { "title": "Private Metrics", "description": "..." }
  ],
  "metadata": {
    "researchDate": "2025-11-13 (UTC)",
    "method": "Summary of approach",
    "note": "Context note."
  },
  "closingText": "Closing sentence."
}
""".strip(),
}
