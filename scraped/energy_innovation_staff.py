#!/usr/bin/env python3
"""Parse Energy Innovation staff and add to people.jsonl"""

import json
from pathlib import Path

BASE_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")

staff = [
    {"name": "Hal Harvey", "role": "Founder Emeritus"},
    {"name": "Sonia Aggarwal", "role": "Chief Executive Officer"},
    {"name": "Olivia Ashmoore", "role": "Senior Analyst"},
    {"name": "Lydia Brown", "role": "Communications Associate"},
    {"name": "Emily Bruns", "role": "Research & Modeling Manager"},
    {"name": "Minshu Deng", "role": "Research & Modeling Manager"},
    {"name": "Sonali Deshpande", "role": "Senior Policy Analyst"},
    {"name": "Jenny Edwards", "role": "Director, Philanthropic Analysis"},
    {"name": "Dan Esposito", "role": "Manager, Fuels & Chemicals"},
    {"name": "Christina Fernandes", "role": "Chief Operating Officer"},
    {"name": "Todd Fincannon", "role": "Senior Software Engineer"},
    {"name": "Matthias Fripp", "role": "Director of Global Policy Research"},
    {"name": "Eric Gimon", "role": "Senior Fellow"},
    {"name": "Xiaoxue Hou", "role": "Senior Analyst"},
    {"name": "Hayley Kunkle", "role": "Analyst"},
    {"name": "Clarissa Lopez", "role": "Finance Manager"},
    {"name": "Megan Mahajan", "role": "Senior Manager, Modeling & Analysis"},
    {"name": "Silvio Marcacci", "role": "Senior Director, Communications"},
    {"name": "Fei Meng", "role": "Director, China"},
    {"name": "Mike O'Boyle", "role": "Senior Director, Policy and Strategy"},
    {"name": "Dan O'Brien", "role": "Senior Modeling Analyst"},
    {"name": "Fanuel Oduor", "role": "Head of Finance"},
    {"name": "Robbie Orvis", "role": "Senior Director, Modeling and Analysis"},
    {"name": "Brendan Pierpont", "role": "Director, Electricity"},
    {"name": "Jeffrey Rissman", "role": "Senior Director, Industry"},
    {"name": "Nik Sawe", "role": "Senior Policy Analyst"},
    {"name": "Michelle Solomon", "role": "Manager, Electricity"},
    {"name": "Stephen Stack", "role": "Senior Analyst"},
    {"name": "Shannon Stirone", "role": "Managing Editor"},
    {"name": "Mary Francis Swint", "role": "Analyst"},
    {"name": "Claire Trevisan", "role": "Senior Analyst"},
    {"name": "Xiuli Zhang", "role": "Project Manager, China"},
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
                "company": "Energy Innovation Policy & Technology LLC",
                "linkedin": None,
                "twitter": None,
                "category": "analyst",
                "source": "energy_innovation_staff_page",
                "notes": "Energy Innovation is a policy research organization focused on clean energy analysis"
            }
            f.write(json.dumps(entry) + '\n')
            added += 1

print(f"Added {added} staff from Energy Innovation")
