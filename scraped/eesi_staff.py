#!/usr/bin/env python3
"""Parse EESI staff and add to people.jsonl"""

import json
from pathlib import Path

BASE_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")

staff = [
    {"name": "Daniel Bresette", "role": "President", "linkedin": "https://www.linkedin.com/in/daniel-bresette-37993b5/"},
    {"name": "Thomas Beach", "role": "Senior Communications Fellow", "linkedin": "https://www.linkedin.com/in/thomas-beach/"},
    {"name": "Nibret Daba", "role": "Salesforce Administrator", "linkedin": "https://www.linkedin.com/in/nibretdaba/"},
    {"name": "Alison Davis", "role": "Communications Manager", "linkedin": "http://linkedin.com/in/alisonldavis"},
    {"name": "Laura Gries", "role": "Policy Associate", "linkedin": "https://www.linkedin.com/in/laura-gries/"},
    {"name": "Jonathan Herz", "role": "Senior Policy Fellow", "linkedin": "https://www.linkedin.com/in/jonathan-herz-faia-leed-ap-215a9314/"},
    {"name": "Amaury Laporte", "role": "Vice President of Communications", "linkedin": "http://www.linkedin.com/in/amaurylaporte"},
    {"name": "Ulrich Lindqvist", "role": "Finance and Operations Manager", "linkedin": "https://www.linkedin.com/in/ulrich-lindqvist-3b8409200/"},
    {"name": "Anna McGinn", "role": "Policy Director", "linkedin": "https://www.linkedin.com/in/anna-mcginn"},
    {"name": "Daniel O'Brien", "role": "Program Manager", "linkedin": "https://www.linkedin.com/in/daniel-anthony-john-o-brien-69461642/"},
    {"name": "Jeff Overton", "role": "Senior Policy Fellow", "linkedin": "https://www.linkedin.com/in/jeff-overton-443813122/"},
    {"name": "Nicole Pouy", "role": "Senior Policy Associate", "linkedin": "https://www.linkedin.com/in/nicole-p-6005907a/"},
    {"name": "David Robison", "role": "Vice President of Finance", "linkedin": "http://www.linkedin.com/pub/david-robison-mba/0/b05/b87"},
    {"name": "Tim Slattery", "role": "Partnerships Manager", "linkedin": "https://www.linkedin.com/in/tim-slattery-51b67659/"},
    {"name": "Susan Williams", "role": "Vice President of Partnerships", "linkedin": "http://www.linkedin.com/in/susanzwillliams"},
    {"name": "Hannah Wilson-Black", "role": "Communications Associate", "linkedin": "https://www.linkedin.com/in/hannah-wilson-black-515560199/"},
    {"name": "Miguel Yañez-Barnuevo", "role": "Project Manager", "linkedin": "https://www.linkedin.com/in/miguel-ya%C3%B1ez-barnuevo-he-his-b063998/"},
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
                "company": "Environmental and Energy Study Institute (EESI)",
                "linkedin": person['linkedin'],
                "twitter": None,
                "category": "policy",
                "source": "eesi_staff_page",
                "notes": "EESI is a non-profit education and policy organization focused on environmental and energy issues"
            }
            f.write(json.dumps(entry) + '\n')
            added += 1

print(f"Added {added} staff from EESI")
