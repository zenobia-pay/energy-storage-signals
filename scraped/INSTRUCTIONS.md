# Scraping Instructions

## Failure Tracking

**ALL failures must be logged to `FAILURES.txt`**

When a scrape fails, append a line:
```
[FAIL] category | source_name | error_type | url | timestamp
```

Example:
```
[FAIL] podcast | The Interchange | 404 | https://rss.example.com/feed | 2026-02-19T16:15:00
[FAIL] twitter | @somehandle | rate_limited | - | 2026-02-19T16:20:00
[FAIL] think_tank | RMI | cloudflare_blocked | https://rmi.org/team | 2026-02-19T16:25:00
```

## Error Types
- `404` - page not found
- `403` - forbidden/blocked
- `timeout` - request timed out
- `rate_limited` - API rate limit hit
- `cloudflare_blocked` - bot detection
- `pdf_only` - content is PDF, can't extract text
- `login_required` - needs authentication
- `parse_error` - couldn't parse the page structure
- `empty` - page loaded but no content found

## Re-running Failures

After fixing issues, grep FAILURES.txt for specific categories:
```bash
grep "podcast" FAILURES.txt
grep "twitter" FAILURES.txt
```

Then re-run those specific items.
