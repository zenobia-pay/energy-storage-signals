# LinkedIn Scraping Status

## Date: 2026-02-20

## Status: ⛔ BLOCKED - Anti-automation detection

## TL;DR
LinkedIn aggressively blocks all API/automated access. Need human to attach a LinkedIn tab via Chrome Relay, then I can scrape via browser automation.

### What Was Attempted

1. **Direct API access via linkedin-chrome CLI** - BLOCKED
   - LinkedIn's Voyager API now actively detects and blocks automated requests
   - Even with valid cookies from Chrome, API requests get redirected and sessions invalidated
   - Error: HTTP 302 redirects with `li_at=delete me` (session invalidation)

2. **Python requests library** - BLOCKED  
   - Same issue - LinkedIn detects non-browser requests
   - Error: "Exceeded 30 redirects"

3. **Browser automation (Playwright)** - SETUP NEEDED
   - Script created but requires Chrome debugging port enabled
   - Chrome needs to be launched with: `--remote-debugging-port=9222`

4. **OpenClaw Browser Relay** - NO TAB ATTACHED
   - No LinkedIn tab currently connected to the Chrome relay

### Files Created

- `linkedin-scraper.js` - Node.js API scraper (blocked by LinkedIn)
- `linkedin-scraper.py` - Python requests scraper (blocked by LinkedIn)
- `browser-scraper.py` - Playwright browser automation script
- `extract-cookies.py` - Cookie extraction helper

### Recommendations

1. **Browser Relay Method** (Easiest)
   - Open LinkedIn in Chrome
   - Click OpenClaw Browser Relay toolbar icon to attach the tab
   - Can then use `browser` tool to navigate and snapshot pages

2. **Chrome Debugging Method**
   - Close Chrome completely
   - Run: `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222`
   - Log into LinkedIn
   - Run `browser-scraper.py`

3. **Manual + AI Assist**
   - Manually navigate LinkedIn search pages
   - Use AI to help extract/organize the data

4. **Third-party Service**
   - Use a LinkedIn scraping service like PhantomBuster, Dux-Soup, or Apify
   - These have rate-limit management built in

### Target Search Terms (Ready to Use)

```
energy storage manager
energy storage director
battery storage engineer
BESS project manager
grid scale storage
utility scale battery
ESS engineer
renewable energy storage
battery project developer
energy storage analyst
```

### Target Companies

```
Fluence
Tesla Energy
BYD
CATL
NextEra Energy
Duke Energy
Enel
Stem Inc
ESS Inc
Form Energy
Eos Energy
Energy Vault
Northvolt
LG Energy Solution
Samsung SDI
Powin Energy
Wärtsilä
```
