import re
import json
import sys

def parse_arxiv_xml(content):
    researchers = {}
    papers = []
    
    # Find all entries
    entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)
    
    for entry in entries:
        # Extract paper info
        paper_id = re.search(r'<id>http://arxiv.org/abs/(.*?)</id>', entry)
        title = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
        summary = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
        published = re.search(r'<published>(.*?)</published>', entry)
        doi = re.search(r'<arxiv:doi>(.*?)</arxiv:doi>', entry)
        
        # Skip non-energy storage papers
        title_text = title.group(1).strip().replace('\n', ' ') if title else ""
        skip_keywords = ['Dark Energy', 'globular cluster', 'malaria', 'lithium abundances', 'Lithium in the Universe', 'fermion', 'protostellar']
        if any(kw.lower() in title_text.lower() for kw in skip_keywords):
            continue
            
        paper = {
            'arxiv_id': paper_id.group(1) if paper_id else None,
            'title': title_text,
            'abstract': summary.group(1).strip().replace('\n', ' ')[:500] if summary else None,
            'published': published.group(1) if published else None,
            'doi': doi.group(1) if doi else None,
            'authors': []
        }
        
        # Extract authors
        authors = re.findall(r'<author>\s*<name>(.*?)</name>(?:\s*<arxiv:affiliation>(.*?)</arxiv:affiliation>)?', entry, re.DOTALL)
        for name, affiliation in authors:
            name = name.strip()
            affiliation = affiliation.strip() if affiliation else None
            
            # Skip collaboration names
            if 'Collaboration' in name or 'collaboration' in name:
                continue
                
            paper['authors'].append(name)
            
            # Add to researchers dict
            if name not in researchers:
                researchers[name] = {
                    'name': name,
                    'affiliation': affiliation,
                    'source': 'arxiv',
                    'research_areas': ['energy storage', 'battery'],
                    'papers': [],
                    'paper_count': 0
                }
            researchers[name]['papers'].append(paper['arxiv_id'])
            researchers[name]['paper_count'] += 1
            if affiliation and not researchers[name].get('affiliation'):
                researchers[name]['affiliation'] = affiliation
        
        if paper['authors']:
            papers.append(paper)
    
    return researchers, papers

# Read input files and combine
all_researchers = {}
all_papers = []

for filename in sys.argv[1:]:
    with open(filename, 'r') as f:
        content = f.read()
    researchers, papers = parse_arxiv_xml(content)
    
    for name, data in researchers.items():
        if name in all_researchers:
            all_researchers[name]['papers'].extend(data['papers'])
            all_researchers[name]['paper_count'] += data['paper_count']
        else:
            all_researchers[name] = data
    
    all_papers.extend(papers)

# Write outputs
with open('researchers.jsonl', 'a') as f:
    for name, data in all_researchers.items():
        f.write(json.dumps(data) + '\n')

with open('papers.jsonl', 'a') as f:
    for paper in all_papers:
        f.write(json.dumps(paper) + '\n')

print(f"Extracted {len(all_researchers)} researchers and {len(all_papers)} papers")
