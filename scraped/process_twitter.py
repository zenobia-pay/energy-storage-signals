#!/usr/bin/env python3
"""Process Twitter search results and add unique accounts to JSONL files."""

import json
import sys
import re
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")

# Energy storage related keywords for filtering
ENERGY_KEYWORDS = [
    'energy', 'storage', 'battery', 'grid', 'bess', 'solar', 'wind', 'power',
    'renewable', 'utility', 'electric', 'ferc', 'ercot', 'pjm', 'iso', 'clean',
    'climate', 'transition', 'ev', 'charging', 'lithium', 'analyst', 'research',
    'policy', 'investment', 'venture', 'capital', 'fund', 'startup', 'ceo',
    'founder', 'director', 'engineer', 'scientist', 'professor', 'journalist',
    'reporter', 'editor', 'infrastructure', 'transmission', 'distribution',
    'megawatt', 'gigawatt', 'mw', 'gw', 'kwh', 'mwh', 'gwh', 'decarbonization',
    'net zero', 'sustainability', 'cleantech', 'greentech', 'bloomberg', 'nef',
    'wood mackenzie', 'caiso', 'miso', 'capacity', 'dispatch', 'peaker'
]

def load_existing_handles():
    """Load existing Twitter handles from file."""
    handles = set()
    twitter_file = BASE_DIR / "twitter-accounts.jsonl"
    if twitter_file.exists():
        with open(twitter_file, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        handles.add(data.get('handle', '').lower())
                    except:
                        pass
    return handles

def load_existing_people():
    """Load existing people names from file."""
    people = set()
    people_file = BASE_DIR / "people.jsonl"
    if people_file.exists():
        with open(people_file, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        people.add(data.get('name', '').lower())
                    except:
                        pass
    return people

def is_relevant(text, name, username):
    """Check if account seems relevant to energy storage."""
    combined = f"{text} {name} {username}".lower()
    return any(kw in combined for kw in ENERGY_KEYWORDS)

def is_bot_or_spam(username, name=''):
    """Filter out obvious bots and spam accounts."""
    username_lower = username.lower()
    name_lower = name.lower() if name else ''
    # Skip obvious spam patterns
    spam_patterns = ['deal', 'coupon', 'free', 'win', 'giveaway', 'sale']
    if any(p in username_lower for p in spam_patterns):
        return True
    if username_lower == 'grok':  # Skip Grok bot
        return True
    # Skip random numeric handles
    if len(username) > 12 and sum(c.isdigit() for c in username) > 5:
        return True
    return False

def categorize_account(text, name, bio=''):
    """Categorize the account type."""
    combined = f"{text} {name} {bio}".lower()
    
    if any(w in combined for w in ['professor', 'researcher', 'phd', 'university', 'lab', 'institute']):
        return 'researcher'
    if any(w in combined for w in ['ceo', 'founder', 'president', 'cto', 'cfo', 'executive']):
        return 'executive'
    if any(w in combined for w in ['analyst', 'research']):
        return 'analyst'
    if any(w in combined for w in ['journalist', 'reporter', 'editor', 'news', 'media']):
        return 'journalist'
    if any(w in combined for w in ['investor', 'venture', 'capital', 'fund', 'partner']):
        return 'investor'
    if any(w in combined for w in ['policy', 'regulatory', 'ferc', 'commissioner', 'government']):
        return 'policy'
    if any(w in combined for w in ['company', 'corp', 'inc', 'llc', 'ltd']):
        return 'company'
    return 'other'

def extract_mentions(text):
    """Extract @mentions from tweet text."""
    pattern = r'@(\w+)'
    return re.findall(pattern, text)

def process_tweets(tweets_json):
    """Process tweets JSON and extract accounts."""
    try:
        tweets = json.loads(tweets_json)
    except:
        return [], []
    
    existing_handles = load_existing_handles()
    existing_people = load_existing_people()
    
    new_accounts = []
    new_people = []
    seen_handles = set()
    seen_names = set()
    
    for tweet in tweets:
        author = tweet.get('author', {})
        username = author.get('username', '')
        name = author.get('name', '')
        text = tweet.get('text', '')
        
        # Process the author
        if username and name:
            handle_lower = username.lower()
            name_lower = name.lower()
            
            if handle_lower not in existing_handles and handle_lower not in seen_handles:
                if not is_bot_or_spam(username, name):
                    if is_relevant(text, name, username):
                        seen_handles.add(handle_lower)
                        category = categorize_account(text, name)
                        
                        account = {
                            "handle": username,
                            "name": name,
                            "bio": None,
                            "category": category,
                            "followerCount": None,
                            "url": f"https://twitter.com/{username}",
                            "source": "twitter_search"
                        }
                        new_accounts.append(account)
                        
                        if category in ['researcher', 'analyst', 'executive', 'journalist', 'investor', 'policy']:
                            if name_lower not in existing_people and name_lower not in seen_names:
                                seen_names.add(name_lower)
                                person = {
                                    "name": name,
                                    "role": category.title(),
                                    "company": None,
                                    "twitter": username,
                                    "linkedin": None,
                                    "category": category,
                                    "source": "twitter_search",
                                    "notes": text[:200] if len(text) > 200 else text
                                }
                                new_people.append(person)
        
        # Process mentions in the tweet
        mentions = extract_mentions(text)
        for mention in mentions:
            mention_lower = mention.lower()
            if mention_lower not in existing_handles and mention_lower not in seen_handles:
                if not is_bot_or_spam(mention):
                    # Add mention as account (we don't have their name)
                    seen_handles.add(mention_lower)
                    account = {
                        "handle": mention,
                        "name": None,
                        "bio": None,
                        "category": "mentioned",
                        "followerCount": None,
                        "url": f"https://twitter.com/{mention}",
                        "source": "twitter_mention"
                    }
                    new_accounts.append(account)
        
        # Process quoted tweets
        quoted = tweet.get('quotedTweet', {})
        if quoted:
            q_author = quoted.get('author', {})
            q_username = q_author.get('username', '')
            q_name = q_author.get('name', '')
            q_text = quoted.get('text', '')
            
            if q_username and q_name:
                q_handle_lower = q_username.lower()
                q_name_lower = q_name.lower()
                
                if q_handle_lower not in existing_handles and q_handle_lower not in seen_handles:
                    if not is_bot_or_spam(q_username, q_name):
                        if is_relevant(q_text, q_name, q_username):
                            seen_handles.add(q_handle_lower)
                            category = categorize_account(q_text, q_name)
                            
                            account = {
                                "handle": q_username,
                                "name": q_name,
                                "bio": None,
                                "category": category,
                                "followerCount": None,
                                "url": f"https://twitter.com/{q_username}",
                                "source": "twitter_quoted"
                            }
                            new_accounts.append(account)
    
    return new_accounts, new_people

def append_to_files(accounts, people):
    """Append new accounts and people to JSONL files."""
    twitter_file = BASE_DIR / "twitter-accounts.jsonl"
    people_file = BASE_DIR / "people.jsonl"
    
    accounts_added = 0
    people_added = 0
    
    with open(twitter_file, 'a') as f:
        for acc in accounts:
            f.write(json.dumps(acc) + '\n')
            accounts_added += 1
    
    with open(people_file, 'a') as f:
        for person in people:
            f.write(json.dumps(person) + '\n')
            people_added += 1
    
    return accounts_added, people_added

if __name__ == "__main__":
    # Read JSON from stdin
    tweets_json = sys.stdin.read()
    accounts, people = process_tweets(tweets_json)
    accounts_added, people_added = append_to_files(accounts, people)
    print(f"Added {accounts_added} accounts, {people_added} people")
