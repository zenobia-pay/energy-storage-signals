#!/usr/bin/env python3.11
"""
LinkedIn Browser Scraper - Uses Playwright to scrape via Chrome DevTools Protocol
Connects to existing Chrome browser with LinkedIn logged in
"""

import json
import time
import random
import asyncio
from pathlib import Path
from urllib.parse import quote

# Try to import playwright
try:
    from playwright.async_api import async_playwright
except ImportError:
    import os
    os.system("pip3.11 install playwright")
    from playwright.async_api import async_playwright

# Config  
OUTPUT_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")
OUTPUT_FILE = OUTPUT_DIR / "linkedin-profiles.jsonl"
LOG_FILE = OUTPUT_DIR / "scrape-log.json"
CDP_URL = "http://127.0.0.1:9222"  # Chrome's debugging port

MIN_DELAY = 8   # seconds - LinkedIn is AGGRESSIVE
MAX_DELAY = 15


def rate_limit():
    """Random delay between requests"""
    delay = MIN_DELAY + random.random() * (MAX_DELAY - MIN_DELAY)
    time.sleep(delay)


class BrowserScraper:
    def __init__(self):
        self.seen_profiles = set()
        self.stats = {'pages': 0, 'found': 0, 'saved': 0}
        
        # Load existing profiles
        if OUTPUT_FILE.exists():
            with open(OUTPUT_FILE) as f:
                for line in f:
                    if line.strip():
                        try:
                            p = json.loads(line)
                            if p.get('publicId'):
                                self.seen_profiles.add(p['publicId'])
                        except:
                            pass
            print(f"Loaded {len(self.seen_profiles)} existing profiles")
    
    def save_profiles(self, profiles):
        """Append profiles to output file"""
        new_profiles = [p for p in profiles if p['publicId'] not in self.seen_profiles]
        if not new_profiles:
            return 0
        
        with open(OUTPUT_FILE, 'a') as f:
            for p in new_profiles:
                f.write(json.dumps(p) + '\n')
                self.seen_profiles.add(p['publicId'])
                self.stats['saved'] += 1
        
        self.stats['found'] += len(new_profiles)
        return len(new_profiles)
    
    def save_progress(self):
        """Save progress to log file"""
        with open(LOG_FILE, 'w') as f:
            json.dump({
                'stats': self.stats,
                'unique_profiles': len(self.seen_profiles),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            }, f, indent=2)


async def extract_profiles_from_page(page) -> list:
    """Extract profile data from a LinkedIn search results page"""
    profiles = []
    
    # Wait for results to load
    await asyncio.sleep(2)
    
    # Get all search result items
    # LinkedIn search results have profile links in the format /in/username
    profile_links = await page.query_selector_all('a[href*="/in/"]')
    
    seen_urls = set()
    for link in profile_links:
        try:
            href = await link.get_attribute('href')
            if not href or '/in/' not in href:
                continue
            
            # Skip if we've already seen this URL on this page
            if href in seen_urls:
                continue
            seen_urls.add(href)
            
            # Extract public ID
            parts = href.split('/in/')
            if len(parts) < 2:
                continue
            public_id = parts[1].split('/')[0].split('?')[0]
            if not public_id or len(public_id) < 2:
                continue
            
            # Try to get name from nearby text
            name = ''
            try:
                # Look for the name span near the link
                parent = await link.query_selector('..')
                if parent:
                    name_el = await parent.query_selector('span[aria-hidden="true"]')
                    if name_el:
                        name = await name_el.inner_text()
            except:
                pass
            
            if not name:
                try:
                    name = await link.inner_text()
                except:
                    pass
            
            # Clean up name
            name = name.strip() if name else ''
            if 'View' in name or 'profile' in name.lower():
                name = ''
            
            profile = {
                'url': f'https://www.linkedin.com/in/{public_id}',
                'publicId': public_id,
                'name': name,
                'title': '',  # Will need to get from individual profile pages
                'company': '',
                'source': 'browser_search',
            }
            profiles.append(profile)
            
        except Exception as e:
            continue
    
    return profiles


async def scrape_search_results(page, scraper, search_url: str, max_pages: int = 10):
    """Scrape multiple pages of search results"""
    print(f"\n  Opening: {search_url}")
    
    try:
        await page.goto(search_url, wait_until='networkidle', timeout=30000)
    except Exception as e:
        print(f"  Error loading page: {e}")
        return
    
    await asyncio.sleep(3)
    
    for page_num in range(max_pages):
        print(f"  Page {page_num + 1}...")
        
        profiles = await extract_profiles_from_page(page)
        new_count = scraper.save_profiles(profiles)
        scraper.stats['pages'] += 1
        scraper.save_progress()
        
        print(f"    → Found {len(profiles)} links, {new_count} new (total unique: {len(scraper.seen_profiles)})")
        
        if new_count == 0 and page_num > 0:
            print("    → No new profiles, stopping pagination")
            break
        
        # Look for "Next" button
        next_button = await page.query_selector('button[aria-label="Next"]')
        if not next_button:
            # Try alternative selectors
            next_button = await page.query_selector('[class*="pagination"] button:last-child')
        
        if not next_button:
            print("    → No next button found")
            break
        
        is_disabled = await next_button.get_attribute('disabled')
        if is_disabled:
            print("    → Reached last page")
            break
        
        # Rate limit before clicking
        rate_limit()
        
        try:
            await next_button.click()
            await asyncio.sleep(3)
        except Exception as e:
            print(f"    → Error clicking next: {e}")
            break


async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    scraper = BrowserScraper()
    
    # Keywords to search
    searches = [
        'energy storage manager',
        'energy storage director',
        'battery storage engineer', 
        'BESS project manager',
        'grid scale storage',
        'utility scale battery',
        'ESS engineer',
        'renewable energy storage',
        'battery project developer',
        'energy storage analyst',
        'energy storage systems',
        'battery supply chain',
        'stationary storage',
        'grid storage solutions',
    ]
    
    print("Starting LinkedIn browser scraper...")
    print(f"Will search for {len(searches)} keyword sets\n")
    
    async with async_playwright() as p:
        # Try to connect to existing Chrome via CDP
        print("Attempting to connect to Chrome via CDP...")
        try:
            browser = await p.chromium.connect_over_cdp(CDP_URL)
            print(f"✓ Connected to Chrome!")
        except Exception as e:
            print(f"❌ Could not connect to Chrome at {CDP_URL}")
            print(f"   Error: {e}")
            print("\nTo enable Chrome debugging:")
            print("  1. Close Chrome completely")
            print("  2. Run: /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222")
            print("  3. Log into LinkedIn in that Chrome window")
            print("  4. Run this script again")
            return
        
        # Get the default context and find a LinkedIn tab or create one
        contexts = browser.contexts
        if not contexts:
            print("No browser contexts found")
            return
        
        context = contexts[0]
        pages = context.pages
        
        # Find existing LinkedIn tab or create new one
        page = None
        for p in pages:
            if 'linkedin.com' in p.url:
                page = p
                print(f"Found existing LinkedIn tab: {p.url}")
                break
        
        if not page:
            page = await context.new_page()
            await page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
            await asyncio.sleep(2)
        
        # Check if logged in
        current_url = page.url
        if 'login' in current_url or 'authwall' in current_url:
            print("❌ Not logged into LinkedIn!")
            print("Please log into LinkedIn in the Chrome window and run again.")
            return
        
        print("✓ LinkedIn session active\n")
        
        # Scrape each search
        for i, keywords in enumerate(searches):
            print(f"\n[{i+1}/{len(searches)}] Searching: '{keywords}'")
            
            # Build search URL
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={quote(keywords)}&origin=GLOBAL_SEARCH_HEADER"
            
            await scrape_search_results(page, scraper, search_url, max_pages=15)
            
            # Extra delay between different searches
            if i < len(searches) - 1:
                delay = 15 + random.random() * 10
                print(f"  [Waiting {delay:.0f}s before next search...]")
                await asyncio.sleep(delay)
        
        print("\n" + "=" * 50)
        print("SCRAPING COMPLETE")
        print(f"Total pages scraped: {scraper.stats['pages']}")
        print(f"Total unique profiles: {len(scraper.seen_profiles)}")
        print(f"Output: {OUTPUT_FILE}")
        scraper.save_progress()


if __name__ == '__main__':
    asyncio.run(main())
