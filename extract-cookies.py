#!/usr/bin/env python3.11
"""Extract LinkedIn cookies from Chrome"""

import json
import sys
import rookiepy

all_cookies = rookiepy.chrome()
linkedin = [c for c in all_cookies if 'linkedin' in c.get('domain', '').lower()]

# Build cookie dict, preferring latest expiry
cookie_dict = {}
for c in linkedin:
    name = c['name']
    if name not in cookie_dict or (c.get('expires', 0) or 0) > (cookie_dict.get(name, {}).get('expires', 0) or 0):
        cookie_dict[name] = c

result = {name: c['value'] for name, c in cookie_dict.items()}

if 'li_at' not in result:
    print('{"error": "No li_at cookie found. Log into LinkedIn in Chrome first."}', file=sys.stderr)
    sys.exit(1)

print(json.dumps(result, indent=2))
