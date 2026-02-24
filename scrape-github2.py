#!/usr/bin/env python3
"""
GitHub Energy Storage Scraper v2 - More robust
"""

import json
import subprocess
import time
import sys
from pathlib import Path

DATA_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")
USERS_FILE = DATA_DIR / "github-users.jsonl"

seen_users = set()
stats = {"users": 0, "repos": 0, "api_calls": 0}

def log(msg):
    print(msg, flush=True)

def gh_api(endpoint, per_page=100):
    """Call GitHub API via gh CLI"""
    stats["api_calls"] += 1
    cmd = f'gh api "{endpoint}?per_page={per_page}" 2>/dev/null'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except Exception as e:
        log(f"API error: {e}")
    return None

def save_user(username):
    """Fetch and save user profile"""
    if not username or username in seen_users:
        return False
    
    seen_users.add(username)
    
    data = gh_api(f"users/{username}")
    if not data or not isinstance(data, dict):
        return False
    
    user = {
        "username": data.get("login"),
        "name": data.get("name"),
        "bio": data.get("bio"),
        "company": data.get("company"),
        "location": data.get("location"),
        "blog": data.get("blog"),
        "email": data.get("email"),
        "twitter": data.get("twitter_username"),
        "followers": data.get("followers", 0),
        "following": data.get("following", 0),
        "public_repos": data.get("public_repos", 0),
        "type": data.get("type"),
        "html_url": data.get("html_url"),
    }
    
    with open(USERS_FILE, "a") as f:
        f.write(json.dumps(user) + "\n")
    
    stats["users"] += 1
    if stats["users"] % 25 == 0:
        log(f"[PROGRESS] Users: {stats['users']} | Repos: {stats['repos']} | API calls: {stats['api_calls']}")
    
    return True

def process_repo(full_name):
    """Get contributors and stargazers from a repo"""
    try:
        owner, repo = full_name.split("/")
    except:
        return
    
    stats["repos"] += 1
    
    # Save owner
    save_user(owner)
    
    # Get contributors
    contributors = gh_api(f"repos/{owner}/{repo}/contributors")
    if contributors and isinstance(contributors, list):
        for c in contributors[:50]:
            if isinstance(c, dict) and c.get("login"):
                save_user(c["login"])
    
    # Get stargazers
    stargazers = gh_api(f"repos/{owner}/{repo}/stargazers")
    if stargazers and isinstance(stargazers, list):
        for s in stargazers[:50]:
            if isinstance(s, dict) and s.get("login"):
                save_user(s["login"])
    
    time.sleep(0.05)

def expand_user_network(username):
    """Get followers and following of a user"""
    followers = gh_api(f"users/{username}/followers")
    if followers and isinstance(followers, list):
        for f in followers[:30]:
            if isinstance(f, dict) and f.get("login"):
                save_user(f["login"])
    
    following = gh_api(f"users/{username}/following")
    if following and isinstance(following, list):
        for f in following[:30]:
            if isinstance(f, dict) and f.get("login"):
                save_user(f["login"])

def search_repos(query):
    """Search for repos"""
    cmd = f'gh search repos "{query}" --limit 100 --json fullName 2>/dev/null'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except:
        pass
    return []

def expand_org(org_name):
    """Get org members and repos"""
    log(f"  Expanding org: {org_name}")
    
    # Get org repos
    repos = gh_api(f"orgs/{org_name}/repos")
    if repos and isinstance(repos, list):
        for r in repos[:30]:
            if isinstance(r, dict) and r.get("full_name"):
                process_repo(r["full_name"])

def main():
    log("=== GitHub Energy Storage Scraper v2 ===")
    
    # Search queries
    searches = [
        "energy storage",
        "battery management system",
        "grid storage",
        "BESS battery",
        "lithium battery BMS",
        "battery optimization",
        "microgrid energy",
        "renewable storage",
        "solar battery",
        "EV battery pack",
        "grid scale battery",
        "energy arbitrage",
        "battery thermal management",
        "power electronics battery",
        "smart grid storage",
    ]
    
    all_repos = []
    
    log("Phase 1: Searching repos...")
    for query in searches:
        log(f"  Query: {query}")
        repos = search_repos(query)
        log(f"    Found: {len(repos)}")
        all_repos.extend(repos)
        time.sleep(0.5)
    
    # Dedupe
    seen_repos = set()
    unique_repos = []
    for r in all_repos:
        fn = r.get("fullName", "")
        if fn and fn not in seen_repos:
            seen_repos.add(fn)
            unique_repos.append(fn)
    
    log(f"\nTotal unique repos: {len(unique_repos)}")
    
    log("\nPhase 2: Processing repos (contributors + stargazers)...")
    for i, repo_name in enumerate(unique_repos):
        if i % 50 == 0:
            log(f"  Processing repo {i+1}/{len(unique_repos)}")
        process_repo(repo_name)
    
    log("\nPhase 3: Expanding key orgs...")
    orgs = ["NREL", "sandialabs", "LibreSolar", "GridLab-D", "OEDI-tools", "energy-modelling-toolkit", "NREL-SIIP"]
    for org in orgs:
        expand_org(org)
    
    log("\nPhase 4: Network expansion for high-follower users...")
    # Re-read users file to find high-value users
    high_value = []
    if USERS_FILE.exists():
        with open(USERS_FILE) as f:
            for line in f:
                try:
                    u = json.loads(line)
                    if u.get("followers", 0) > 100:
                        high_value.append(u.get("username"))
                except:
                    pass
    
    log(f"  Found {len(high_value)} high-value users to expand")
    for username in high_value[:100]:
        if username:
            expand_user_network(username)
    
    log(f"\n=== FINAL RESULTS ===")
    log(f"Users saved: {stats['users']}")
    log(f"Repos processed: {stats['repos']}")
    log(f"API calls: {stats['api_calls']}")

if __name__ == "__main__":
    main()
