#!/usr/bin/env python3
import json
import sys

seen = set()
output = []

# Try to load existing accounts
try:
    with open('twitter-accounts.jsonl', 'r') as f:
        for line in f:
            try:
                acc = json.loads(line.strip())
                if acc.get('handle'):
                    seen.add(acc['handle'].lower())
            except:
                pass
except:
    pass

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        data = json.loads(line)
        items = data if isinstance(data, list) else [data]
        
        for item in items:
            # Handle search results (tweets)
            if 'author' in item:
                author = item['author']
                handle = author.get('username', '')
                if handle and handle.lower() not in seen:
                    seen.add(handle.lower())
                    output.append({
                        'handle': handle,
                        'name': author.get('name', ''),
                        'authorId': item.get('authorId', ''),
                        'bio': '',
                        'followers': 0,
                        'following': 0,
                        'source': 'search'
                    })
                # Quoted tweets
                if 'quotedTweet' in item and item['quotedTweet']:
                    qt = item['quotedTweet']
                    if 'author' in qt:
                        qauthor = qt['author']
                        qhandle = qauthor.get('username', '')
                        if qhandle and qhandle.lower() not in seen:
                            seen.add(qhandle.lower())
                            output.append({
                                'handle': qhandle,
                                'name': qauthor.get('name', ''),
                                'authorId': qt.get('authorId', ''),
                                'bio': '',
                                'followers': 0,
                                'following': 0,
                                'source': 'search_qt'
                            })
            # Handle followers/following results
            elif 'username' in item:
                handle = item.get('username', '')
                if handle and handle.lower() not in seen:
                    seen.add(handle.lower())
                    output.append({
                        'handle': handle,
                        'name': item.get('name', ''),
                        'authorId': item.get('id', ''),
                        'bio': item.get('description', '')[:500] if item.get('description') else '',
                        'followers': item.get('followersCount', 0),
                        'following': item.get('followingCount', 0),
                        'source': 'network'
                    })
    except Exception as e:
        pass

for acc in output:
    print(json.dumps(acc))

# Print count to stderr
print(f"Extracted {len(output)} new accounts, total seen: {len(seen)}", file=sys.stderr)
