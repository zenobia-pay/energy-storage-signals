#!/usr/bin/env python3
"""
GitHub Energy Storage Scraper
Target: 20,000+ users
"""

import json
import subprocess
import time
import os
from pathlib import Path

DATA_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")
USERS_FILE = DATA_DIR / "github-users.jsonl"
REPOS_FILE = DATA_DIR / "repos-found.jsonl"
LOG_FILE = DATA_DIR / "scrape-log.json"

# Track what we've seen
seen_users = set()
seen_repos = set()
stats = {"users_found": 0, "repos_processed": 0, "api_calls": 0}

def load_state():
    global seen_users, seen_repos, stats
    if USERS_FILE.exists():
        with open(USERS_FILE) as f:
            for line in f:
                try:
                    u = json.loads(line)
                    seen_users.add(u.get("username", ""))
                except: pass
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            data = json.load(f)
            stats = data.get("stats", stats)
            seen_repos = set(data.get("seen_repos", []))
    print(f"Loaded state: {len(seen_users)} users, {len(seen_repos)} repos processed")

def save_state():
    with open(LOG_FILE, "w") as f:
        json.dump({"stats": stats, "seen_repos": list(seen_repos)[:5000]}, f)

def gh_api(endpoint, per_page=100):
    """Call GitHub API via gh CLI"""
    stats["api_calls"] += 1
    cmd = f'gh api "{endpoint}?per_page={per_page}" 2>/dev/null'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"API error {endpoint}: {e}")
    return []

def get_user_profile(username):
    """Fetch user profile"""
    if not username or username in seen_users:
        return None
    
    data = gh_api(f"users/{username}")
    if not data or isinstance(data, list):
        return None
    
    return {
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
        "created_at": data.get("created_at"),
        "html_url": data.get("html_url"),
    }

def save_user(user):
    """Append user to JSONL file"""
    if not user or not user.get("username"):
        return False
    username = user["username"]
    if username in seen_users:
        return False
    
    seen_users.add(username)
    stats["users_found"] += 1
    
    with open(USERS_FILE, "a") as f:
        f.write(json.dumps(user) + "\n")
    
    return True

def get_repo_contributors(owner, repo):
    """Get contributors for a repo"""
    return gh_api(f"repos/{owner}/{repo}/contributors")

def get_repo_stargazers(owner, repo):
    """Get stargazers for a repo"""
    return gh_api(f"repos/{owner}/{repo}/stargazers")

def get_user_followers(username):
    """Get who follows this user"""
    return gh_api(f"users/{username}/followers")

def get_user_following(username):
    """Get who this user follows"""
    return gh_api(f"users/{username}/following")

def get_org_members(org):
    """Get members of an org"""
    return gh_api(f"orgs/{org}/members")

def expand_user(username, depth=0):
    """Get user profile and optionally their network"""
    if depth > 1 or username in seen_users:
        return
    
    profile = get_user_profile(username)
    if profile and save_user(profile):
        if stats["users_found"] % 50 == 0:
            print(f"Users: {stats['users_found']} | Repos: {stats['repos_processed']} | API calls: {stats['api_calls']}")
            save_state()
        
        # One-depth expansion for high-value users
        if depth == 0 and profile.get("followers", 0) > 50:
            followers = get_user_followers(username)
            for f in (followers or [])[:30]:
                if f.get("login"):
                    expand_user(f["login"], depth=1)
            
            following = get_user_following(username)
            for f in (following or [])[:30]:
                if f.get("login"):
                    expand_user(f["login"], depth=1)

def process_repo(full_name):
    """Process a single repo - get contributors and stargazers"""
    if full_name in seen_repos:
        return
    
    seen_repos.add(full_name)
    stats["repos_processed"] += 1
    
    parts = full_name.split("/")
    if len(parts) != 2:
        return
    owner, repo = parts
    
    # Get owner first
    expand_user(owner)
    
    # Get contributors
    contributors = get_repo_contributors(owner, repo)
    for c in (contributors or []):
        if c.get("login"):
            expand_user(c["login"])
    
    # Get stargazers
    stargazers = get_repo_stargazers(owner, repo)
    for s in (stargazers or []):
        if s.get("login"):
            expand_user(s["login"])
    
    time.sleep(0.1)  # Rate limiting

def search_repos(query):
    """Search for repos and return results"""
    cmd = f'gh search repos "{query}" --limit 100 --json fullName,owner,description,stargazersCount 2>/dev/null'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return json.loads(result.stdout)
    except:
        pass
    return []

def expand_org(org_name):
    """Expand an organization - get all members and their connections"""
    print(f"Expanding org: {org_name}")
    
    # Get org profile
    org_data = gh_api(f"orgs/{org_name}")
    if org_data:
        expand_user(org_name)
    
    # Get members
    members = get_org_members(org_name)
    for m in (members or []):
        if m.get("login"):
            expand_user(m["login"])
    
    # Get org repos and their contributors
    repos = gh_api(f"orgs/{org_name}/repos")
    for r in (repos or [])[:50]:
        if r.get("full_name"):
            process_repo(r["full_name"])

def main():
    load_state()
    
    # Search queries
    searches = [
        "energy storage",
        "battery management system",
        "grid storage",
        "BESS",
        "lithium battery",
        "battery optimization",
        "microgrid",
        "renewable energy storage",
        "power grid battery",
        "EV battery",
        "solar battery",
        "energy arbitrage",
    ]
    
    # Key orgs to expand
    key_orgs = [
        "NREL",
        "sandialabs",
        "LibreSolar",
        "GridLab",
        "OpenEnergyPlatform",
        "OEDI-tools",
        "pypsa",
        "calliope-project",
    ]
    
    print("Phase 1: Searching for repos...")
    all_repos = []
    for query in searches:
        print(f"  Searching: {query}")
        repos = search_repos(query)
        all_repos.extend(repos)
        print(f"    Found {len(repos)} repos")
        time.sleep(1)
    
    print(f"\nTotal repos found: {len(all_repos)}")
    
    print("\nPhase 2: Processing repos...")
    for repo in all_repos:
        if repo.get("fullName"):
            process_repo(repo["fullName"])
    
    print("\nPhase 3: Expanding key orgs...")
    for org in key_orgs:
        expand_org(org)
    
    save_state()
    print(f"\n=== FINAL STATS ===")
    print(f"Users found: {stats['users_found']}")
    print(f"Repos processed: {stats['repos_processed']}")
    print(f"API calls: {stats['api_calls']}")

if __name__ == "__main__":
    main()
