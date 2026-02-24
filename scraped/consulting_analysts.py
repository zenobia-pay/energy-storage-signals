#!/usr/bin/env python3
"""Add more known consulting analysts and industry figures"""

import json
from pathlib import Path

BASE_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")

# Consulting/research analysts across firms
figures = [
    # E3 (Energy and Environmental Economics)
    {"name": "Arne Olson", "role": "Senior Partner", "company": "E3 (Energy and Environmental Economics)", "category": "analyst"},
    {"name": "Nick Schlag", "role": "Managing Director", "company": "E3", "category": "analyst"},
    {"name": "Zach Ming", "role": "Director", "company": "E3", "category": "analyst"},
    {"name": "Amber Mahone", "role": "Managing Director", "company": "E3", "category": "analyst"},
    
    # Synapse Energy
    {"name": "Bruce Biewald", "role": "Co-Founder & CEO", "company": "Synapse Energy Economics", "category": "analyst"},
    {"name": "Jeannie Ramey", "role": "Co-Founder", "company": "Synapse Energy Economics", "category": "analyst"},
    {"name": "Pat Knight", "role": "Senior Associate", "company": "Synapse Energy Economics", "category": "analyst"},
    
    # Rocky Mountain Institute
    {"name": "Jules Kortenhorst", "role": "Former CEO", "company": "RMI", "category": "analyst"},
    {"name": "Jon Creyts", "role": "Managing Director", "company": "RMI", "category": "analyst"},
    {"name": "Leia Guccione", "role": "Principal", "company": "RMI", "category": "analyst"},
    {"name": "James Newcomb", "role": "Managing Director", "company": "RMI", "category": "analyst"},
    {"name": "Titiaan Palazzi", "role": "Principal", "company": "RMI", "category": "analyst"},
    {"name": "Mark Dyson", "role": "Managing Director", "company": "RMI", "category": "analyst"},
    {"name": "Dan Wetzel", "role": "Principal", "company": "RMI", "category": "analyst"},
    
    # Brattle Group
    {"name": "Johannes Pfeifenberger", "role": "Principal", "company": "Brattle Group", "category": "analyst"},
    {"name": "Judy Chang", "role": "Principal", "company": "Brattle Group", "category": "analyst"},
    {"name": "Marc Chupka", "role": "Principal", "company": "Brattle Group", "category": "analyst"},
    {"name": "Frank Graves", "role": "Principal", "company": "Brattle Group", "category": "analyst"},
    {"name": "William Zarakas", "role": "Principal", "company": "Brattle Group", "category": "analyst"},
    
    # ICF
    {"name": "Judah Rose", "role": "Managing Director", "company": "ICF", "category": "analyst"},
    {"name": "Himanshu Pande", "role": "Vice President", "company": "ICF", "category": "analyst"},
    
    # Lazard
    {"name": "George Bilicic", "role": "Global Head Power", "company": "Lazard", "category": "analyst"},
    
    # Guidehouse
    {"name": "Dexter Gauntlett", "role": "Research Director", "company": "Guidehouse Insights", "category": "analyst"},
    {"name": "Brett Simon", "role": "Principal Research Analyst", "company": "Guidehouse", "category": "analyst"},
    
    # IHS Markit / S&P Global Commodity Insights
    {"name": "Dan Yergin", "role": "Vice Chairman", "company": "S&P Global", "category": "analyst"},
    {"name": "Carlos Pascual", "role": "Senior Vice President", "company": "S&P Global", "category": "analyst"},
    
    # NRECA / Co-op analysis
    {"name": "Kirk Johnson", "role": "CEO", "company": "NRECA", "category": "policy"},
    
    # GridLab
    {"name": "Ric O'Connell", "role": "Executive Director", "company": "GridLab", "category": "analyst"},
    
    # Rewiring America
    {"name": "Ari Matusiak", "role": "CEO", "company": "Rewiring America", "category": "policy"},
    {"name": "Emily Levin", "role": "Managing Director", "company": "Rewiring America", "category": "analyst"},
    
    # Lawrence Berkeley National Lab
    {"name": "Ryan Wiser", "role": "Senior Scientist", "company": "Lawrence Berkeley National Lab", "category": "researcher"},
    {"name": "Andrew Mills", "role": "Research Scientist", "company": "Lawrence Berkeley National Lab", "category": "researcher"},
    {"name": "Joachim Seel", "role": "Research Scientist", "company": "Lawrence Berkeley National Lab", "category": "researcher"},
    {"name": "Will Gorman", "role": "Research Scientist", "company": "Lawrence Berkeley National Lab", "category": "researcher"},
    {"name": "Galen Barbose", "role": "Research Scientist", "company": "Lawrence Berkeley National Lab", "category": "researcher"},
    {"name": "Naim Darghouth", "role": "Research Scientist", "company": "Lawrence Berkeley National Lab", "category": "researcher"},
    {"name": "Dev Millstein", "role": "Research Scientist", "company": "Lawrence Berkeley National Lab", "category": "researcher"},
    
    # DOE Office of Electricity
    {"name": "Patricia Hoffman", "role": "Principal Deputy Assistant Secretary", "company": "DOE Office of Electricity", "category": "policy"},
    
    # Princeton ZERO Lab
    {"name": "Eric Larson", "role": "Senior Research Engineer", "company": "Princeton ZERO Lab", "category": "researcher"},
    {"name": "Chris Greig", "role": "Professor", "company": "Princeton University", "category": "researcher"},
    
    # MIT Energy Initiative
    {"name": "Robert Armstrong", "role": "Director", "company": "MIT Energy Initiative", "category": "researcher"},
    {"name": "Howard Herzog", "role": "Senior Research Engineer", "company": "MIT Energy Initiative", "category": "researcher"},
    
    # Stanford
    {"name": "Sally Benson", "role": "Professor", "company": "Stanford University", "category": "researcher"},
    {"name": "John Weyant", "role": "Professor", "company": "Stanford University", "category": "researcher"},
    {"name": "Mark Jacobson", "role": "Professor", "company": "Stanford University", "category": "researcher"},
    
    # Grid integration experts
    {"name": "Erik Ela", "role": "Principal", "company": "EPRI", "category": "researcher"},
    {"name": "Brendan Kirby", "role": "Consultant", "company": "Power System Consulting", "category": "analyst"},
    {"name": "Michael Milligan", "role": "Principal", "company": "NREL (former)", "category": "researcher"},
    {"name": "Paul Denholm", "role": "Senior Research Fellow", "company": "NREL", "category": "researcher"},
    {"name": "Trieu Mai", "role": "Senior Analyst", "company": "NREL", "category": "researcher"},
    {"name": "Wesley Cole", "role": "Senior Analyst", "company": "NREL", "category": "researcher"},
    {"name": "Daniel Steinberg", "role": "Senior Analyst", "company": "NREL", "category": "researcher"},
    {"name": "Aaron Bloom", "role": "Grid Modernization Lead", "company": "NREL", "category": "researcher"},
    
    # Vibrant Clean Energy
    {"name": "Christopher Clack", "role": "CEO", "company": "Vibrant Clean Energy", "category": "analyst"},
    
    # Evolved Energy Research
    {"name": "Benjamin Haley", "role": "Principal", "company": "Evolved Energy Research", "category": "analyst"},
    
    # Moment Energy
    {"name": "Pat Murphy", "role": "CEO", "company": "Moment Energy", "category": "executive"},
    {"name": "Bill Acker", "role": "Executive Director", "company": "NY-BEST", "category": "policy"},
    
    # CESA
    {"name": "Todd Olinsky-Paul", "role": "Senior Project Director", "company": "CESA", "category": "policy"},
    {"name": "Katherine Hamilton", "role": "Chair", "company": "38 North Solutions", "category": "policy"},
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
    for person in figures:
        if person['name'].lower() not in existing:
            entry = {
                "name": person['name'],
                "role": person.get('role'),
                "company": person.get('company'),
                "linkedin": None,
                "twitter": person.get('twitter'),
                "category": person.get('category', 'analyst'),
                "source": "manual_consulting_analysts",
                "notes": "Key energy consultant, researcher, or analyst"
            }
            f.write(json.dumps(entry) + '\n')
            added += 1

print(f"Added {added} consulting analysts and researchers")
