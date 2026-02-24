# Energy Storage Signal Database

Intelligence briefing source database for battery energy storage systems (BESS), grid storage, and related markets.

## Database Structure

| File | Description | Count |
|------|-------------|-------|
| `twitter-accounts.jsonl` | Twitter/X accounts covering energy storage | 151+ |
| `people.jsonl` | Key individuals with social handles and roles | 71+ |
| `think-tanks.jsonl` | Research organizations and policy institutes | 21 |
| `podcasts.jsonl` | Energy/cleantech podcasts | 20 |
| `communities.jsonl` | Slack, Discord, VC communities, research orgs | 23+ |
| `events.jsonl` | Conferences, summits, expos | 17+ |
| `government-docs.jsonl` | FERC orders, DOE programs, IRS guidance | 23 |
| `industry-sources.jsonl` | Trade publications, research firms, data sources | 37 |
| `tariffs.jsonl` | Section 301, anti-dumping, IRA domestic content | 17 |
| `arena-blocks.jsonl` | Are.na channels (requires browser for full extraction) | 3 |
| `twitter-network.jsonl` | High-value network nodes | 7 |

## Key Categories

### Companies
- **Manufacturers**: CATL, BYD, LG Energy Solution, Samsung SDI, Panasonic
- **Integrators**: Fluence, Powin, Stem Inc, Tesla Energy
- **Developers**: NextEra, Plus Power, Jupiter Power, AES
- **LDES**: Form Energy (iron-air), Eos Energy (zinc), ESS Tech, Ambri, Rondo Energy
- **Recyclers**: Redwood Materials, Li-Cycle, Ascend Elements, Cirba Solutions

### People Categories
- **Researchers**: Jesse Jenkins (Princeton), LBNL EMP team
- **Analysts**: Wood Mackenzie, Rho Motion, BloombergNEF, Volta Foundation
- **Executives**: Julian Nebreda (Fluence), JB Straubel (Redwood), Andy Bowman (Jupiter)
- **Policy**: Jason Burwen, Travis Kavulla, FERC Commissioners
- **Media**: David Roberts (Volts), Shayle Kann (Catalyst), Eric Wesoff (Canary)

### VC/Investment
- Breakthrough Energy Ventures
- Energy Impact Partners
- MCJ Collective
- Buoyant Ventures
- Congruent Ventures
- Lowercarbon Capital

### Think Tanks
- NREL, LBNL, Argonne
- RMI (Rocky Mountain Institute)
- Princeton ZERO Lab
- IEEFA, Ember, Pembina Institute

## Data Sources Used
- Twitter/X via `bird` CLI searches
- Web fetch of known URLs
- Structured data from previous research phases

## Schema

### people.jsonl
```json
{
  "name": "string",
  "role": "string", 
  "company": "string",
  "twitter": "@handle",
  "linkedin": "profile-slug",
  "instagram": "@handle",
  "tiktok": "@handle",
  "category": "analyst|executive|researcher|policy|media|investor",
  "source": "string",
  "notes": "string"
}
```

### twitter-accounts.jsonl
```json
{
  "handle": "string",
  "name": "string",
  "bio": "string",
  "category": "company|analyst|trade_publication|developer|utility|etc",
  "followerCount": number|null,
  "url": "string"
}
```

### communities.jsonl
```json
{
  "platform": "slack|discord|community|vc_community|research|podcast|newsletter|organization",
  "name": "string",
  "url": "string",
  "description": "string",
  "invite_source": "string"
}
```

## Status
- **Total signals**: 390+ (as of 2026-02-19)
- **Target**: 1000+ signals
- **In progress**: Additional Twitter searches, depth searches on key people

## Next Steps
1. Expand people.jsonl with LinkedIn URLs via depth searches
2. Add more events from Luma/Eventbrite
3. Extract Are.na channels via browser automation
4. Cross-reference people across platforms (Twitter → LinkedIn → Instagram)
