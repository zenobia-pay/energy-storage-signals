#!/usr/bin/env python3
"""Process arXiv API responses and extract researchers/papers."""
import re
import json
import sys
from datetime import datetime

def parse_arxiv_xml(content):
    """Parse arXiv XML and extract researchers and papers."""
    researchers = {}
    papers = []
    
    # Find all entries
    entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)
    print(f"Found {len(entries)} entries in XML")
    
    # Skip keywords for non-energy-storage papers
    skip_keywords = [
        'Dark Energy', 'globular cluster', 'malaria', 'lithium abundances', 
        'Lithium in the Universe', 'fermion', 'protostellar', 'GRID detector',
        'Gamma-Ray', 'CubeSat', 'quasicrystal', 'cosmological'
    ]
    
    for entry in entries:
        # Extract paper info
        paper_id_match = re.search(r'<id>http://arxiv.org/abs/(.*?)</id>', entry)
        title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
        summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
        published_match = re.search(r'<published>(.*?)</published>', entry)
        doi_match = re.search(r'<arxiv:doi>(.*?)</arxiv:doi>', entry)
        journal_match = re.search(r'<arxiv:journal_ref>(.*?)</arxiv:journal_ref>', entry)
        
        title_text = title_match.group(1).strip().replace('\n', ' ') if title_match else ""
        
        # Skip non-energy storage papers
        if any(kw.lower() in title_text.lower() for kw in skip_keywords):
            continue
            
        paper = {
            'arxiv_id': paper_id_match.group(1) if paper_id_match else None,
            'title': title_text,
            'abstract': summary_match.group(1).strip().replace('\n', ' ')[:1000] if summary_match else None,
            'published': published_match.group(1) if published_match else None,
            'doi': doi_match.group(1) if doi_match else None,
            'journal': journal_match.group(1) if journal_match else None,
            'authors': []
        }
        
        # Extract authors with affiliations
        author_blocks = re.findall(r'<author>(.*?)</author>', entry, re.DOTALL)
        for block in author_blocks:
            name_match = re.search(r'<name>(.*?)</name>', block)
            affil_match = re.search(r'<arxiv:affiliation>(.*?)</arxiv:affiliation>', block)
            
            if name_match:
                name = name_match.group(1).strip()
                affiliation = affil_match.group(1).strip() if affil_match else None
                
                # Skip collaboration names
                if 'Collaboration' in name or 'collaboration' in name:
                    continue
                
                paper['authors'].append(name)
                
                # Create unique key for researcher
                key = name.lower().replace(' ', '_')
                
                if key not in researchers:
                    researchers[key] = {
                        'name': name,
                        'affiliation': affiliation,
                        'source': 'arxiv',
                        'research_areas': ['energy storage', 'battery', 'power systems'],
                        'papers': [],
                        'paper_count': 0,
                        'first_seen': paper['published']
                    }
                
                researchers[key]['papers'].append({
                    'arxiv_id': paper['arxiv_id'],
                    'title': paper['title'][:100],
                    'year': paper['published'][:4] if paper['published'] else None
                })
                researchers[key]['paper_count'] += 1
                
                # Update affiliation if we have a better one
                if affiliation and not researchers[key].get('affiliation'):
                    researchers[key]['affiliation'] = affiliation
        
        if paper['authors']:
            papers.append(paper)
    
    return researchers, papers

def main():
    all_researchers = {}
    all_papers = []
    
    # Read all XML content from stdin or files
    if len(sys.argv) > 1:
        for filename in sys.argv[1:]:
            with open(filename, 'r') as f:
                content = f.read()
            researchers, papers = parse_arxiv_xml(content)
            
            for key, data in researchers.items():
                if key in all_researchers:
                    all_researchers[key]['papers'].extend(data['papers'])
                    all_researchers[key]['paper_count'] += data['paper_count']
                else:
                    all_researchers[key] = data
            
            all_papers.extend(papers)
    else:
        content = sys.stdin.read()
        all_researchers, all_papers = parse_arxiv_xml(content)
    
    # Write outputs
    with open('researchers.jsonl', 'w') as f:
        for key, data in all_researchers.items():
            f.write(json.dumps(data) + '\n')
    
    with open('papers.jsonl', 'w') as f:
        for paper in all_papers:
            f.write(json.dumps(paper) + '\n')
    
    print(f"\n=== EXTRACTION COMPLETE ===")
    print(f"Researchers: {len(all_researchers)}")
    print(f"Papers: {len(all_papers)}")
    
    # Save abstracts to content folder
    import os
    os.makedirs('content/papers', exist_ok=True)
    for paper in all_papers[:100]:  # Save first 100 abstracts
        if paper.get('arxiv_id') and paper.get('abstract'):
            safe_id = paper['arxiv_id'].replace('/', '_')
            with open(f"content/papers/{safe_id}.txt", 'w') as f:
                f.write(f"Title: {paper['title']}\n\n")
                f.write(f"Authors: {', '.join(paper['authors'])}\n\n")
                f.write(f"Abstract:\n{paper['abstract']}\n")
    
    print(f"Saved {min(100, len(all_papers))} paper abstracts to content/papers/")

if __name__ == '__main__':
    main()
