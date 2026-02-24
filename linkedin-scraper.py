#!/usr/bin/env python3.11
"""
LinkedIn Energy Storage Scraper
Uses requests library for more robust HTTP handling
"""

import json
import os
import time
import random
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system("pip3.11 install requests")
    import requests

try:
    import rookiepy
except ImportError:
    print("Installing rookiepy...")
    os.system("pip3.11 install rookiepy")
    import rookiepy

# Config
OUTPUT_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")
OUTPUT_FILE = OUTPUT_DIR / "linkedin-profiles.jsonl"
LOG_FILE = OUTPUT_DIR / "scrape-log.json"

MIN_DELAY = 5  # seconds
MAX_DELAY = 12  # seconds
MAX_RETRIES = 3

VOYAGER_BASE = "https://www.linkedin.com/voyager/api"

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
]


def extract_cookies():
    """Extract LinkedIn cookies from Chrome"""
    all_cookies = rookiepy.chrome()
    linkedin = [c for c in all_cookies if 'linkedin' in c.get('domain', '').lower()]
    
    cookie_dict = {}
    for c in linkedin:
        name = c['name']
        if name not in cookie_dict or (c.get('expires', 0) or 0) > (cookie_dict.get(name, {}).get('expires', 0) or 0):
            cookie_dict[name] = c
    
    result = {name: c['value'] for name, c in cookie_dict.items()}
    
    if 'li_at' not in result:
        raise Exception("No li_at cookie found. Log into LinkedIn in Chrome first.")
    
    return result


def rate_limit():
    """Random delay between requests"""
    delay = MIN_DELAY + random.random() * (MAX_DELAY - MIN_DELAY)
    time.sleep(delay)


class LinkedInScraper:
    def __init__(self):
        self.cookies = extract_cookies()
        self.csrf_token = self.cookies.get('JSESSIONID', '').strip('"')
        self.session = requests.Session()
        
        # Set up session with cookies
        for name, value in self.cookies.items():
            self.session.cookies.set(name, value, domain='.linkedin.com')
        
        self.seen_profiles = set()
        self.stats = {'searched': 0, 'found': 0, 'saved': 0, 'errors': 0}
        
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
    
    def _headers(self):
        return {
            'user-agent': random.choice(USER_AGENTS),
            'accept': 'application/vnd.linkedin.normalized+json+2.1',
            'accept-language': 'en-US,en;q=0.9',
            'x-li-lang': 'en_US',
            'x-li-track': json.dumps({
                'clientVersion': '1.13.8837',
                'mpVersion': '1.13.8837',
                'osName': 'web',
                'timezoneOffset': -5,
                'deviceFormFactor': 'DESKTOP',
                'mpName': 'voyager-web'
            }),
            'x-restli-protocol-version': '2.0.0',
            'csrf-token': self.csrf_token,
        }
    
    def request(self, url, retries=MAX_RETRIES):
        """Make a request with rate limiting and retries"""
        rate_limit()
        
        for attempt in range(retries):
            try:
                resp = self.session.get(url, headers=self._headers(), timeout=30)
                
                if resp.status_code == 429:
                    print(f"  ⚠️  Rate limited! Waiting 120s...")
                    time.sleep(120)
                    continue
                
                if resp.status_code in (401, 403):
                    print(f"  ❌ Auth error {resp.status_code} - cookies may have expired")
                    self.stats['errors'] += 1
                    return None
                
                if resp.status_code == 302:
                    print(f"  ⚠️  Redirect (session expired?) - {resp.headers.get('location', '')}")
                    self.stats['errors'] += 1
                    return None
                
                if not resp.ok:
                    print(f"  HTTP {resp.status_code}: {resp.text[:200]}")
                    if attempt < retries - 1:
                        time.sleep(10 * (attempt + 1))
                        continue
                    return None
                
                self.stats['searched'] += 1
                return resp.json()
                
            except requests.exceptions.RequestException as e:
                print(f"  Request error: {e}")
                if attempt < retries - 1:
                    time.sleep(10 * (attempt + 1))
        
        return None
    
    def extract_profiles(self, data):
        """Extract profiles from API response"""
        if not data:
            return []
        
        profiles = []
        included = data.get('included', [])
        
        for item in included:
            item_type = item.get('$type', '')
            if 'MiniProfile' in item_type or 'Profile' in item_type:
                public_id = item.get('publicIdentifier')
                if not public_id or public_id in self.seen_profiles:
                    continue
                
                profile = {
                    'url': f"https://www.linkedin.com/in/{public_id}",
                    'publicId': public_id,
                    'name': f"{item.get('firstName', '')} {item.get('lastName', '')}".strip(),
                    'title': item.get('occupation') or item.get('headline', ''),
                    'company': '',
                }
                
                # Extract company from title
                import re
                match = re.search(r'(?:at|@)\s+(.+?)(?:\s*[|·]|$)', profile['title'], re.I)
                if match:
                    profile['company'] = match.group(1).strip()
                
                self.seen_profiles.add(public_id)
                profiles.append(profile)
        
        return profiles
    
    def search_people(self, keywords, start=0, count=25):
        """Search for people by keywords"""
        from urllib.parse import urlencode, quote
        
        params = {
            'decorationId': 'com.linkedin.voyager.dash.deco.search.SearchClusterCollection-175',
            'count': str(count),
            'q': 'all',
            'query': f'(keywords:{quote(keywords)},resultType:PEOPLE)',
            'start': str(start),
        }
        
        url = f"{VOYAGER_BASE}/search/dash/clusters?{urlencode(params, safe='():,')}"
        print(f"  Searching: '{keywords}' (start={start})")
        
        data = self.request(url)
        return self.extract_profiles(data)
    
    def search_by_title(self, title_keywords, start=0, count=25):
        """Search for people with specific title"""
        from urllib.parse import urlencode, quote
        
        params = {
            'decorationId': 'com.linkedin.voyager.dash.deco.search.SearchClusterCollection-175',
            'count': str(count),
            'q': 'all',
            'query': f'(title:{quote(title_keywords)},resultType:PEOPLE)',
            'start': str(start),
        }
        
        url = f"{VOYAGER_BASE}/search/dash/clusters?{urlencode(params, safe='():,')}"
        print(f"  Title search: '{title_keywords}' (start={start})")
        
        data = self.request(url)
        return self.extract_profiles(data)
    
    def get_profile(self, public_id):
        """Get full profile data"""
        from urllib.parse import quote
        url = f"{VOYAGER_BASE}/identity/profiles/{quote(public_id)}/profileView"
        print(f"  Getting profile: {public_id}")
        return self.request(url)
    
    def save_profiles(self, profiles):
        """Append profiles to output file"""
        with open(OUTPUT_FILE, 'a') as f:
            for p in profiles:
                f.write(json.dumps(p) + '\n')
                self.stats['saved'] += 1
        self.stats['found'] += len(profiles)
        print(f"    → Found {len(profiles)} profiles (total: {self.stats['found']})")
    
    def save_progress(self):
        """Save progress to log file"""
        with open(LOG_FILE, 'w') as f:
            json.dump({
                'stats': self.stats,
                'unique_profiles': len(self.seen_profiles),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            }, f, indent=2)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    scraper = LinkedInScraper()
    
    # Test connectivity first
    print("Testing LinkedIn API connectivity...")
    test = scraper.get_profile('rprendergast')
    if not test:
        print("\n❌ Cannot connect to LinkedIn API. Session may be expired or blocked.")
        print("Try logging into LinkedIn in Chrome browser again.")
        sys.exit(1)
    print("✓ Connected successfully!\n")
    
    # === Phase 1: Keyword searches ===
    keyword_searches = [
        'energy storage manager',
        'energy storage director', 
        'battery storage engineer',
        'battery manager energy',
        'grid scale storage',
        'ESS engineer',
        'utility scale battery',
        'energy storage systems',
        'BESS project manager',
        'stationary storage',
        'energy storage sales',
        'battery energy storage',
        'grid storage solutions',
        'renewable energy storage',
        'storage integration',
        'battery project developer',
        'energy storage analyst',
        'battery supply chain',
        'ESS operations',
        'storage asset manager',
    ]
    
    print("=== PHASE 1: Keyword Searches ===")
    for i, kw in enumerate(keyword_searches):
        print(f"\n[{i+1}/{len(keyword_searches)}] '{kw}'")
        
        consecutive_empty = 0
        for start in range(0, 1000, 25):
            profiles = scraper.search_people(kw, start, 25)
            if not profiles:
                consecutive_empty += 1
                if consecutive_empty >= 2:
                    print(f"    → No more results")
                    break
            else:
                consecutive_empty = 0
                scraper.save_profiles(profiles)
                scraper.save_progress()
            
            # Extra delay periodically
            if start > 0 and start % 100 == 0:
                print("    [Extra delay...]")
                time.sleep(10)
    
    # === Phase 2: Title searches ===
    title_searches = [
        'Energy Storage',
        'Battery Director',
        'Battery Manager',
        'Grid Storage',
        'ESS Manager',
        'Storage Engineer',
        'BESS',
    ]
    
    print("\n=== PHASE 2: Title Searches ===")
    for i, title in enumerate(title_searches):
        print(f"\n[{i+1}/{len(title_searches)}] Title: '{title}'")
        
        consecutive_empty = 0
        for start in range(0, 1000, 25):
            profiles = scraper.search_by_title(title, start, 25)
            if not profiles:
                consecutive_empty += 1
                if consecutive_empty >= 2:
                    break
            else:
                consecutive_empty = 0
                scraper.save_profiles(profiles)
                scraper.save_progress()
    
    # === Final stats ===
    print("\n" + "=" * 50)
    print("SCRAPING COMPLETE")
    print(f"Total profiles found: {scraper.stats['found']}")
    print(f"Total unique profiles: {len(scraper.seen_profiles)}")
    print(f"Total API calls: {scraper.stats['searched']}")
    print(f"Errors: {scraper.stats['errors']}")
    print(f"Output: {OUTPUT_FILE}")
    
    scraper.save_progress()


if __name__ == '__main__':
    main()
