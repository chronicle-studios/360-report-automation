SECTION_PROMPTS = {
    "metadata": """
You must return valid JSON with keys reportMetadata, platformStats, chapters (all three are required).
- reportMetadata: include date, title of channel, subtitle exactly as written. description must be a 1-line summary of what the report is.
- platformStats: array of { "platform": string, "followers": string } entries (limit 6). Use the best available follower/subscriber/member counts from the section text; if a platform hides counts (e.g. login wall), put a short human-readable note with the best proxy (e.g. "Not visible without login — see section") instead of "N/A" when the text explains why.
- chapters: **exactly 8** objects in narrative order, each { "id": string, "label": string, "emoji": string, "number": integer } with number 1..8. Use these ids in order: "overview", "youtube", "community", "sentiment", "creative", "proof", "reach", "data". Label "youtube" as **Instagram & Social** (or **Primary Social**) when the report is brand-first / Instagram-primary; other labels should match the report section names (Overview, Community, Sentiment, Creative Impact, Commercial, Geographic Reach, Data Notes).

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
  ],
  "chapters": [
    { "id": "overview", "label": "Overview", "emoji": "📊", "number": 1 },
    { "id": "youtube", "label": "Instagram & Social", "emoji": "📸", "number": 2 },
    { "id": "community", "label": "Community", "emoji": "🤝", "number": 3 },
    { "id": "sentiment", "label": "Sentiment", "emoji": "❤️", "number": 4 },
    { "id": "creative", "label": "Creative Impact", "emoji": "🎨", "number": 5 },
    { "id": "proof", "label": "Commercial", "emoji": "💵", "number": 6 },
    { "id": "reach", "label": "Geographic Reach", "emoji": "🌍", "number": 7 },
    { "id": "data", "label": "Data Notes", "emoji": "🔍", "number": 8 }
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
- platforms: include at most FOUR entries. Each entry must have name, icon, color, description, and stats. **Every platform must include at least one stat** (never an empty stats array). Prefer follower/subscriber/member counts when present; otherwise use numeric signals from the text only (review counts, aggregate ratings, number of named communities, etc.). Stat values should be compact (mostly digits, K/M suffixes, decimals like 4.08/5) — no long sentences.
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
Return JSON with introText, stats, notableHighlight, closingText.
- stats: array of { label, value, trend, confidence } (up to 6 entries).
- use 2 words max for the value
- notableHighlight: the single most impressive commercial proof point (distribution milestone, award, press feature, etc.). If the text mentions a **national distributor agreement** (e.g. RNDC / Republic National) or equivalent wholesale deal, prefer that over generic availability claims when supported.

Example:
{
  "introText": "Commercial summary sentence.",
  "stats": [
    { "label": "Retail Availability", "value": "30+ states", "trend": "expanding", "confidence": "estimated" }
  ],
  "notableHighlight": {
    "title": "Notable Achievement",
    "value": "Key metric or fact",
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
    "instagram_social": """
Extract Instagram and social media data from the research text. Return JSON with platformOverview, contentAnalysis, engagementMetrics, crossPlatformPresence, topContent, earnedMedia, keyInsights.

- platformOverview: primary platform (Instagram) profile data. Include handle, followers, following, postCount, bio, verified status. Set followersConfidence to "confirmed", "estimated", or "sparse".
- contentAnalysis: postCadence (e.g., "3-4 posts per week"), contentThemes (array of theme strings), formatMix (e.g., "60% Reels, 30% static, 10% carousel"), hashtagStrategy.
- engagementMetrics: avgLikesPerPost, avgCommentsPerPost, engagementRateEstimate — note sampleSize and sampleNote (e.g., "Based on 20 most recent public posts"). Set confidence.
- crossPlatformPresence: array of other platforms discovered (TikTok, Facebook, Twitter/X, YouTube, etc.) with handle, followers, confidence, description.
- topContent: array of up to 5 standout pieces of content across all platforms, ranked by engagement. Each has rank, platform, description, metric (e.g., "12.4K likes"), type (e.g., "Reel", "Post", "TikTok"), confidence.
- earnedMedia: summary of brand mentions by others, mentionCount with confidence, topMentions array of { source, description }.
- keyInsights: strengths (array), patterns (array), gaps (array).

Preserve confidence tags from the source material. If the research text marks something as Confirmed/Estimated/Sparse, carry that through.

Example:
{
  "platformOverview": {
    "platform": "Instagram",
    "handle": "@ghosttequila",
    "followers": "45.2K",
    "followersConfidence": "confirmed",
    "following": "1,200",
    "postCount": "350",
    "bio": "Ghost pepper infused tequila.",
    "verified": false
  },
  "contentAnalysis": {
    "postCadence": "3-4 posts per week",
    "contentThemes": ["Product shots", "Cocktail recipes", "Events"],
    "formatMix": "Mix of Reels and static posts",
    "hashtagStrategy": "#ghosttequila #spicymargarita"
  },
  "engagementMetrics": {
    "avgLikesPerPost": "850",
    "avgCommentsPerPost": "25",
    "engagementRateEstimate": "1.9%",
    "sampleSize": "20",
    "sampleNote": "Based on 20 most recent public posts",
    "confidence": "estimated"
  },
  "crossPlatformPresence": [
    { "name": "TikTok", "handle": "@ghosttequila", "followers": "12K", "confidence": "confirmed", "description": "Active with cocktail content" }
  ],
  "topContent": [
    { "rank": 1, "platform": "Instagram", "description": "Spicy margarita Reel", "metric": "12.4K likes", "type": "Reel", "confidence": "confirmed" }
  ],
  "earnedMedia": {
    "summary": "Featured in several cocktail blogs and YouTube reviews.",
    "mentionCount": "50+",
    "mentionCountConfidence": "estimated",
    "topMentions": [
      { "source": "VinePair", "description": "Included in best spicy tequilas list" }
    ]
  },
  "keyInsights": {
    "strengths": ["Strong visual brand identity"],
    "patterns": ["Cocktail content drives highest engagement"],
    "gaps": ["No TikTok presence"]
  }
}

Return JSON only.
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
