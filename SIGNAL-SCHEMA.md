# Signal Schema v2: Account-Driven Intelligence

Based on the Deep Research philosophy: **Find trustworthy accounts → Build their canon → Follow their network**

---

## Core Principle

**A signal is a person, not a piece of content.**

Every signal should answer: "Who is this person, why should I trust them, and what shaped their thinking?"

---

## Signal Schema

```jsonc
{
  // === IDENTITY ===
  "handle": "string",              // Primary platform handle
  "name": "string",                // Display name
  "platforms": {                   // Cross-platform presence
    "twitter": "@handle",
    "linkedin": "profile-slug",
    "substack": "publication-name",
    "podcast": "show-name",
    "github": "username",
    "arena": "username"
  },
  
  // === TRUST INDICATORS ===
  "tier": "A|B|C|D",               // A=primary source, B=reliable analyst, C=aggregator, D=noise
  "trustScore": 0-100,             // Computed from indicators below
  "trustIndicators": {
    "specificExpertise": true,     // Knows one thing deeply
    "regularPosting": true,        // Active, not dormant
    "originalThinking": true,      // Says things you haven't heard
    "showsReceipts": true,         // Cites sources, shows work
    "skinInGame": true,            // Has something to lose
    "trackRecord": "string"        // Notable predictions/calls
  },
  
  // === CANON ===
  "canon": {
    "books": ["Title - Author"],
    "papers": ["arxiv:1234.5678"],
    "mentors": ["@handle"],
    "podcasts": ["appearances"],
    "influences": ["key figures"],
    "events": ["formative experiences"]
  },
  
  // === NETWORK POSITION ===
  "network": {
    "followedBy": ["@handle"],     // Who we trust that follows them
    "follows": ["@handle"],        // Who they follow (expansion candidates)
    "citedBy": ["@handle"],        // Who quotes/references them
    "cites": ["@handle"],          // Who they quote/reference
    "appearedWith": ["@handle"]    // Podcast co-guests, co-authors
  },
  
  // === ENGAGEMENT SIGNALS ===
  "engagement": {
    "avgLikes": 0,
    "avgRetweets": 0,
    "highEngagementPosts": [       // Posts that got unusual attention
      {
        "url": "string",
        "likes": 0,
        "topic": "string"
      }
    ]
  },
  
  // === CONTENT FOCUS ===
  "themes": ["energy storage", "BESS", "grid policy"],
  "stance": {                      // Known positions (predictive)
    "IRA": "supportive",
    "nuclear": "skeptical",
    "tariffs": "concerned"
  },
  
  // === METADATA ===
  "source": "how we found them",
  "addedAt": "ISO date",
  "lastScraped": "ISO date",
  "notes": "free text"
}
```

---

## Tier Definitions

| Tier | Description | Example |
|------|-------------|---------|
| **A** | Primary sources. Create original research, have direct industry access, make predictions with track records. | @JesseJenkins, @shaylekann, @jburwen |
| **B** | Reliable analysts. Synthesize well, cite sources, have specific expertise. | @ThinkWithSaurav, @QuincyEdmundLee |
| **C** | Aggregators. Useful for news flow, but mostly amplify others. | @CanaryMediaInc, @UtilityDive |
| **D** | Noise. Low signal-to-noise, engagement farming, or unreliable. | (filter these out) |

---

## Discovery Methods

### 1. Engagement-Weighted Search
Find **posts** with high engagement on key themes, then extract authors.
```
"energy storage" min_faves:50 since:2025-01-01
"BESS" min_faves:20 since:2025-01-01
"battery grid" min_faves:30 since:2025-01-01
```

### 2. Network Expansion
For each Tier A/B account:
- Who do they follow?
- Who follows them?
- Who do they quote/cite?
- Who appears on podcasts with them?

### 3. Canon Extraction
For key accounts, extract:
- Book recommendations
- Paper citations
- Podcast appearances
- "Best thing I read this week" threads
- Acknowledgments in papers

### 4. Cross-Platform Linking
Same person across platforms:
- Twitter → LinkedIn (for job history, credibility)
- Twitter → Substack (for long-form thinking)
- Twitter → Are.na (for canon/references)
- Twitter → Podcast guest list

---

## Migration Path

### Current State
- `twitter-accounts.jsonl`: 2,807 accounts with basic metadata
- `people.jsonl`: 1,614 people with roles
- `researchers.jsonl`: 7,843 from arXiv

### Target State
- `signals.jsonl`: Unified, enriched records per the schema above
- `canon/`: Extracted canon per account
- `network/`: Network graph data
- `daily/YYYY-MM-DD/`: Scraped content

### Migration Steps
1. Merge twitter-accounts + people + researchers
2. Dedupe by identity (cross-platform matching)
3. Enrich with trust indicators
4. Extract canon from scraped content
5. Build network graph from following/follower data

---

## Quality Over Quantity

**The goal is not 10,000 accounts. The goal is 100 Tier A/B accounts with deep canon understanding.**

A smaller roster of trusted voices, deeply understood, beats a massive list of handles.
