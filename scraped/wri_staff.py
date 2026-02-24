#!/usr/bin/env python3
"""Parse WRI staff and add to people.jsonl"""

import json
from pathlib import Path

BASE_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")

staff = [
    {"name": "Ani Dasgupta", "role": "President & CEO"},
    {"name": "Elizabeth Cook", "role": "Executive Vice President for Governance & Development"},
    {"name": "Craig Hanson", "role": "Managing Director, Programs"},
    {"name": "Adriana Lobo", "role": "Managing Director, Global Presence and National Action"},
    {"name": "Wanjira Mathai", "role": "Managing Director, Africa and Global Partnerships"},
    {"name": "Kevin Moss", "role": "Chief Administrative Officer"},
    {"name": "Janet Ranganathan", "role": "Managing Director, Strategy, Learning and Results"},
    {"name": "Melanie Robinson", "role": "Global Climate, Economics and Finance Program Director"},
    {"name": "Pollyana Abreu", "role": "Urban Mobility Analyst"},
    {"name": "Alejandra Achury", "role": "Research Analyst, Electric School Bus Initiative"},
    {"name": "Claudia Adriazola-Steil", "role": "Deputy Director, Global Urban Mobility, and Director, Health & Road Safety"},
    {"name": "Teite Adukeh", "role": "Digital Communications and Marketing Specialist, Ocean Program"},
    {"name": "Bhawna Ahuja", "role": "Manager, Climate Resilience Practice, WRI India"},
    {"name": "Shazabe Akhtar", "role": "Research Analyst, Air Quality"},
]

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

existing = load_existing_people()
people_file = BASE_DIR / "people.jsonl"
added = 0

with open(people_file, 'a') as f:
    for person in staff:
        if person['name'].lower() not in existing:
            entry = {
                "name": person['name'],
                "role": person['role'],
                "company": "World Resources Institute (WRI)",
                "linkedin": None,
                "twitter": None,
                "category": "policy",
                "source": "wri_staff_page",
                "notes": "WRI is a global research organization working on environmental sustainability"
            }
            f.write(json.dumps(entry) + '\n')
            added += 1

print(f"Added {added} staff from WRI")
