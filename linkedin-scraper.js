#!/usr/bin/env node
/**
 * LinkedIn Energy Storage Scraper
 * Uses Voyager API for people search, company employees, hashtag feeds
 */

import { existsSync, readFileSync, writeFileSync, appendFileSync, mkdirSync } from 'fs';
import { execSync } from 'child_process';

const VOYAGER_BASE = 'https://www.linkedin.com/voyager/api';
const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36';

// Rate limiting
const MIN_DELAY_MS = 3000;  // 3 seconds between requests (conservative)
const MAX_DELAY_MS = 8000;  // Random up to 8 seconds
let lastRequestTime = 0;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function rateLimit() {
  const elapsed = Date.now() - lastRequestTime;
  const delay = MIN_DELAY_MS + Math.random() * (MAX_DELAY_MS - MIN_DELAY_MS);
  if (elapsed < delay) {
    await sleep(delay - elapsed);
  }
  lastRequestTime = Date.now();
}

// Cookie extraction - uses separate Python script
function extractCookies() {
  const configDir = `${process.env.HOME}/.config/linkedin-cli/accounts`;
  mkdirSync(configDir, { recursive: true });
  const cookieFile = `${configDir}/chrome-live.json`;
  const extractScript = '/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage/extract-cookies.py';
  
  // Run the Python script
  execSync(`python3.11 "${extractScript}" > "${cookieFile}"`, { encoding: 'utf-8' });
  
  return JSON.parse(readFileSync(cookieFile, 'utf-8'));
}

class LinkedInScraper {
  constructor() {
    this.cookies = extractCookies();
    this.cookieString = Object.entries(this.cookies)
      .map(([k, v]) => `${k}=${v}`)
      .join('; ');
    this.csrfToken = (this.cookies.JSESSIONID || '').replace(/^"|"$/g, '');
    this.seenProfiles = new Set();
    this.stats = { searched: 0, found: 0, saved: 0 };
  }

  headers(extra = {}) {
    return {
      'user-agent': USER_AGENT,
      'accept': 'application/vnd.linkedin.normalized+json+2.1',
      'accept-language': 'en-US,en;q=0.9',
      'x-li-lang': 'en_US',
      'x-li-track': JSON.stringify({ clientVersion: '1.13.8837', mpVersion: '1.13.8837', osName: 'web', timezoneOffset: -5, deviceFormFactor: 'DESKTOP', mpName: 'voyager-web' }),
      'x-restli-protocol-version': '2.0.0',
      'csrf-token': this.csrfToken,
      'cookie': this.cookieString,
      ...extra,
    };
  }

  async request(url, retries = 3) {
    await rateLimit();
    
    for (let attempt = 0; attempt < retries; attempt++) {
      try {
        const resp = await fetch(url, { headers: this.headers() });
        
        if (resp.status === 429) {
          console.error('  ⚠️  Rate limited! Waiting 60s...');
          await sleep(60000);
          continue;
        }
        
        if (resp.status === 403 || resp.status === 401) {
          throw new Error(`Auth error ${resp.status} - cookies may have expired`);
        }
        
        if (!resp.ok) {
          const body = await resp.text().catch(() => '');
          console.error(`  HTTP ${resp.status}: ${body.slice(0, 200)}`);
          if (attempt < retries - 1) {
            await sleep(5000 * (attempt + 1));
            continue;
          }
          return null;
        }
        
        return await resp.json();
      } catch (err) {
        console.error(`  Request error: ${err.message}`);
        if (attempt < retries - 1) {
          await sleep(5000 * (attempt + 1));
        }
      }
    }
    return null;
  }

  // Extract profile data from various response structures
  extractProfiles(data) {
    if (!data) return [];
    
    const profiles = [];
    const included = data.included || [];
    
    for (const item of included) {
      if (item.$type === 'com.linkedin.voyager.identity.shared.MiniProfile' ||
          item.$type === 'com.linkedin.voyager.identity.profile.Profile') {
        const publicId = item.publicIdentifier;
        if (!publicId || this.seenProfiles.has(publicId)) continue;
        
        const profile = {
          url: `https://www.linkedin.com/in/${publicId}`,
          publicId,
          name: `${item.firstName || ''} ${item.lastName || ''}`.trim(),
          title: item.occupation || item.headline || '',
          company: '',
        };
        
        // Extract company from title if possible
        const titleMatch = profile.title.match(/(?:at|@)\s+(.+?)(?:\s*[|·]|$)/i);
        if (titleMatch) profile.company = titleMatch[1].trim();
        
        this.seenProfiles.add(publicId);
        profiles.push(profile);
      }
    }
    
    return profiles;
  }

  // People search by keywords
  async searchPeople(keywords, start = 0, count = 25) {
    const params = new URLSearchParams({
      decorationId: 'com.linkedin.voyager.dash.deco.search.SearchClusterCollection-175',
      count: String(count),
      q: 'all',
      query: `(keywords:${encodeURIComponent(keywords)},resultType:PEOPLE)`,
      start: String(start),
    });
    
    console.log(`  Searching: "${keywords}" (start=${start})`);
    const data = await this.request(`${VOYAGER_BASE}/search/dash/clusters?${params}`);
    this.stats.searched++;
    
    return this.extractProfiles(data);
  }

  // Search people with specific title keywords
  async searchByTitle(titleKeywords, start = 0, count = 25) {
    const params = new URLSearchParams({
      decorationId: 'com.linkedin.voyager.dash.deco.search.SearchClusterCollection-175',
      count: String(count),
      q: 'all',
      query: `(title:${encodeURIComponent(titleKeywords)},resultType:PEOPLE)`,
      start: String(start),
    });
    
    console.log(`  Title search: "${titleKeywords}" (start=${start})`);
    const data = await this.request(`${VOYAGER_BASE}/search/dash/clusters?${params}`);
    this.stats.searched++;
    
    return this.extractProfiles(data);
  }

  // Get company page and employees
  async getCompanyEmployees(companyUrn, start = 0, count = 25) {
    const params = new URLSearchParams({
      decorationId: 'com.linkedin.voyager.dash.deco.search.SearchClusterCollection-175',
      count: String(count),
      q: 'all',
      query: `(currentCompany:List(${companyUrn}),resultType:PEOPLE)`,
      start: String(start),
    });
    
    console.log(`  Company employees (${companyUrn}) start=${start}`);
    const data = await this.request(`${VOYAGER_BASE}/search/dash/clusters?${params}`);
    this.stats.searched++;
    
    return this.extractProfiles(data);
  }

  // Get company info by vanity name
  async getCompany(vanityName) {
    const url = `${VOYAGER_BASE}/organization/companies?decorationId=com.linkedin.voyager.deco.organization.web.WebFullCompanyMain-65&q=universalName&universalName=${encodeURIComponent(vanityName)}`;
    console.log(`  Looking up company: ${vanityName}`);
    
    const data = await this.request(url);
    if (!data?.elements?.[0]) return null;
    
    const company = data.elements[0];
    return {
      entityUrn: company.entityUrn,
      name: company.name,
      universalName: company.universalName,
    };
  }

  // Hashtag feed
  async getHashtagFeed(hashtag, start = 0, count = 25) {
    // Remove # if present
    hashtag = hashtag.replace(/^#/, '');
    
    const params = new URLSearchParams({
      count: String(count),
      q: 'hashtag',
      hashtag: hashtag,
      start: String(start),
    });
    
    console.log(`  Hashtag #${hashtag} (start=${start})`);
    const data = await this.request(`${VOYAGER_BASE}/feed/updatesV2?${params}`);
    this.stats.searched++;
    
    return this.extractProfiles(data);
  }

  // Save profile to JSONL file
  saveProfile(profile, outputFile) {
    const line = JSON.stringify(profile) + '\n';
    appendFileSync(outputFile, line);
    this.stats.saved++;
  }

  // Save batch of profiles
  saveBatch(profiles, outputFile) {
    for (const p of profiles) {
      this.saveProfile(p, outputFile);
    }
    this.stats.found += profiles.length;
    console.log(`    → Found ${profiles.length} profiles (total: ${this.stats.found})`);
  }
}

// ─── Main scraping logic ────────────────────────────────────────

async function main() {
  const outputDir = '/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage';
  const outputFile = `${outputDir}/linkedin-profiles.jsonl`;
  const logFile = `${outputDir}/scrape-log.json`;
  
  mkdirSync(outputDir, { recursive: true });
  
  // Load previous progress if exists
  let progress = { lastPhase: '', lastIndex: 0, totalFound: 0 };
  if (existsSync(logFile)) {
    progress = JSON.parse(readFileSync(logFile, 'utf-8'));
  }
  
  // Load seen profiles from existing file
  const scraper = new LinkedInScraper();
  if (existsSync(outputFile)) {
    const lines = readFileSync(outputFile, 'utf-8').split('\n').filter(Boolean);
    for (const line of lines) {
      try {
        const p = JSON.parse(line);
        if (p.publicId) scraper.seenProfiles.add(p.publicId);
      } catch {}
    }
    console.log(`Loaded ${scraper.seenProfiles.size} existing profiles`);
  }
  
  function saveProgress() {
    progress.totalFound = scraper.stats.found;
    writeFileSync(logFile, JSON.stringify(progress, null, 2));
  }

  // ─── Phase 1: Keyword searches ────────────────────────────────
  const keywordSearches = [
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
  ];

  console.log('\n=== PHASE 1: Keyword Searches ===');
  for (let i = 0; i < keywordSearches.length; i++) {
    const kw = keywordSearches[i];
    console.log(`\n[${i+1}/${keywordSearches.length}] "${kw}"`);
    
    // Paginate through results (LinkedIn caps at ~1000)
    for (let start = 0; start < 1000; start += 25) {
      const profiles = await scraper.searchPeople(kw, start, 25);
      if (!profiles || profiles.length === 0) {
        console.log(`    → No more results`);
        break;
      }
      scraper.saveBatch(profiles, outputFile);
      saveProgress();
      
      // Extra delay every 100 results
      if (start > 0 && start % 100 === 0) {
        console.log('    [Extra delay...]');
        await sleep(5000);
      }
    }
  }

  // ─── Phase 2: Title searches ──────────────────────────────────
  const titleSearches = [
    'Energy Storage',
    'Battery Director',
    'Battery Manager',
    'Grid Storage',
    'ESS Manager',
    'Storage Engineer',
    'BESS',
  ];

  console.log('\n=== PHASE 2: Title Searches ===');
  for (let i = 0; i < titleSearches.length; i++) {
    const title = titleSearches[i];
    console.log(`\n[${i+1}/${titleSearches.length}] Title: "${title}"`);
    
    for (let start = 0; start < 1000; start += 25) {
      const profiles = await scraper.searchByTitle(title, start, 25);
      if (!profiles || profiles.length === 0) {
        console.log(`    → No more results`);
        break;
      }
      scraper.saveBatch(profiles, outputFile);
      saveProgress();
    }
  }

  // ─── Phase 3: Company lookups ─────────────────────────────────
  const companies = [
    'fluence',
    'tesla-energy',
    'byd-company',
    'catlobal',  // CATL
    'nextera-energy',
    'duke-energy',
    'enel',
    'stem-inc',
    'ess-inc',
    'form-energy',
    'eos-energy',
    'energy-vault',
    'northvolt',
    'lg-energy-solution',
    'samsung-sdi',
    'powin-energy',
    'wartsila',
    'siemens-gamesa',
  ];

  console.log('\n=== PHASE 3: Company Employees ===');
  for (const companyVanity of companies) {
    console.log(`\nLooking up company: ${companyVanity}`);
    const company = await scraper.getCompany(companyVanity);
    
    if (!company) {
      console.log(`  ⚠️  Company not found, trying search...`);
      // Try a keyword search instead
      const profiles = await scraper.searchPeople(`${companyVanity} energy storage`, 0, 25);
      if (profiles) scraper.saveBatch(profiles, outputFile);
      continue;
    }
    
    console.log(`  Found: ${company.name} (${company.entityUrn})`);
    
    // Get employees
    for (let start = 0; start < 500; start += 25) {
      const profiles = await scraper.getCompanyEmployees(company.entityUrn, start, 25);
      if (!profiles || profiles.length === 0) {
        console.log(`    → No more employees`);
        break;
      }
      // Tag with company
      for (const p of profiles) {
        if (!p.company) p.company = company.name;
      }
      scraper.saveBatch(profiles, outputFile);
      saveProgress();
    }
  }

  // ─── Phase 4: Hashtag feeds ───────────────────────────────────
  const hashtags = [
    'energystorage',
    'batterystorage', 
    'gridscale',
    'cleanenergy',
    'BESS',
    'gridmodernization',
    'renewableenergy',
    'batterytech',
    'energytransition',
  ];

  console.log('\n=== PHASE 4: Hashtag Feeds ===');
  for (const tag of hashtags) {
    console.log(`\n#${tag}`);
    
    for (let start = 0; start < 300; start += 25) {
      const profiles = await scraper.getHashtagFeed(tag, start, 25);
      if (!profiles || profiles.length === 0) {
        console.log(`    → No more posts`);
        break;
      }
      scraper.saveBatch(profiles, outputFile);
      saveProgress();
    }
  }

  // ─── Final stats ──────────────────────────────────────────────
  console.log('\n' + '='.repeat(50));
  console.log('SCRAPING COMPLETE');
  console.log(`Total profiles found: ${scraper.stats.found}`);
  console.log(`Total unique profiles: ${scraper.seenProfiles.size}`);
  console.log(`Total API calls: ${scraper.stats.searched}`);
  console.log(`Output: ${outputFile}`);
  
  saveProgress();
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
