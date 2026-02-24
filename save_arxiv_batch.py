#!/usr/bin/env python3
"""Save raw arXiv data and extract researchers."""
import re
import json
import os
from datetime import datetime

# All the XML content we collected (simplified extraction)
xml_content = """
""" # Will be populated by heredoc

def extract_from_xml(content):
    """Extract authors from arXiv XML."""
    researchers = {}
    papers = []
    
    # Skip non-energy storage papers  
    skip_keywords = [
        'Dark Energy', 'globular cluster', 'malaria', 'lithium abundances', 
        'Lithium in the Universe', 'fermion', 'protostellar', 'GRID detector',
        'Gamma-Ray', 'CubeSat', 'quasicrystal', 'cosmological', 'muonic', 'solvated in helium'
    ]
    
    entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)
    
    for entry in entries:
        paper_id_match = re.search(r'<id>http://arxiv.org/abs/(.*?)</id>', entry)
        title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
        published_match = re.search(r'<published>(.*?)</published>', entry)
        doi_match = re.search(r'<arxiv:doi>(.*?)</arxiv:doi>', entry)
        
        title_text = title_match.group(1).strip().replace('\n', ' ') if title_match else ""
        
        # Skip non-energy storage papers
        if any(kw.lower() in title_text.lower() for kw in skip_keywords):
            continue
            
        paper = {
            'arxiv_id': paper_id_match.group(1) if paper_id_match else None,
            'title': title_text,
            'published': published_match.group(1) if published_match else None,
            'doi': doi_match.group(1) if doi_match else None,
            'authors': []
        }
        
        # Extract authors
        author_blocks = re.findall(r'<author>(.*?)</author>', entry, re.DOTALL)
        for block in author_blocks:
            name_match = re.search(r'<name>(.*?)</name>', block)
            affil_match = re.search(r'<arxiv:affiliation>(.*?)</arxiv:affiliation>', block)
            
            if name_match:
                name = name_match.group(1).strip()
                affiliation = affil_match.group(1).strip() if affil_match else None
                
                if 'Collaboration' in name:
                    continue
                
                paper['authors'].append(name)
                key = name.lower().replace(' ', '_').replace('.', '')
                
                if key not in researchers:
                    researchers[key] = {
                        'name': name,
                        'affiliation': affiliation,
                        'source': 'arxiv',
                        'type': 'researcher',
                        'research_areas': ['energy storage', 'battery'],
                        'paper_count': 0,
                        'papers': []
                    }
                
                researchers[key]['paper_count'] += 1
                if len(researchers[key]['papers']) < 10:  # Keep top 10 papers
                    researchers[key]['papers'].append({
                        'arxiv_id': paper['arxiv_id'],
                        'title': paper['title'][:150]
                    })
                
                if affiliation and not researchers[key].get('affiliation'):
                    researchers[key]['affiliation'] = affiliation
        
        if paper['authors']:
            papers.append(paper)
    
    return researchers, papers

# Read existing data if any
existing_researchers = set()
if os.path.exists('researchers.jsonl'):
    with open('researchers.jsonl', 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                existing_researchers.add(data.get('name', '').lower())
            except:
                pass

print(f"Existing researchers: {len(existing_researchers)}")

# Process arXiv API directly from stdin
import sys
content = sys.stdin.read()
researchers, papers = extract_from_xml(content)

# Append new researchers
new_count = 0
with open('researchers.jsonl', 'a') as f:
    for key, data in researchers.items():
        if data['name'].lower() not in existing_researchers:
            f.write(json.dumps(data) + '\n')
            existing_researchers.add(data['name'].lower())
            new_count += 1

# Append papers
with open('papers.jsonl', 'a') as f:
    for paper in papers:
        f.write(json.dumps(paper) + '\n')

print(f"Added {new_count} new researchers, {len(papers)} papers")
print(f"Total researchers now: {len(existing_researchers)}")
