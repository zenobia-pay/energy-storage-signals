#!/usr/bin/env python3
"""Parse Clean Air Council staff and add to people.jsonl"""

import json
from pathlib import Path

BASE_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")

staff = [
    {"name": "Alex Bomstein", "role": "Executive Director"},
    {"name": "Eric Cheung", "role": "Director of Finance and Administration"},
    {"name": "Katie Edwards", "role": "Communications Director"},
    {"name": "Larry Hafetz", "role": "Legal Director"},
    {"name": "Kathryn Urbanowicz", "role": "Deputy Director"},
    {"name": "Nick Zuwiala-Rogers", "role": "Development Director"},
    {"name": "Eleanor Breslin", "role": "Senior Attorney"},
    {"name": "Annie Fox", "role": "Staff Attorney"},
    {"name": "Sarah Gordon", "role": "Staff Attorney"},
    {"name": "Sean Hoffmann", "role": "Legislative Attorney"},
    {"name": "Lauren Otero", "role": "Staff Attorney"},
    {"name": "Liz Green Schultz", "role": "Political Director"},
    {"name": "Logan Welde", "role": "Senior Attorney"},
    {"name": "Echo Alford", "role": "Delaware County Advocacy Coordinator"},
    {"name": "Alyssa Felix-Arreola", "role": "Delaware County Outreach Coordinator"},
    {"name": "Terrie Baumgardner", "role": "Outreach Coordinator"},
    {"name": "Lois Bower-Bjornson", "role": "Outreach Coordinator"},
    {"name": "Joanne Douglas", "role": "Sustainable Transportation Program Coordinator"},
    {"name": "Will Fraser", "role": "Watersheds/Trails Program Manager"},
    {"name": "Sally Hecht", "role": "Sustainable Transportation Program Coordinator"},
    {"name": "Jendaiya Hill", "role": "Philadelphia Community Organizer"},
    {"name": "Nate Johnson", "role": "Engineer"},
    {"name": "Karl Koerner", "role": "Engineer II"},
    {"name": "John Lee", "role": "Air Quality and Public Health Programs Manager"},
    {"name": "Mani Lewis-Norelle", "role": "Trails Coordinator"},
    {"name": "Alice Lu", "role": "Policy Analyst"},
    {"name": "Titania Markland", "role": "Sustainable Transportation Program Manager"},
    {"name": "Larisa Mednis", "role": "Advocacy Coordinator"},
    {"name": "Eve S. Miari", "role": "Director of Programs"},
    {"name": "Marley Myers", "role": "Trails Outreach Coordinator"},
    {"name": "Alexis Oltmer-Bergmann", "role": "Advocacy Coordinator"},
    {"name": "Tom Pike", "role": "Director of Campaigns"},
    {"name": "Jay Ting Walker", "role": "Community Organizer"},
    {"name": "Emily Wildman", "role": "Legislative Advocate"},
    {"name": "Russell Zerbo", "role": "Advocate"},
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
                "company": "Clean Air Council",
                "linkedin": None,
                "twitter": None,
                "category": "policy",
                "source": "cleanair_council_staff_page",
                "notes": "Clean Air Council is an environmental advocacy organization focused on air quality and transportation"
            }
            f.write(json.dumps(entry) + '\n')
            added += 1

print(f"Added {added} staff from Clean Air Council")
