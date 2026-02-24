#!/usr/bin/env python3
import json
import sys

# Read all search results from stdin
accounts = {}

for line in sys.stdin:
    try:
        data = json.loads(line.strip())
        if isinstance(data, list):
            for tweet in data:
                if 'author' in tweet:
                    author = tweet['author']
                    handle = author.get('username', '')
                    if handle and handle not in accounts:
                        accounts[handle] = {
                            'handle': handle,
                            'name': author.get('name', ''),
                            'authorId': tweet.get('authorId', ''),
                            'bio': '',  # Not in search results
                            'followers': 0,
                            'following': 0,
                            'source': 'search'
                        }
                # Also get quoted tweet authors
                if 'quotedTweet' in tweet and tweet['quotedTweet']:
                    qt = tweet['quotedTweet']
                    if 'author' in qt:
                        author = qt['author']
                        handle = author.get('username', '')
                        if handle and handle not in accounts:
                            accounts[handle] = {
                                'handle': handle,
                                'name': author.get('name', ''),
                                'authorId': qt.get('authorId', ''),
                                'bio': '',
                                'followers': 0,
                                'following': 0,
                                'source': 'search_quoted'
                            }
    except:
        pass

# Output as JSONL
for acc in accounts.values():
    print(json.dumps(acc))
