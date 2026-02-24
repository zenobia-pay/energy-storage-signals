#!/usr/bin/env python3
"""Bulk arXiv scraper for energy storage researchers."""
import urllib.request
import re
import json
import time
import os

def fetch_arxiv(query, start=0, max_results=500):
    """Fetch arXiv API results."""
    url = f"https://export.arxiv.org/api/query?search_query={query}&start={start}&max_results={max_results}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def extract_researchers(content):
    """Extract researchers from arXiv XML."""
    researchers = {}
    papers = []
    
    skip_keywords = [
        'Dark Energy', 'globular cluster', 'malaria', 'lithium abundances', 
        'Lithium in the Universe', 'fermion', 'protostellar', 'GRID detector',
        'Gamma-Ray', 'CubeSat', 'quasicrystal', 'cosmological', 'muonic', 
        'solvated in helium', 'quantum battery', 'quantum batteries'
    ]
    
    entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)
    
    for entry in entries:
        paper_id_match = re.search(r'<id>http://arxiv.org/abs/(.*?)</id>', entry)
        title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
        summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
        published_match = re.search(r'<published>(.*?)</published>', entry)
        doi_match = re.search(r'<arxiv:doi>(.*?)</arxiv:doi>', entry)
        journal_match = re.search(r'<arxiv:journal_ref>(.*?)</arxiv:journal_ref>', entry)
        
        title_text = title_match.group(1).strip().replace('\n', ' ') if title_match else ""
        
        if any(kw.lower() in title_text.lower() for kw in skip_keywords):
            continue
            
        paper = {
            'arxiv_id': paper_id_match.group(1) if paper_id_match else None,
            'title': title_text,
            'abstract': summary_match.group(1).strip().replace('\n', ' ')[:500] if summary_match else None,
            'published': published_match.group(1) if published_match else None,
            'doi': doi_match.group(1) if doi_match else None,
            'journal': journal_match.group(1) if journal_match else None,
            'authors': []
        }
        
        author_blocks = re.findall(r'<author>(.*?)</author>', entry, re.DOTALL)
        for block in author_blocks:
            name_match = re.search(r'<name>(.*?)</name>', block)
            affil_match = re.search(r'<arxiv:affiliation>(.*?)</arxiv:affiliation>', block)
            
            if name_match:
                name = name_match.group(1).strip()
                affiliation = affil_match.group(1).strip() if affil_match else None
                
                if 'Collaboration' in name or len(name) < 3:
                    continue
                
                paper['authors'].append(name)
                key = name.lower().replace(' ', '_').replace('.', '').replace(',', '')
                
                if key not in researchers:
                    researchers[key] = {
                        'name': name,
                        'affiliation': affiliation,
                        'source': 'arxiv',
                        'type': 'researcher',
                        'research_areas': [],
                        'paper_count': 0,
                        'papers': []
                    }
                
                researchers[key]['paper_count'] += 1
                if len(researchers[key]['papers']) < 5:
                    researchers[key]['papers'].append({
                        'arxiv_id': paper['arxiv_id'],
                        'title': paper['title'][:100]
                    })
                
                if affiliation and not researchers[key].get('affiliation'):
                    researchers[key]['affiliation'] = affiliation
        
        if paper['authors']:
            papers.append(paper)
    
    return researchers, papers

# Queries to run
queries = [
    "ti:battery+AND+ti:storage",
    "ti:lithium+AND+ti:battery",
    "ti:energy+AND+ti:storage+AND+ti:grid",
    "ti:electrochemical+AND+ti:storage",
    "cat:eess.SY+AND+battery",
    "cat:eess.SY+AND+energy+storage",
    "cat:cond-mat.mtrl-sci+AND+lithium",
    "ti:solid+AND+ti:electrolyte",
    "ti:flow+AND+ti:battery",
    "ti:supercapacitor",
    "ti:sodium+AND+ti:battery",
    "ti:redox+AND+ti:battery",
]

all_researchers = {}
all_papers = []

for i, query in enumerate(queries):
    print(f"[{i+1}/{len(queries)}] Fetching: {query}")
    
    # Fetch multiple pages
    for start in [0, 200, 400]:
        content = fetch_arxiv(query, start=start, max_results=200)
        if content:
            researchers, papers = extract_researchers(content)
            
            for key, data in researchers.items():
                if key in all_researchers:
                    all_researchers[key]['paper_count'] += data['paper_count']
                    all_researchers[key]['papers'].extend(data['papers'])
                    all_researchers[key]['papers'] = all_researchers[key]['papers'][:10]
                else:
                    all_researchers[key] = data
            
            all_papers.extend(papers)
            
            print(f"  Found {len(researchers)} researchers, {len(papers)} papers")
        
        time.sleep(0.5)  # Be nice to arXiv

# Deduplicate papers
seen_ids = set()
unique_papers = []
for paper in all_papers:
    if paper['arxiv_id'] and paper['arxiv_id'] not in seen_ids:
        seen_ids.add(paper['arxiv_id'])
        unique_papers.append(paper)

# Add research areas based on paper titles
for key, data in all_researchers.items():
    areas = set()
    for p in data.get('papers', []):
        title = p.get('title', '').lower()
        if 'lithium' in title:
            areas.add('lithium-ion batteries')
        if 'grid' in title:
            areas.add('grid storage')
        if 'solid' in title and 'electrolyte' in title:
            areas.add('solid-state batteries')
        if 'sodium' in title:
            areas.add('sodium-ion batteries')
        if 'flow' in title:
            areas.add('flow batteries')
        if 'supercapacitor' in title:
            areas.add('supercapacitors')
        if 'degradation' in title:
            areas.add('battery degradation')
        if 'thermal' in title:
            areas.add('thermal management')
    data['research_areas'] = list(areas) if areas else ['energy storage']

# Save results
with open('researchers.jsonl', 'w') as f:
    for key, data in all_researchers.items():
        f.write(json.dumps(data) + '\n')

with open('papers.jsonl', 'w') as f:
    for paper in unique_papers:
        f.write(json.dumps(paper) + '\n')

# Save abstracts
os.makedirs('content/papers', exist_ok=True)
for paper in unique_papers[:200]:
    if paper.get('arxiv_id') and paper.get('abstract'):
        safe_id = paper['arxiv_id'].replace('/', '_')
        with open(f"content/papers/{safe_id}.txt", 'w') as f:
            f.write(f"Title: {paper['title']}\n\n")
            f.write(f"Authors: {', '.join(paper['authors'])}\n\n")
            if paper.get('doi'):
                f.write(f"DOI: {paper['doi']}\n\n")
            f.write(f"Abstract:\n{paper['abstract']}\n")

print(f"\n=== FINAL RESULTS ===")
print(f"Total researchers: {len(all_researchers)}")
print(f"Total unique papers: {len(unique_papers)}")
print(f"Paper abstracts saved: {min(200, len(unique_papers))}")
