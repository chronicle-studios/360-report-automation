from typing import Any, Dict

SECTION_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "metadata": {
        "type": "object",
        "properties": {
            "reportMetadata": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"},
                    "title": {"type": "string"},
                    "subtitle": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["date", "title", "subtitle", "description"],
            },
            "platformStats": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "platform": {"type": "string"},
                        "followers": {"type": "string"},
                    },
                    "required": ["platform", "followers"],
                },
            },
            "chapters": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "label": {"type": "string"},
                        "emoji": {"type": "string"},
                        "number": {"type": "integer"},
                    },
                    "required": ["id", "label", "emoji", "number"],
                },
            },
        },
        "required": ["reportMetadata", "platformStats", "chapters"],
    },
    "overview": {
        "type": "object",
        "properties": {
            "introText": {"type": "string"},
            "stats": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "label": {"type": "string"},
                        "value": {"type": "string"},
                        "confidence": {"type": "string"},
                    },
                    "required": ["label", "value", "confidence"],
                },
            },
            "closingText": {"type": "string"},
        },
        "required": ["introText", "stats", "closingText"],
    },
    "youtube": {
        "type": "object",
        "properties": {
            "channelOverview": {
                "type": "object",
                "properties": {
                    "subscribers": {"type": "string"},
                    "totalViews": {"type": "string"},
                    "totalLikes": {"type": "string"},
                    "totalComments": {"type": "string"},
                    "channelName": {"type": "string"},
                    "handle": {"type": "string"},
                    "channelCreated": {"type": "string"},
                    "channelAge": {"type": "string"},
                    "videosInDataset": {"type": "string"},
                },
                "required": [
                    "subscribers",
                    "totalViews",
                    "totalLikes",
                    "totalComments",
                    "channelName",
                    "handle",
                    "channelCreated",
                    "channelAge",
                    "videosInDataset",
                ],
            },
            "performanceMetrics": {
                "type": "object",
                "properties": {
                    "avgViewsPerVideo": {"type": "string"},
                    "avgLikesPerVideo": {"type": "string"},
                    "avgCommentsPerVideo": {"type": "string"},
                    "medianViews": {"type": "string"},
                    "avgLikeViewRatio": {"type": "string"},
                    "avgCommentViewRatio": {"type": "string"},
                    "avgEngagementRate": {"type": "string"},
                },
                "required": [
                    "avgViewsPerVideo",
                    "avgLikesPerVideo",
                    "avgCommentsPerVideo",
                    "medianViews",
                    "avgLikeViewRatio",
                    "avgCommentViewRatio",
                    "avgEngagementRate",
                ],
            },
            "currentYearAnalysis": {
                "type": "object",
                "properties": {
                    "monthlyData": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "month": {"type": "string"},
                                "views": {"type": "number"},
                                "likes": {"type": "number"},
                                "comments": {"type": "number"},
                            },
                            "required": ["month", "views", "likes", "comments"],
                        },
                    },
                    "summaryCards": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "label": {"type": "string"},
                                "value": {"type": "string"},
                                "detail": {"type": "string"},
                            },
                            "required": ["label", "value", "detail"],
                        },
                    },
                },
                "required": ["monthlyData", "summaryCards"],
            },
            "videoLengthAnalysis": {
                "type": "object",
                "properties": {
                    "categories": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "range": {"type": "string"},
                                "avgViews": {"type": "string"},
                                "count": {"type": "integer"},
                                "percentage": {"type": "string"},
                            },
                            "required": ["range", "avgViews", "count", "percentage"],
                        },
                    }
                },
                "required": ["categories"],
            },
            "topVideos": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "rank": {"type": "integer"},
                        "title": {"type": "string"},
                        "views": {"type": "string"},
                        "engagement": {"type": "string"},
                        "engagementRate": {"type": "string"},
                        "type": {"type": "string"},
                        "year": {"type": "string"},
                        "duration": {"type": "string"},
                    },
                    "required": [
                        "rank",
                        "title",
                        "views",
                        "engagement",
                        "engagementRate",
                        "type",
                        "year",
                        "duration",
                    ],
                },
            },
            "keyInsights": {
                "type": "object",
                "properties": {
                    "critical": {"type": "array", "items": {"type": "string"}},
                    "contentPatterns": {"type": "array", "items": {"type": "string"}},
                    "recommendations": {"type": "array", "items": {"type": "string"}},
                    "trajectoryAssessment": {
                        "type": "object",
                        "properties": {
                            "state": {"type": "string"},
                            "description": {"type": "string"},
                        },
                        "required": ["state", "description"],
                    },
                },
                "required": [
                    "critical",
                    "contentPatterns",
                    "recommendations",
                    "trajectoryAssessment",
                ],
            },
        },
        "required": [
            "channelOverview",
            "performanceMetrics",
            "keyMetrics",
            "contentTypeBreakdown",
            "topPerformers",
            "yearOverYearTrends",
            "currentYearAnalysis",
            "videoLengthAnalysis",
            "topVideos",
            "keyInsights",
        ],
    },
    "community": {
        "type": "object",
        "properties": {
            "introText": {"type": "string"},
            "platforms": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "icon": {"type": "string"},
                        "color": {"type": "string"},
                        "description": {"type": "string"},
                        "stats": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "label": {"type": "string"},
                                    "value": {"type": "string"},
                                },
                                "required": ["label", "value"],
                            },
                        },
                    },
                    "required": ["name", "icon", "color", "description", "stats"],
                },
            },
            "quote": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "author": {"type": "string"},
                    "platform": {"type": "string"},
                },
                "required": ["text", "author", "platform"],
            },
            "closingText": {"type": "string"},
        },
        "required": ["introText", "platforms", "quote", "closingText"],
    },
    "sentiment": {
        "type": "object",
        "properties": {
            "overall": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "subtitle": {"type": "string"},
                },
                "required": ["title", "subtitle"],
            },
            "platformSentiments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "emoji": {"type": "string"},
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                    },
                    "required": ["emoji", "title", "description"],
                },
            },
            "quotes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "platform": {"type": "string"},
                    },
                    "required": ["text", "platform"],
                },
            },
            "closingText": {"type": "string"},
        },
        "required": ["overall", "platformSentiments", "quotes", "closingText"],
    },
    "creative": {
        "type": "object",
        "properties": {
            "introText": {"type": "string"},
            "stats": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "label": {"type": "string"},
                        "value": {"type": "string"},
                        "trend": {"type": "string"},
                        "confidence": {"type": "string"},
                    },
                    "required": ["label", "value", "trend", "confidence"],
                },
            },
            "highlights": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                    },
                    "required": ["title", "description"],
                },
            },
            "closingText": {"type": "string"},
        },
        "required": ["introText", "stats", "highlights", "closingText"],
    },
    "commercial": {
        "type": "object",
        "properties": {
            "introText": {"type": "string"},
            "stats": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "label": {"type": "string"},
                        "value": {"type": "string"},
                        "trend": {"type": "string"},
                        "confidence": {"type": "string"},
                    },
                    "required": ["label", "value", "trend", "confidence"],
                },
            },
            "supercellInvestment": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "amount": {"type": "string"},
                    "description": {"type": "string"},
                    "impact": {"type": "string"},
                },
                "required": ["title", "amount", "description", "impact"],
            },
            "closingText": {"type": "string"},
        },
        "required": ["introText", "stats", "supercellInvestment", "closingText"],
    },
    "geographic": {
        "type": "object",
        "properties": {
            "introText": {"type": "string"},
            "primaryMarkets": {"type": "array", "items": {"type": "string"}},
            "emergingMarkets": {"type": "array", "items": {"type": "string"}},
            "languages": {
                "type": "object",
                "properties": {
                    "primary": {"type": "array", "items": {"type": "string"}},
                    "secondary": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["primary", "secondary"],
            },
            "closingText": {"type": "string"},
        },
        "required": [
            "introText",
            "primaryMarkets",
            "emergingMarkets",
            "languages",
            "closingText",
        ],
    },
    "data_gaps": {
        "type": "object",
        "properties": {
            "introText": {"type": "string"},
            "confidenceLevels": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "symbol": {"type": "string"},
                        "label": {"type": "string"},
                        "description": {"type": "string"},
                    },
                    "required": ["symbol", "label", "description"],
                },
            },
            "limitations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                    },
                    "required": ["title", "description"],
                },
            },
            "metadata": {
                "type": "object",
                "properties": {
                    "researchDate": {"type": "string"},
                    "method": {"type": "string"},
                    "note": {"type": "string"},
                },
                "required": ["researchDate", "method", "note"],
            },
            "closingText": {"type": "string"},
        },
        "required": [
            "introText",
            "confidenceLevels",
            "limitations",
            "metadata",
            "closingText",
        ],
    },
}

