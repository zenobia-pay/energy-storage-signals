#!/usr/bin/env python3
"""Add state energy officials and utility executives"""

import json
from pathlib import Path

BASE_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")

# State officials and utility executives
figures = [
    # More utility CEOs
    {"name": "Lynn Good", "role": "CEO", "company": "Duke Energy", "category": "executive"},
    {"name": "Nick Akins", "role": "CEO", "company": "AEP", "category": "executive"},
    {"name": "Thomas Fanning", "role": "Former CEO", "company": "Southern Company", "category": "executive"},
    {"name": "Chris Womack", "role": "CEO", "company": "Southern Company", "category": "executive"},
    {"name": "Maria Pope", "role": "CEO", "company": "Portland General Electric", "category": "executive"},
    {"name": "Jeffrey Lyash", "role": "CEO", "company": "TVA", "category": "executive"},
    {"name": "Geisha Williams", "role": "Former CEO", "company": "PG&E", "category": "executive"},
    {"name": "Bill Johnson", "role": "Former CEO", "company": "PG&E", "category": "executive"},
    {"name": "David Crane", "role": "Former CEO", "company": "NRG Energy", "category": "executive"},
    {"name": "Mauricio Gutierrez", "role": "CEO", "company": "NRG Energy", "category": "executive"},
    {"name": "Ralph Izzo", "role": "Former CEO", "company": "PSEG", "category": "executive"},
    {"name": "Leo Denault", "role": "CEO", "company": "Entergy", "category": "executive"},
    {"name": "Scott Prochazka", "role": "CEO", "company": "CenterPoint Energy", "category": "executive"},
    {"name": "Les Silverman", "role": "CEO", "company": "CenterPoint Energy", "category": "executive"},
    {"name": "Bill Spence", "role": "Former CEO", "company": "PPL", "category": "executive"},
    {"name": "Vincent Sorgi", "role": "CEO", "company": "PPL", "category": "executive"},
    {"name": "Dennis Arriola", "role": "Former CEO", "company": "Avangrid", "category": "executive"},
    {"name": "Pedro Azagra", "role": "CEO", "company": "Avangrid", "category": "executive"},
    {"name": "Ben Fowke", "role": "Former CEO", "company": "Xcel Energy", "category": "executive"},
    {"name": "Bob Frenzel", "role": "CEO", "company": "Xcel Energy", "category": "executive"},
    {"name": "Chris Peel", "role": "CEO", "company": "Xcel Energy (CFO)", "category": "executive"},
    {"name": "Tom Webb", "role": "Former CEO", "company": "DTE Energy", "category": "executive"},
    {"name": "Gerry Anderson", "role": "CEO", "company": "DTE Energy", "category": "executive"},
    {"name": "Jerry Norcia", "role": "CEO", "company": "DTE Energy", "category": "executive"},
    {"name": "Joseph Dominguez", "role": "CEO", "company": "Constellation Energy", "category": "executive"},
    {"name": "Bill Von Hoene", "role": "Chief Strategy Officer", "company": "Exelon", "category": "executive"},
    
    # More state officials
    {"name": "Mary Ann Hitt", "role": "SVP", "company": "Sierra Club", "category": "policy"},
    {"name": "Bruce Nilles", "role": "Founder", "company": "America's Power Plan", "category": "policy"},
    {"name": "David Terry", "role": "Executive Director", "company": "NASEO", "category": "policy"},
    {"name": "Kate Gordon", "role": "Former Director", "company": "California OPR", "category": "policy"},
    {"name": "Ken Alex", "role": "Former Director", "company": "California OPR", "category": "policy"},
    {"name": "Mary Nichols", "role": "Former Chair", "company": "CARB", "category": "policy"},
    {"name": "Liane Randolph", "role": "Chair", "company": "CARB", "category": "policy"},
    {"name": "Alicia Barton", "role": "Former President", "company": "NYSERDA", "category": "policy"},
    {"name": "Gil Quiniones", "role": "CEO", "company": "ComEd", "category": "executive"},
    {"name": "Justin Driscoll", "role": "CEO", "company": "NYPA", "category": "executive"},
    {"name": "Rich Dewey", "role": "CEO", "company": "NYISO", "category": "policy"},
    {"name": "Gordon van Welie", "role": "CEO", "company": "ISO-NE", "category": "policy"},
    {"name": "Pablo Vegas", "role": "CEO", "company": "ERCOT", "category": "policy"},
    {"name": "Craig Jones", "role": "CEO", "company": "MISO", "category": "policy"},
    {"name": "Kevin Gresham", "role": "SVP", "company": "SPP", "category": "policy"},
    
    # NARUC / state PUC leaders
    {"name": "Judith Jagdmann", "role": "President", "company": "NARUC", "category": "policy"},
    {"name": "Greg White", "role": "Executive Director", "company": "NARUC", "category": "policy"},
    {"name": "Rachael Terada", "role": "Staff", "company": "NARUC", "category": "policy"},
    {"name": "Miles Keogh", "role": "Former Director", "company": "NARUC", "category": "policy"},
    
    # Energy NGO leaders
    {"name": "Michael Brune", "role": "Former Executive Director", "company": "Sierra Club", "category": "policy"},
    {"name": "Ben Jealous", "role": "Executive Director", "company": "Sierra Club", "category": "policy"},
    {"name": "John Podesta", "role": "Senior Advisor", "company": "White House (former)", "category": "policy"},
    {"name": "Gina McCarthy", "role": "Former National Climate Advisor", "company": "White House", "category": "policy"},
    {"name": "Ali Zaidi", "role": "National Climate Advisor", "company": "White House", "category": "policy"},
    {"name": "Brenda Mallory", "role": "Chair", "company": "CEQ", "category": "policy"},
    {"name": "Jennifer Granholm", "role": "Secretary", "company": "Department of Energy", "category": "policy"},
    {"name": "Michael Regan", "role": "Administrator", "company": "EPA", "category": "policy"},
    {"name": "Pete Buttigieg", "role": "Secretary", "company": "Department of Transportation", "category": "policy"},
    
    # Clean energy coalitions
    {"name": "Lisa Jacobson", "role": "President", "company": "Business Council for Sustainable Energy", "category": "policy"},
    {"name": "Maria Korsnick", "role": "CEO", "company": "Nuclear Energy Institute", "category": "policy"},
    {"name": "Fred Krupp", "role": "President", "company": "Environmental Defense Fund", "category": "policy"},
    {"name": "Manish Bapna", "role": "President", "company": "NRDC", "category": "policy"},
    {"name": "Kathleen Rogers", "role": "President", "company": "Earthday.org", "category": "policy"},
    
    # More co-op / public power
    {"name": "Jim Matheson", "role": "CEO", "company": "NRECA", "category": "policy"},
    {"name": "Joy Ditto", "role": "CEO", "company": "APPA", "category": "policy"},
    {"name": "Scott Peters", "role": "Director", "company": "LPPC", "category": "policy"},
    
    # State energy office directors
    {"name": "David Terry", "role": "Executive Director", "company": "NASEO", "category": "policy"},
    {"name": "Sandy Fazeli", "role": "Program Manager", "company": "NASEO", "category": "policy"},
    {"name": "Jeffrey Ackermann", "role": "Director", "company": "Colorado CEO", "category": "policy"},
    {"name": "Will Toor", "role": "Director", "company": "Colorado CEO", "category": "policy"},
    
    # Texas energy figures
    {"name": "Peter Lake", "role": "Chairman", "company": "PUCT", "category": "policy"},
    {"name": "DeAnn Walker", "role": "Former Chair", "company": "PUCT", "category": "policy"},
    {"name": "Lori Cobos", "role": "Commissioner", "company": "PUCT", "category": "policy"},
    
    # More cleantech foundations
    {"name": "Wendy Abrams", "role": "Trustee", "company": "Energy Foundation", "category": "investor"},
    {"name": "Eric Heitz", "role": "President", "company": "Energy Foundation", "category": "investor"},
    {"name": "Jason Mark", "role": "Director", "company": "Energy Foundation", "category": "investor"},
    {"name": "Sonia Aggarwal", "role": "Former VP", "company": "Energy Innovation", "category": "policy"},
    
    # IPP executives
    {"name": "Bill Holmberg", "role": "CEO", "company": "EDF Renewables North America", "category": "executive"},
    {"name": "Tristan Grimbert", "role": "CEO", "company": "EDF Renewables North America", "category": "executive"},
    {"name": "Morten Dyrholm", "role": "Group SVP", "company": "Vestas", "category": "executive"},
    {"name": "Henrik Andersen", "role": "CEO", "company": "Vestas", "category": "executive"},
    {"name": "Chris Brown", "role": "CEO", "company": "Vestas Americas", "category": "executive"},
    {"name": "Eduardo Medina", "role": "CEO", "company": "Siemens Gamesa Americas", "category": "executive"},
    {"name": "Jochen Eickholt", "role": "CEO", "company": "Siemens Gamesa", "category": "executive"},
    {"name": "Lars Thinggaard", "role": "CEO", "company": "GE Vernova (former)", "category": "executive"},
    {"name": "Scott Strazik", "role": "CEO", "company": "GE Vernova", "category": "executive"},
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
                "category": person.get('category', 'executive'),
                "source": "manual_state_utility_figures",
                "notes": "Utility executive or state energy official"
            }
            f.write(json.dumps(entry) + '\n')
            added += 1

print(f"Added {added} state/utility figures")
