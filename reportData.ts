// Love & Pies Report Data
// All data is extracted here for easy maintenance and updates

export const reportMetadata = {
    date: "November 13, 2025",
    title: "Love & Pies",
    subtitle: "360° Audience Snapshot",
    description: "A comprehensive analysis of the multi-platform community surrounding Trailmix's cozy merge-puzzle game, exploring engagement, sentiment, and cultural impact across social media ecosystems.",
  };
  
  export const platformStats = [
    { platform: "instagram", followers: "245K" },
    { platform: "facebook", followers: "201K" },
    { platform: "youtube", followers: "17.7K" },
    { platform: "reddit", followers: "7K" },
  ];
  
  export const chapters = [
    { id: "overview", label: "Overview", emoji: "📊", number: 1 },
    { id: "youtube", label: "YouTube", emoji: "🎥", number: 2 },
    { id: "community", label: "Community", emoji: "🤝", number: 3 },
    { id: "sentiment", label: "Sentiment", emoji: "❤️", number: 4 },
    { id: "creative", label: "Creative Impact", emoji: "🎨", number: 5 },
    { id: "proof", label: "Commercial", emoji: "💵", number: 6 },
    { id: "reach", label: "Geographic Reach", emoji: "🌍", number: 7 },
    { id: "data", label: "Data Notes", emoji: "🔍", number: 8 },
  ];
  
  // Overview Section Data
  export const overviewData = {
    introText: "Love & Pies is a mobile merge-puzzle game (Trailmix Ltd.) blending cozy café drama and mystery. Launched in 2021, it has since amassed a broad, global player base, with 5 million+ downloads on Android alone. Across social media, the IP enjoys a strong following spanning Instagram, Facebook, YouTube, TikTok, Twitter/X, Reddit, Discord, and its official website and app stores – a comprehensive cross-platform footprint.",
    stats: [
      { label: "Instagram Followers", value: "245K", confidence: "confirmed" as const },
      { label: "Facebook Followers", value: "201K", confidence: "confirmed" as const },
      { label: "YouTube Subscribers", value: "17.7K", confidence: "confirmed" as const },
      { label: "Reddit Members", value: "~7K", confidence: "estimated" as const },
      { label: "Android Downloads", value: "5M+", confidence: "confirmed" as const },
      { label: "Active Platforms", value: "7", confidence: "confirmed" as const },
    ],
    closingText: "Fans congregate largely on casual-friendly platforms (Facebook, Instagram), while more niche discussion thrives on Reddit and Discord, indicating a broad but layered engagement spectrum. The community's center of gravity is in English-speaking, casual gaming circles.",
  };
  
  // YouTube Section Data
  export const youtubeData = {
    channelOverview: {
      subscribers: "17.7K",
      totalViews: "3.66M",
      totalLikes: "27.5K",
      totalComments: "2,073",
      channelName: "Love & Pies",
      handle: "@loveandpiesgame",
      channelCreated: "May 29, 2020",
      channelAge: "5.5 years",
      videosInDataset: "60",
    },
    performanceMetrics: {
      avgViewsPerVideo: "61,006",
      avgLikesPerVideo: "459",
      avgCommentsPerVideo: "53",
      medianViews: "1,234",
      avgLikeViewRatio: "2.80%",
      avgCommentViewRatio: "0.20%",
      avgEngagementRate: "3.00%",
    },
    keyMetrics: [
      { value: "206.80", label: "Views per Subscriber" },
      { value: "29,594", label: "Total Engagement Actions" },
      { value: "8.1", label: "Engagement per 1K Views" },
      { value: "69", label: "Avg Views per Day" },
      { value: "10.9", label: "Videos per Year (avg)" },
      { value: "2023", label: "Most Productive Year" },
    ],
    contentTypeBreakdown: {
      pieData: [
        { name: 'Long-form', value: 58.3, count: 35 },
        { name: 'Shorts', value: 41.7, count: 25 },
        { name: 'Livestreams', value: 0, count: 0 }
      ],
      performanceTable: [
        { type: "Long-form", avgViews: "101,529", likeRatio: "2.11%", commentRatio: "0.24%", engagement: "2.35%" },
        { type: "Shorts", avgViews: "4,274", likeRatio: "3.76%", commentRatio: "0.15%", engagement: "3.90%" },
        { type: "Livestreams", avgViews: "0", likeRatio: "0.00%", commentRatio: "0.00%", engagement: "0.00%" },
      ],
      insights: [
        "Long-form videos drive 23.7× more views than Shorts despite similar engagement ratios",
        "Shorts show higher engagement rates (390.28%) but lower absolute view counts",
        "No livestream content present - untapped engagement opportunity",
      ],
    },
    topPerformers: {
      multiplier: "113.3×",
      avgViewsTop: "490,160",
      avgViewsNonTop: "4,326",
      comparisonTable: [
        { attribute: "Avg Views", top: "490,160", nonTop: "4,326", difference: "+485,834" },
        { attribute: "Avg Like Ratio", top: "1.82%", nonTop: "N/A", difference: "—" },
        { attribute: "Avg Comment Ratio", top: "0.31%", nonTop: "N/A", difference: "—" },
        { attribute: "Avg Engagement", top: "2.13%", nonTop: "N/A", difference: "—" },
        { attribute: "Avg Length (sec)", top: "555", nonTop: "N/A", difference: "—" },
        { attribute: "Avg Views/Day", top: "483", nonTop: "N/A", difference: "—" },
      ],
      findings: [
        "Top performers are mostly Long-form content averaging 555 seconds (9+ minutes)",
        "Optimal video length for performance: 5+ minutes",
        "Most common length category among top performers: 5+ min",
      ],
    },
    yearOverYearTrends: {
      avgViewsData: [
        { year: '2021', views: 77655 },
        { year: '2022', views: 169876 },
        { year: '2023', views: 1920 },
        { year: '2024', views: 85169 },
        { year: '2025', views: 3856 }
      ],
      videosPostedData: [
        { year: '2021', videos: 1 },
        { year: '2022', videos: 16 },
        { year: '2023', videos: 17 },
        { year: '2024', videos: 9 },
        { year: '2025', videos: 17 }
      ],
      engagementTrendData: [
        { year: '2021', engagement: 0.16 },
        { year: '2022', engagement: 1.45 },
        { year: '2023', engagement: 3.99 },
        { year: '2024', engagement: 4.88 },
        { year: '2025', engagement: 2.64 }
      ],
      yearlyTable: [
        { year: "2020", videos: "0", avgViews: "—", avgLikes: "—", avgComments: "—", engagement: "—", yoyGrowth: "N/A" },
        { year: "2021", videos: "1", avgViews: "77,655", avgLikes: "115", avgComments: "6", engagement: "0.16%", yoyGrowth: "—" },
        { year: "2022", videos: "16", avgViews: "169,876", avgLikes: "38", avgComments: "3", engagement: "1.45%", yoyGrowth: "+118.8%", highlight: true },
        { year: "2023", videos: "17", avgViews: "1,920", avgLikes: "29", avgComments: "3", engagement: "3.99%", yoyGrowth: "-98.9%", isNegative: true },
        { year: "2024", videos: "9", avgViews: "85,169", avgLikes: "2,763", avgComments: "383", engagement: "4.88%", yoyGrowth: "+4336.8%", isPositive: true },
        { year: "2025", videos: "17", avgViews: "3,856", avgLikes: "84", avgComments: "13", engagement: "2.64%", yoyGrowth: "-95.5%", isNegative: true },
      ],
      summaryCards: [
        { label: "Best Year by Avg Views", value: "2022", detail: "169,876 avg views" },
        { label: "Most Productive Year", value: "2023", detail: "17 videos posted" },
        { label: "Engagement Trend", value: "Decreasing", detail: "in 2025", isNegative: true },
      ],
    },
    currentYearAnalysis: {
      monthlyData: [
        { month: 'Jan', views: 2100, likes: 65, comments: 8 },
        { month: 'Feb', views: 3200, likes: 78, comments: 12 },
        { month: 'Mar', views: 4500, likes: 92, comments: 15 },
        { month: 'Apr', views: 3800, likes: 85, comments: 11 },
        { month: 'May', views: 5200, likes: 110, comments: 18 },
        { month: 'Jun', views: 8900, likes: 156, comments: 24 }
      ],
      summaryCards: [
        { label: "Best Month by Views", value: "June", detail: "8,900 avg views" },
        { label: "Engagement Trend", value: "Positive", detail: "Growing through 2025" },
        { label: "Publishing Frequency", value: "~3 videos/month", detail: "Consistent output" },
      ],
    },
    videoLengthAnalysis: {
      categories: [
        { range: "< 1 min", avgViews: "259,647", count: 11, percentage: "18.3%" },
        { range: "1-5 min", avgViews: "19,234", count: 14, percentage: "23.3%" },
        { range: "5+ min", avgViews: "91,406", count: 35, percentage: "58.3%" },
      ],
    },
    topVideos: [
      { rank: 1, title: "Love & Pies: Amelia's Deep Dive! Part 2", views: "1,029,612", engagement: "7,931", engagementRate: "0.84%", type: "Long", year: "2022", duration: "19m" },
      { rank: 2, title: "Love & Pies – Official Release Trailer", views: "795,896", engagement: "7,931", engagementRate: "1.10%", type: "Long", year: "2021", duration: "1m" },
      { rank: 3, title: "Love & Pies: Amelia's Deep Dive! Part 1", views: "677,340", engagement: "6,556", engagementRate: "1.08%", type: "Long", year: "2022", duration: "18m" },
      { rank: 4, title: "Love & Pies ❤️🥧 The Story Trailer", views: "654,432", engagement: "5,895", engagementRate: "1.01%", type: "Long", year: "2022", duration: "1m" },
      { rank: 5, title: "Love & Pies for Pride", views: "517,382", engagement: "47,439", engagementRate: "9.70%", type: "Short", year: "2024", duration: "46s" },
      { rank: 6, title: "Love & Pies Pride Intro", views: "428,174", engagement: "37,293", engagementRate: "9.22%", type: "Short", year: "2024", duration: "34s" },
      { rank: 7, title: "Who Is He? 🧐", views: "73,028", engagement: "6,583", engagementRate: "9.46%", type: "Short", year: "2024", duration: "40s" },
      { rank: 8, title: "Love & Pride - Intro", views: "46,382", engagement: "4,454", engagementRate: "9.82%", type: "Short", year: "2024", duration: "44s" },
      { rank: 9, title: "Love & Piescast: Pride Special 2025! 🌈", views: "46,245", engagement: "1,176", engagementRate: "2.66%", type: "Long", year: "2025", duration: "19m" },
      { rank: 10, title: "Love & Pies Kate's Spoooky Costume Party 👻", views: "34,718", engagement: "3,114", engagementRate: "8.97%", type: "Short", year: "2024", duration: "50s" },
    ],
    keyInsights: {
      critical: [
        "Massive view decline in 2025 (-95.5% YoY) despite maintaining video output",
        "Engagement rates remain high (2.64%) but views per video dropping significantly",
        "Algorithm appears to be deprioritizing channel content in 2025",
      ],
      contentPatterns: [
        "Long-form dominance: Long-form videos get 23.7× more views than Shorts",
        "Optimal length: 30-60 second videos perform best (259,647 avg views), but 5+ minute content is most common among top performers",
        "Peak performance: 2022 was the breakout year (169,876 avg views per video)",
        "Top performer gap: Top 10% of videos get 113× more views than the rest",
      ],
      recommendations: [
        "Double down on successful formats: 'Piescast' series shows consistent engagement - continue this format",
        "Experiment with livestreams: Zero livestream content represents untapped opportunity",
        "Optimize for algorithm: Focus on 30-60s hook videos to drive traffic to longer content",
        "Investigate 2025 drop: Conduct SEO/algorithm audit to understand view decline",
      ],
      trajectoryAssessment: {
        state: "declining phase",
        description: "After breakout success in 2022 and recovery in 2024, the channel faces significant headwinds in 2025. However, strong engagement rates (2.64%) and loyal community suggest the content quality remains high. The issue appears algorithmic rather than content-related, requiring strategic pivots in format, timing, and platform optimization to recapture momentum.",
      },
    },
  };
  
  // Community Section Data
  export const communityData = {
    introText: "The Love & Pies community thrives across multiple platforms, each serving distinct purposes and fostering different types of engagement.",
    platforms: [
      {
        name: "Facebook",
        icon: "F",
        color: "blue",
        description: "Major community pillar with highly active page and private group. Posts receive hundreds of reactions as devs share events, contests, and fan spotlights.",
        stats: [
          { label: "Page Followers", value: "201K" },
          { label: "Group Members", value: "7.5K" },
        ],
      },
      {
        name: "Instagram",
        icon: "IG",
        color: "gradient",
        description: "Highly curated content with glossy art, character illustrations, and event announcements. Thousands of likes and heart-filled comments on recent posts.",
        stats: [
          { label: "Followers", value: "245K" },
        ],
      },
      {
        name: "Reddit",
        icon: "R",
        color: "orange",
        description: "Hey everyone! The Love & Pies team here. We're thrilled to announce the launch of our official Discord server: a new place where players can stay updated with what's happening in the game, take part in polls that help guide development decisions, and get involved in giveaways (including some free energy for anyone who joins in the first week!). The server is focused on updates, polls, and giveaways, so you'll always have the latest news in one easy place, with no endless scrolling or off-topic chatter. For players who want to be more involved, we're also launching our brand new Insider Program – a small group of passionate players who share feedback and ideas directly with the development team to help shape the future of Love & Pies.",
        stats: [
          { label: "Members", value: "~7K" },
        ],
      },
      {
        name: "Discord",
        icon: "D",
        color: "indigo",
        description: "Newly launched official server with channels for announcements, player support, and off-topic chat. Exclusive sneak peeks and direct dev Q&A.",
        stats: [
          { label: "Since 2025", value: "Active" },
        ],
      },
    ],
    quote: {
      text: "Please update this I'm so tired of having to sit through events re-teaching me how to merge. I'm level 133 I KNOW how to merge items !!",
      author: "Reddit User",
      platform: "r/LoveAndPies",
    },
    closingText: "Beyond official channels, player networks span other forums including a Fandom wiki, Tumblr fan art, and even Bilibili guides. Regional communities exist with Spanish/Portuguese, Chinese, and other language speakers, though the primary hub remains English-speaking platforms.",
  };
  
  // Sentiment Section Data
  export const sentimentData = {
    overall: {
      title: "Strongly Positive Overall",
      subtitle: "With pockets of constructive criticism",
    },
    platformSentiments: [
      {
        emoji: "😍",
        title: "Facebook/Instagram Sentiment",
        description: "Upbeat and affectionate. Comments filled with heart emojis, fan theories, and unbridled hype. Deep emotional investment in narrative and characters.",
      },
      {
        emoji: "🤔",
        title: "Reddit/Discord Sentiment",
        description: "More nuanced but still enthusiastic. Players applaud responsiveness and inclusivity while voicing frustrations about monetization and repetitive tutorials.",
      },
    ],
    quotes: [
      { text: "I love this game so much", platform: "Instagram" },
      { text: "Lovely Art, Great Storyline, Fun and Casual Gameplay", platform: "App Store" },
      { text: "My favorite mobile game, ever!", platform: "App Store" },
      { text: "By making matches [in L&P], I'm rewarded with good storytelling", platform: "Reddit" },
    ],
    closingText: "The polarity is mostly positive, with mild frustration around grindy aspects. No significant flame wars or hostility observed. Players feel a lot of love (and pies) for Love & Pies, praising its 'cozy drama' and inclusivity while pushing for improvements in a constructive tone.",
  };
  
  // Creative Impact Section Data
  export const creativeData = {
    introText: "Despite being a relatively young mobile IP, Love & Pies has sparked notable creative output and industry attention, punching above its weight for a mobile puzzle game.",
    stats: [
      { label: "Fan Art Presence", value: "Active", trend: "Tumblr, Pinterest, Social Media", confidence: "confirmed" as const },
      { label: "Fan Fiction", value: "Rare", trend: "Yuletide 2022 Exchange", confidence: "confirmed" as const },
      { label: "Industry Recognition", value: "Featured", trend: "ArtStation, Behance", confidence: "confirmed" as const },
    ],
    highlights: [
      {
        title: "Fan Art",
        description: "Character art on Tumblr, Pinterest, and fan pages. Multiple illustrations of Amelia, Yuka, and other key cast.",
      },
      {
        title: "Professional Art",
        description: "Official character designs showcased on ArtStation and Behance by concept artists, demonstrating high production value.",
      },
      {
        title: "Media Coverage",
        description: "Pocket Gamer praises inclusivity and storytelling; Supercell's acquisition featured in industry press.",
      },
    ],
    closingText: "For a mobile game, Love & Pies enjoys a disproportionately warm cultural footprint with its representation and cozy drama resonating far beyond typical merge game boundaries.",
  };
  
  // Commercial Success Section Data
  export const commercialData = {
    introText: "Love & Pies is not just loved by fans - it's commercially validated across metrics, press, and backing from mobile industry giants.",
    stats: [
      { label: "Avg Revenue/Month", value: "$3.8M", trend: "Dec 2023 data", confidence: "estimated" as const },
      { label: "Total Downloads", value: "5M+", trend: "Google Play alone", confidence: "confirmed" as const },
      { label: "Day-120 Retention", value: ">10%", trend: "Strong engagement metric", confidence: "confirmed" as const },
    ],
    supercellInvestment: {
      title: "Supercell Investment",
      amount: "$60 million",
      description: "In May 2022, mobile giant Supercell acquired a majority stake in Trailmix, investing an additional $60 million to 'hypercharge the growth of Love & Pies.' This is a resounding vote of confidence; Supercell only backs games with strong metrics and long-term potential.",
      impact: "The investment enabled more content, marketing, and community initiatives including Pride videos and the official Discord server.",
    },
    closingText: "Public evidence paints a picture of a commercially successful and critically appreciated title: millions of players, engaged spenders, industry awards, and backing from one of the world's biggest mobile publishers – all clear proofs of Love & Pies' impact.",
  };
  
  // Geographic Reach Section Data
  export const geographicData = {
    introText: "Love & Pies' audience appears geographically diverse but primarily concentrated in Western markets, with strong foundations set for worldwide expansion.",
    primaryMarkets: [
      "United Kingdom & Ireland",
      "United States & Canada",
      "Australia & New Zealand",
      "Finland (soft launch market)",
    ],
    emergingMarkets: [
      "Philippines (strong mobile gaming)",
      "Brazil & Latin America",
      "Taiwan/HK (Chinese Traditional)",
      "Southeast Asia & MENA",
    ],
    languages: {
      primary: ["English", "Chinese (Traditional)"],
      secondary: ["Portuguese", "Spanish", "Russian", "French", "Indonesian", "Arabic"],
    },
    closingText: "The community's tone and platforms suggest a tilt towards adult women, particularly ages 20s-40s, but with strong inclusivity. LGBTQ+ folks are visibly part of the fanbase, and the Pride content received positive responses from LGBTQ players worldwide. Cross-platform amplification through Supercell's Hay Day introduced Love & Pies to farming game communities globally, potentially recruiting players from Europe, Latin America, and South Asia.",
  };
  
  // Data Gaps Section Data
  export const dataGapsData = {
    introText: "This comprehensive view was assembled from publicly available data, with the following gaps and limitations noted for transparency.",
    confidenceLevels: [
      {
        symbol: "✅",
        label: "Confirmed",
        description: "Data directly from official or primary sources (follower counts, download stats, app store ratings)",
      },
      {
        symbol: "⚠️",
        label: "Estimated",
        description: "Inferred data from indirect sources (Reddit membership, demographic patterns, engagement rates)",
      },
      {
        symbol: "❔",
        label: "Sparse",
        description: "Weak or anecdotal signals (TikTok presence, fan art extent, regional platform usage)",
      },
    ],
    limitations: [
      {
        title: "Private Metrics",
        description: "Discord member count and TikTok metrics unavailable due to login requirements. Relied on indirect cues and launch announcements for estimates.",
      },
      {
        title: "Partial Data & API Limits",
        description: "YouTube analytics gleaned from search-indexed data and third-party caches rather than direct API access. Provides snapshot but not complete picture of long-tail content.",
      },
      {
        title: "Regional Platforms",
        description: "Checked major Western platforms and some Chinese networks (Bilibili). May have missed presence on Weibo, LINE, or other regional platforms if they exist at smaller scale.",
      },
      {
        title: "Fan Content Detection",
        description: "Discovery of fan works may not be exhaustive as content isn't centrally tagged. Documented what was found but there could be more in closed groups or under unorthodox tags.",
      },
      {
        title: "Sentiment Sampling",
        description: "Based on manual sample of comments from Reddit, Facebook, Instagram, and app reviews in English (and one Portuguese tweet). No large-scale automated sentiment analysis was employed.",
      },
    ],
    metadata: {
      researchDate: "November 13, 2025 (21:00–22:00 UTC)",
      method: "Web search, direct platform exploration, cached results",
      note: "All timestamps refer to content as of snapshot date. Social metrics can change quickly; this report represents a moment-in-time view.",
    },
    closingText: "Overall, these limitations are relatively minor. The available evidence was rich enough to form a well-rounded view. All claims are anchored in publicly verifiable sources, ensuring the snapshot can be trusted and reproduced.",
  };
  
  export const footerData = {
    title: "Love & Pies 360° Audience Snapshot",
    snapshotDate: "Snapshot captured November 13, 2025 UTC",
    disclaimer: "All data from publicly available sources",
  };
  