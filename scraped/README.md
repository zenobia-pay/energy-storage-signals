# Energy Storage Intelligence - Scraped Data
## Summary - 2026-02-19

This directory contains scraped plain-text content from energy storage signal sources.

## Statistics
- **Total Files**: 25 .txt files
- **Total Size**: 480 KB
- **Total Lines**: ~5,500 lines of content
- **Scraped Date**: February 19, 2026

## Directory Structure

### Podcasts (`/podcasts/`)
| Podcast | Episodes | Guests | Notes |
|---------|----------|--------|-------|
| The Energy Gang | ✅ 560 episodes | ✅ | Full RSS feed parsed |
| Resources Radio | ✅ 24+ episodes | ✅ | Recent episodes + guests |
| Volts | ✅ Overview | - | David Roberts podcast |
| Catalyst | ✅ Overview | - | Shayle Kann |
| The Interchange | ✅ Overview | - | Wood Mackenzie |
| My Climate Journey | ✅ Overview | - | Jason Jacobs |

### Twitter (`/twitter/`)
| Account | Bio | Tweets | Following |
|---------|-----|--------|-----------|
| @JesseJenkins | - | ✅ 14 tweets | - |
| @drvolts | - | ✅ 8 tweets | - |
| @fluenceenergy | - | ✅ 6 tweets | - |
| @FormEnergyInc | - | ✅ 4 tweets | - |
| @CaliforniaISO | - | ✅ 4 tweets | - |
| @ERCOT_ISO | - | ✅ 5 tweets | - |
| @jburwen | - | ✅ 6 tweets | - |

### Think Tanks (`/think-tanks/`)
| Organization | About | Staff | Reports |
|--------------|-------|-------|---------|
| RMI | ✅ | ✅ 700+ staff | - |
| E3 | ✅ | - | - |
| LBNL/EMP | ✅ | - | - |
| NREL | ✅ | - | - |

### Government (`/government/`)
| Agency | Documents |
|--------|-----------|
| FERC | Order 2023 (Interconnection), Order 841 (Storage Markets) |
| DOE | LDES Earthshot Initiative |
| EIA | Battery Storage Data Overview |

## Key Content Highlights

### From Podcasts
- **Energy Gang**: 560 episodes covering clean energy since ~2012
- **Resources Radio**: RFF podcast with economics focus
- **Volts**: Technical deep dives with David Roberts

### From Twitter
- **Jesse Jenkins**: Multi-day storage research, $10/kWh threshold analysis
- **David Roberts**: Sodium-ion batteries, solar+storage economics
- **Fluence**: US manufacturing facility (Arizona), supply chain
- **Form Energy**: Hiring 50+ roles, multi-day iron-air batteries
- **CAISO**: 122 MW → 14,000+ MW growth since 2020
- **ERCOT**: ESR dashboard, 174 GW storage pipeline

### From Think Tanks
- **RMI**: 700+ staff, founded by Amory Lovins, focus on market transformation
- **LBNL**: Interconnection queue analysis, cost benchmarking
- **NREL**: Storage Futures Study, Standard Scenarios

### From Government
- **FERC Order 2023**: Interconnection reform for queue backlog
- **FERC Order 841**: Storage participation in wholesale markets
- **DOE LDES Shot**: 90% cost reduction target by 2030

## Limitations
- Twitter: No user profile/following data (bird CLI limitation)
- Some websites blocked by Cloudflare (FERC, LBNL)
- Podcast RSS feeds: Some not publicly accessible
- No PDF extraction capability

## Next Steps for Deeper Scraping
1. Use browser automation for Cloudflare-protected sites
2. Scrape individual podcast episode pages for transcripts
3. Get Twitter following lists via API
4. Extract PDF documents where available
5. Scrape company investor presentations
