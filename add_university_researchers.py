#!/usr/bin/env python3
"""Add university researchers from scraped pages."""
import json
import os

# Princeton Andlinger Center researchers (from earlier scrape)
princeton_researchers = [
    {"name": "Sigrid Adriaenssens", "affiliation": "Princeton University", "dept": "Civil and Environmental Engineering", "email": "sadriaen@princeton.edu", "research_areas": ["adaptive structural systems", "energy efficiency"]},
    {"name": "Craig Arnold", "affiliation": "Princeton University", "dept": "Mechanical and Aerospace Engineering", "email": "cbarnold@princeton.edu", "research_areas": ["energy storage", "batteries", "materials recycling"]},
    {"name": "Emily A. Carter", "affiliation": "Princeton University", "dept": "Mechanical and Aerospace Engineering", "email": "eac@princeton.edu", "research_areas": ["quantum mechanics", "energy materials", "CO2 utilization"]},
    {"name": "Minjie Chen", "affiliation": "Princeton University", "dept": "Electrical and Computer Engineering", "email": "minjie@princeton.edu", "research_areas": ["power conversion", "energy storage", "smart grid"]},
    {"name": "Ian Bourg", "affiliation": "Princeton University", "dept": "Civil and Environmental Engineering", "email": "bourg@princeton.edu", "research_areas": ["geochemistry", "CO2 sequestration"]},
    {"name": "René Carmona", "affiliation": "Princeton University", "dept": "Operations Research", "email": "rcarmona@princeton.edu", "research_areas": ["energy markets", "emissions markets"]},
]

# CMU energy researchers (from scraped directory)
cmu_researchers = [
    {"name": "Jay Whitacre", "affiliation": "Carnegie Mellon University", "dept": "Materials Science and Engineering", "email": "jwhitacre@cmu.edu", "research_areas": ["energy storage", "lithium-ion batteries", "grid storage"]},
    {"name": "Jay Apt", "affiliation": "Carnegie Mellon University", "dept": "Engineering and Public Policy", "email": "japt@andrew.cmu.edu", "research_areas": ["energy policy", "grid reliability"]},
    {"name": "Venkat Viswanathan", "affiliation": "Carnegie Mellon University", "dept": "Mechanical Engineering", "research_areas": ["batteries", "electrochemical systems", "solid-state batteries"]},
    {"name": "Shawn Litster", "affiliation": "Carnegie Mellon University", "dept": "Mechanical Engineering", "research_areas": ["fuel cells", "electrochemical systems"]},
    {"name": "Guannan He", "affiliation": "Carnegie Mellon University", "research_areas": ["battery storage", "power systems"]},
    {"name": "Soummya Kar", "affiliation": "Carnegie Mellon University", "dept": "Electrical and Computer Engineering", "research_areas": ["distributed systems", "smart grid"]},
]

# Stanford Precourt researchers
stanford_researchers = [
    {"name": "Yi Cui", "affiliation": "Stanford University", "dept": "Materials Science", "research_areas": ["batteries", "nanomaterials", "energy storage"]},
    {"name": "William Chueh", "affiliation": "Stanford University", "dept": "Materials Science", "research_areas": ["electrochemistry", "batteries", "fuel cells"]},
    {"name": "Ram Rajagopal", "affiliation": "Stanford University", "dept": "Civil Engineering", "research_areas": ["energy systems", "machine learning", "power systems"]},
    {"name": "Simona Onori", "affiliation": "Stanford University", "research_areas": ["battery management", "state estimation"]},
]

# MIT researchers
mit_researchers = [
    {"name": "Yet-Ming Chiang", "affiliation": "MIT", "dept": "Materials Science", "research_areas": ["batteries", "electrochemistry"]},
    {"name": "Yang Shao-Horn", "affiliation": "MIT", "dept": "Mechanical Engineering", "research_areas": ["electrochemistry", "batteries", "fuel cells"]},
    {"name": "Jessika Trancik", "affiliation": "MIT", "research_areas": ["energy systems", "technology policy"]},
]

# NREL/DOE researchers  
nrel_researchers = [
    {"name": "Ahmad Pesaran", "affiliation": "NREL", "research_areas": ["battery thermal management", "energy storage"]},
    {"name": "Kandler Smith", "affiliation": "NREL", "research_areas": ["battery modeling", "degradation"]},
    {"name": "Paul Denholm", "affiliation": "NREL", "research_areas": ["grid integration", "energy storage"]},
]

# Berkeley researchers
berkeley_researchers = [
    {"name": "Gerbrand Ceder", "affiliation": "UC Berkeley / LBNL", "research_areas": ["battery materials", "computational materials"]},
    {"name": "Bryan McCloskey", "affiliation": "UC Berkeley", "research_areas": ["electrochemistry", "batteries"]},
]

all_university_researchers = (
    princeton_researchers + 
    cmu_researchers + 
    stanford_researchers + 
    mit_researchers + 
    nrel_researchers +
    berkeley_researchers
)

# Load existing to avoid duplicates
existing = set()
if os.path.exists('researchers.jsonl'):
    with open('researchers.jsonl', 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                existing.add(data.get('name', '').lower())
            except:
                pass

print(f"Existing researchers: {len(existing)}")

# Add new researchers
added = 0
with open('researchers.jsonl', 'a') as f:
    for r in all_university_researchers:
        if r['name'].lower() not in existing:
            r['source'] = 'university_directory'
            r['type'] = 'faculty'
            f.write(json.dumps(r) + '\n')
            existing.add(r['name'].lower())
            added += 1

print(f"Added {added} university researchers")
print(f"Total now: {len(existing)}")
