#!/usr/bin/env python3
"""Final large batch of energy storage and clean energy figures"""

import json
from pathlib import Path

BASE_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")

figures = [
    # More academic researchers
    {"name": "Jeremiah Johnson", "role": "Professor", "company": "NC State", "category": "researcher"},
    {"name": "Inês Azevedo", "role": "Professor", "company": "Stanford", "category": "researcher"},
    {"name": "Michael Greenstone", "role": "Professor", "company": "University of Chicago", "category": "researcher"},
    {"name": "Catherine Wolfram", "role": "Professor", "company": "MIT / UC Berkeley", "category": "researcher"},
    {"name": "Meredith Fowlie", "role": "Professor", "company": "UC Berkeley", "category": "researcher"},
    {"name": "Lucas Davis", "role": "Professor", "company": "UC Berkeley", "category": "researcher"},
    {"name": "James Bushnell", "role": "Professor", "company": "UC Davis", "category": "researcher"},
    {"name": "Frank Wolak", "role": "Professor", "company": "Stanford", "category": "researcher"},
    {"name": "James Sweeney", "role": "Professor", "company": "Stanford", "category": "researcher"},
    {"name": "Maximilian Auffhammer", "role": "Professor", "company": "UC Berkeley", "category": "researcher"},
    {"name": "Mar Reguant", "role": "Professor", "company": "Northwestern", "category": "researcher"},
    {"name": "Joseph Shapiro", "role": "Professor", "company": "UC Berkeley", "category": "researcher"},
    {"name": "Josh Graff Zivin", "role": "Professor", "company": "UC San Diego", "category": "researcher"},
    {"name": "Matthew Kahn", "role": "Professor", "company": "USC", "category": "researcher"},
    {"name": "Kenneth Gillingham", "role": "Professor", "company": "Yale", "category": "researcher"},
    {"name": "Erin Mansur", "role": "Professor", "company": "Dartmouth", "category": "researcher"},
    {"name": "Matt Kotchen", "role": "Professor", "company": "Yale", "category": "researcher"},
    {"name": "Tony Reames", "role": "Professor", "company": "University of Michigan", "category": "researcher"},
    {"name": "Destenie Nock", "role": "Professor", "company": "Carnegie Mellon", "category": "researcher"},
    {"name": "Jay Apt", "role": "Professor", "company": "Carnegie Mellon", "category": "researcher"},
    {"name": "Granger Morgan", "role": "Professor", "company": "Carnegie Mellon", "category": "researcher"},
    {"name": "Paulina Jaramillo", "role": "Professor", "company": "Carnegie Mellon", "category": "researcher"},
    {"name": "Costa Samaras", "role": "Professor", "company": "Carnegie Mellon", "category": "researcher"},
    {"name": "Michael Wara", "role": "Director", "company": "Stanford Woods Institute", "category": "researcher"},
    {"name": "Dan Reicher", "role": "Senior Scholar", "company": "Stanford", "category": "researcher"},
    {"name": "Arun Majumdar", "role": "Professor", "company": "Stanford", "category": "researcher"},
    {"name": "Dan Kammen", "role": "Professor", "company": "UC Berkeley", "category": "researcher"},
    {"name": "Alexandra von Meier", "role": "Research Scientist", "company": "UC Berkeley", "category": "researcher"},
    {"name": "Scott Moura", "role": "Professor", "company": "UC Berkeley", "category": "researcher"},
    {"name": "Gireesh Shrimali", "role": "Professor", "company": "Stanford", "category": "researcher"},
    
    # More state-level policy folks
    {"name": "Angie O'Connor", "role": "Commissioner", "company": "Mass DPU", "category": "policy"},
    {"name": "Matthew Nelson", "role": "Chair", "company": "Mass DPU", "category": "policy"},
    {"name": "Patricia Ackerman", "role": "Commissioner", "company": "NJ BPU", "category": "policy"},
    {"name": "Joseph Fiordaliso", "role": "President", "company": "NJ BPU", "category": "policy"},
    {"name": "Christine Guhl-Sadovy", "role": "Commissioner", "company": "NJ BPU", "category": "policy"},
    {"name": "Upendra Chivukula", "role": "Commissioner", "company": "NJ BPU", "category": "policy"},
    {"name": "Diane Burman", "role": "Commissioner", "company": "NY PSC", "category": "policy"},
    {"name": "Rory Christian", "role": "Chair", "company": "NY PSC", "category": "policy"},
    {"name": "Saul Lopes", "role": "Commissioner", "company": "Hawaii PUC", "category": "policy"},
    {"name": "Leo Asuncion", "role": "Commissioner", "company": "Hawaii PUC", "category": "policy"},
    {"name": "Leodoro Quilala", "role": "Chair", "company": "Hawaii PUC", "category": "policy"},
    {"name": "Michael Peevey", "role": "Former President", "company": "CPUC", "category": "policy"},
    {"name": "Loretta Lynch", "role": "Former President", "company": "CPUC", "category": "policy"},
    
    # More electric cooperative and municipal utility folks
    {"name": "Kody Kirkland", "role": "VP", "company": "NRECA", "category": "policy"},
    {"name": "Lauren Khair", "role": "Director", "company": "NRECA", "category": "policy"},
    {"name": "Wes Kelley", "role": "VP", "company": "NRECA", "category": "policy"},
    {"name": "Steve Chriss", "role": "Director", "company": "Walmart Energy", "category": "executive"},
    {"name": "Ron Okel", "role": "Director", "company": "SMUD", "category": "executive"},
    {"name": "Arlen Orchard", "role": "CEO", "company": "SMUD", "category": "executive"},
    {"name": "Paul Lau", "role": "CEO", "company": "SMUD", "category": "executive"},
    {"name": "David Wright", "role": "CEO", "company": "SCPPA", "category": "executive"},
    {"name": "Bill Carnahan", "role": "Director", "company": "NCPA", "category": "executive"},
    {"name": "Randy Howard", "role": "General Manager", "company": "NCPA", "category": "executive"},
    
    # More EV infrastructure
    {"name": "Sarah Derdowski", "role": "CEO", "company": "EVBox", "category": "executive"},
    {"name": "Kristof Vereenooghe", "role": "CEO", "company": "EVBox", "category": "executive"},
    {"name": "Ryan Citron", "role": "Research Director", "company": "Guidehouse", "category": "analyst"},
    {"name": "Michael Austin", "role": "Director", "company": "Guidehouse", "category": "analyst"},
    {"name": "Anthony Eggert", "role": "CEO", "company": "CALSTART (former)", "category": "policy"},
    {"name": "John Boesel", "role": "President", "company": "CALSTART", "category": "policy"},
    {"name": "Gabe Klein", "role": "Executive Director", "company": "Joint Office of Energy & Transportation", "category": "policy"},
    {"name": "Stephanie Pollack", "role": "Deputy Administrator", "company": "FHWA", "category": "policy"},
    
    # More energy efficiency
    {"name": "Steven Nadel", "role": "Executive Director", "company": "ACEEE", "category": "policy"},
    {"name": "Maggie Molina", "role": "Director", "company": "ACEEE", "category": "policy"},
    {"name": "Sara Baldwin", "role": "Director", "company": "ACEEE", "category": "policy"},
    {"name": "Brian Castelli", "role": "EVP", "company": "Alliance to Save Energy", "category": "policy"},
    {"name": "Jason Hartke", "role": "President", "company": "Alliance to Save Energy", "category": "policy"},
    {"name": "Clay Nesler", "role": "VP", "company": "Johnson Controls", "category": "executive"},
    {"name": "Katie McGinty", "role": "VP", "company": "Johnson Controls", "category": "executive"},
    
    # More building decarbonization
    {"name": "Erin Callahan", "role": "Director", "company": "NEEP", "category": "policy"},
    {"name": "Jeremy McDiarmid", "role": "Managing Director", "company": "NEEP", "category": "policy"},
    {"name": "Amy Turner", "role": "Director", "company": "Columbia SIPA", "category": "researcher"},
    {"name": "Constantine Samaras", "role": "Director", "company": "Carnegie Mellon", "category": "researcher"},
    {"name": "Jonathan Koomey", "role": "Research Fellow", "company": "Stanford", "category": "researcher"},
    {"name": "Peter Senge", "role": "Senior Lecturer", "company": "MIT", "category": "researcher"},
    {"name": "John Sterman", "role": "Professor", "company": "MIT", "category": "researcher"},
    {"name": "Karen Ehrhardt-Martinez", "role": "Director", "company": "ACEEE", "category": "researcher"},
    {"name": "Rachel Gold", "role": "Director", "company": "ACEEE", "category": "analyst"},
    
    # More climate finance
    {"name": "Rhian-Mari Thomas", "role": "CEO", "company": "Green Finance Institute", "category": "investor"},
    {"name": "Sagarika Chatterjee", "role": "Director", "company": "PRI", "category": "investor"},
    {"name": "Fiona Reynolds", "role": "Former CEO", "company": "PRI", "category": "investor"},
    {"name": "David Atkin", "role": "CEO", "company": "PRI", "category": "investor"},
    {"name": "Mindy Lubber", "role": "CEO", "company": "Ceres", "category": "policy"},
    {"name": "Steven Rothstein", "role": "Managing Director", "company": "Ceres", "category": "policy"},
    {"name": "Kirsten Snow Spalding", "role": "VP", "company": "Ceres", "category": "policy"},
    {"name": "Anne Kelly", "role": "VP", "company": "Ceres", "category": "policy"},
    {"name": "Andrew Logan", "role": "Director", "company": "Ceres", "category": "policy"},
    {"name": "Jenny McColloch", "role": "Chief Sustainability Officer", "company": "McDonald's", "category": "executive"},
    {"name": "Jessica Long", "role": "Managing Director", "company": "Accenture", "category": "analyst"},
    {"name": "Kara Hurst", "role": "VP Sustainability", "company": "Amazon", "category": "executive"},
    {"name": "Dara O'Rourke", "role": "Co-Founder", "company": "Good Guide / UC Berkeley", "category": "researcher"},
    
    # More emerging tech / innovation
    {"name": "Chad Holliday", "role": "Chair", "company": "Royal Dutch Shell (former)", "category": "executive"},
    {"name": "Julio Friedmann", "role": "Chief Scientist", "company": "Carbon Direct", "category": "researcher"},
    {"name": "Noah Deich", "role": "President", "company": "Carbon180", "category": "policy"},
    {"name": "Erin Burns", "role": "Executive Director", "company": "Carbon180", "category": "policy"},
    {"name": "Giana Amador", "role": "Co-Founder", "company": "Carbon180", "category": "policy"},
    {"name": "Matt Rogers", "role": "Co-Founder", "company": "Mission Possible Partnership", "category": "analyst"},
    {"name": "Zach Bogue", "role": "Partner", "company": "DCVC", "category": "investor"},
    {"name": "Matt Ocko", "role": "Partner", "company": "DCVC", "category": "investor"},
    {"name": "Carmichael Roberts", "role": "Founding Partner", "company": "Material Impact", "category": "investor"},
    {"name": "Yet-Ming Chiang", "role": "Professor", "company": "MIT", "category": "researcher"},
    {"name": "Donald Sadoway", "role": "Professor", "company": "MIT", "category": "researcher"},
    {"name": "Angela Belcher", "role": "Professor", "company": "MIT", "category": "researcher"},
    {"name": "Paula Hammond", "role": "Professor", "company": "MIT", "category": "researcher"},
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
                "source": "manual_final_batch_1",
                "notes": "Energy storage / clean energy industry figure"
            }
            f.write(json.dumps(entry) + '\n')
            added += 1

print(f"Added {added} figures from final batch 1")
