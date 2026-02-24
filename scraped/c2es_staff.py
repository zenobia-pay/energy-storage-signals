#!/usr/bin/env python3
"""Parse C2ES staff and add to people.jsonl"""

import json
from pathlib import Path

BASE_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")

staff = [
    {"name": "Nat Keohane", "role": "President"},
    {"name": "Francesco Aimone", "role": "Industrial Electrification Senior Fellow"},
    {"name": "Diandra Angiello", "role": "Technology Innovation Policy Associate Fellow"},
    {"name": "Amy Bailey", "role": "Senior Director of Operations"},
    {"name": "Rebecca Berg", "role": "Manager of Corporate Climate Standards Development and Engagement"},
    {"name": "Brock Burton", "role": "Climate and Trade Associate Fellow"},
    {"name": "Tim Carroll", "role": "Senior Press Secretary"},
    {"name": "Rose Luttenberger Caruso", "role": "Director of Advocacy"},
    {"name": "Paige Curtis", "role": "Digital Communications Manager"},
    {"name": "Tiffany Fisher", "role": "Executive Assistant"},
    {"name": "Nicholas Franco", "role": "Director of Corporate Net Zero Transition"},
    {"name": "Stephanie Gagnon-Rodriguez", "role": "Director of Regional Clean Economies"},
    {"name": "Mirela Gavins", "role": "Senior Executive Assistant"},
    {"name": "Alec Gerlach", "role": "Vice President of Communications"},
    {"name": "Kaveh Guilanpour", "role": "Vice President for International Strategies"},
    {"name": "Kristin Gunn", "role": "Development Manager"},
    {"name": "Sophia Haber", "role": "International Associate Fellow"},
    {"name": "John Holler", "role": "Senior Fellow, Low-Carbon Fuels and Transportation"},
    {"name": "Philip Horowitz", "role": "Communications Manager"},
    {"name": "Jennifer Huang", "role": "Director for International Strategies"},
    {"name": "Catalina Cecchi Hucke", "role": "Senior Manager for International Strategies"},
    {"name": "Melissa Hulting", "role": "Director for Industrial Decarbonization"},
    {"name": "Sydney Jerabek", "role": "Operations Manager"},
    {"name": "Chelsea Johnson", "role": "International Fellow"},
    {"name": "Robin Johnson", "role": "Senior Director of Institutional Giving"},
    {"name": "Naila Karamally", "role": "Climate Stewardship and Sustainable Investing Fellow"},
    {"name": "Brian Kelly", "role": "Chief Financial Officer"},
    {"name": "Meredith Keyse", "role": "Senior Director of Major Gifts"},
    {"name": "Eda Kosma", "role": "International Fellow"},
    {"name": "Tess Machi", "role": "Senior Industrial Policy Analyst"},
    {"name": "Sharon McShane", "role": "Senior Institutional Giving Officer"},
    {"name": "James-Christopher Miller", "role": "Director of Finance"},
    {"name": "Jamel Muschette", "role": "Staff Accountant"},
    {"name": "Elizabeth North", "role": "Vice President for Strategy and Development"},
    {"name": "Christa Ogata", "role": "Senior Manager for the Kinetic Coalition"},
    {"name": "Hanna Payne", "role": "Climate Resilience Manager"},
    {"name": "Bob Perciasepe", "role": "Senior Adviser"},
    {"name": "Emily Pope", "role": "Carbon Management Senior Fellow"},
    {"name": "Kira Presley", "role": "Business Engagement Coordinator for Net Zero Pathways"},
    {"name": "Maire Quinn", "role": "Development Associate"},
    {"name": "Verena Radulovic", "role": "Vice President for Business Engagement"},
    {"name": "Rosalie Ruetz", "role": "Business Engagement Associate"},
    {"name": "Riccardo Serbolonghi", "role": "Kinetic Coalition Coordinator"},
    {"name": "Clare Sierawski", "role": "Managing Director of the Kinetic Coalition"},
    {"name": "Brad Townsend", "role": "Vice President for Policy and Outreach"},
    {"name": "Peter Trousdale", "role": "Associate Policy Fellow, Regional Programs"},
    {"name": "Veronica Valerio", "role": "Director for Human Resources"},
    {"name": "Elina Vanuska", "role": "Industrial Decarbonization Fellow"},
    {"name": "Doug Vine", "role": "Director of Energy Analysis"},
    {"name": "Johanna Wassermann", "role": "Innovation Manager"},
    {"name": "Olivia Windorf", "role": "U.S. Policy Fellow"},
    {"name": "Shannon Wood", "role": "Advocacy Manager"},
    {"name": "Jason Ye", "role": "Director for U.S. Policy and Outreach"},
    {"name": "Libby Zemaitis", "role": "Senior Manager for Resilience Programs"},
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
                "company": "Center for Climate and Energy Solutions (C2ES)",
                "linkedin": None,
                "twitter": None,
                "category": "policy",
                "source": "c2es_staff_page",
                "notes": "C2ES is an independent nonprofit working on climate and energy policy"
            }
            f.write(json.dumps(entry) + '\n')
            added += 1

print(f"Added {added} staff from C2ES")
