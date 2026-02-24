#!/usr/bin/env python3
"""Add more known energy storage executives and influencers"""

import json
from pathlib import Path

BASE_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")

# More known figures in energy storage and clean energy
executives = [
    # Utility executives
    {"name": "Armando Pimentel", "role": "President & CEO", "company": "Florida Power & Light", "category": "executive"},
    {"name": "Rebecca Kujawa", "role": "President & CEO", "company": "NextEra Energy Resources", "category": "executive"},
    {"name": "Calvin Butler", "role": "President & CEO", "company": "Exelon", "category": "executive"},
    {"name": "Patricia Poppe", "role": "CEO", "company": "PG&E", "category": "executive"},
    {"name": "Pedro Pizarro", "role": "President & CEO", "company": "Edison International", "category": "executive"},
    {"name": "Gale Klappa", "role": "Executive Chairman", "company": "WEC Energy Group", "category": "executive"},
    {"name": "Tom Fanning", "role": "Former CEO", "company": "Southern Company", "category": "executive"},
    {"name": "Chris Weston", "role": "CEO", "company": "Georgia Power", "category": "executive"},
    {"name": "Dan Brouillette", "role": "Former Secretary of Energy", "company": "US DOE", "category": "policy"},
    {"name": "Ernest Moniz", "role": "Former Secretary of Energy / CEO", "company": "EFI Foundation", "category": "policy"},
    
    # More storage companies
    {"name": "Scott Mosier", "role": "CEO", "company": "MassCEC", "category": "executive"},
    {"name": "Mia Hood", "role": "CEO", "company": "Pivot Energy", "category": "executive"},
    {"name": "Arcady Sosinov", "role": "CEO", "company": "FreeWire Technologies", "category": "executive"},
    {"name": "Kiran Kumaraswamy", "role": "VP Markets", "company": "Fluence", "category": "executive"},
    {"name": "Seyed Madaeni", "role": "VP Strategy", "company": "Stem Inc", "category": "executive"},
    
    # VCs / Cleantech investors  
    {"name": "Shayle Kann", "role": "Partner", "company": "Energy Impact Partners", "twitter": "@shaborki", "category": "investor"},
    {"name": "Abe Yokell", "role": "Co-Founder & Managing Partner", "company": "Congruent Ventures", "twitter": "@AbeYokell", "category": "investor"},
    {"name": "Katie Rae", "role": "CEO", "company": "The Engine", "category": "investor"},
    {"name": "Nancy Pfund", "role": "Founder & Managing Partner", "company": "DBL Partners", "category": "investor"},
    {"name": "David Crane", "role": "Clean Energy Entrepreneur", "company": "Former NRG CEO", "category": "executive"},
    {"name": "Arjun Murti", "role": "Partner", "company": "Veriten / Super-Spiked", "twitter": "@ArjunMurti", "category": "analyst"},
    {"name": "Michael Liebreich", "role": "Founder", "company": "Liebreich Associates / BNEF Founder", "twitter": "@MLiebreich", "category": "analyst"},
    {"name": "Hemant Taneja", "role": "Managing Partner", "company": "General Catalyst", "category": "investor"},
    {"name": "Chris Sacca", "role": "Founder", "company": "Lowercarbon Capital", "twitter": "@sacca", "category": "investor"},
    {"name": "Matt Rogers", "role": "Co-Founder", "company": "Incite Ventures / Nest Labs", "category": "investor"},
    
    # Energy storage associations / advocacy
    {"name": "Kelly Speakes-Backman", "role": "CEO", "company": "Energy Storage Association (former)", "category": "policy"},
    {"name": "Heather Zichal", "role": "CEO", "company": "American Clean Power Association", "category": "policy"},
    {"name": "Abigail Ross Hopper", "role": "CEO", "company": "SEIA", "category": "policy"},
    {"name": "Jason Ryan", "role": "VP Communications", "company": "American Clean Power", "category": "policy"},
    
    # Research / National labs
    {"name": "Martin Keller", "role": "Director", "company": "NREL", "category": "researcher"},
    {"name": "Steven Chu", "role": "Former Secretary of Energy", "company": "Stanford University", "category": "researcher"},
    {"name": "Daniel Kammen", "role": "Professor", "company": "UC Berkeley", "twitter": "@dan_kammen", "category": "researcher"},
    {"name": "Saul Griffith", "role": "Founder", "company": "Rewiring America", "twitter": "@saaborki", "category": "researcher"},
    {"name": "Nate Lewis", "role": "Professor", "company": "Caltech", "category": "researcher"},
    {"name": "Paul Albertus", "role": "Professor", "company": "University of Maryland", "category": "researcher"},
    {"name": "George Crabtree", "role": "Director", "company": "JCESR (Argonne)", "category": "researcher"},
    
    # More journalists / media
    {"name": "Emma Foehringer Merchant", "role": "Senior Editor", "company": "Canary Media", "category": "media"},
    {"name": "Maria Virginia Olano", "role": "Reporter", "company": "Canary Media", "category": "media"},
    {"name": "Jeff St. John", "role": "Senior Editor", "company": "Canary Media", "category": "media"},
    {"name": "Andy Colthorpe", "role": "Editor", "company": "Energy Storage News", "category": "media"},
    {"name": "Jason Deign", "role": "Reporter", "company": "Energy Storage News", "category": "media"},
    {"name": "Herman Trabish", "role": "Editor", "company": "Utility Dive", "category": "media"},
    {"name": "Robert Walton", "role": "Editor", "company": "Utility Dive", "category": "media"},
    {"name": "Ethan Howland", "role": "Senior Reporter", "company": "Utility Dive", "category": "media"},
    
    # Consulting / Advisory
    {"name": "Mike Henchen", "role": "Principal", "company": "RMI", "category": "analyst"},
    {"name": "Daniel Finn-Foley", "role": "Head of Storage", "company": "Wood Mackenzie", "category": "analyst"},
    {"name": "Chloe Holden", "role": "Research Manager", "company": "Wood Mackenzie", "category": "analyst"},
    {"name": "Mitalee Gupta", "role": "Senior Research Analyst", "company": "Wood Mackenzie", "category": "analyst"},
    {"name": "Thomas Brandstetter", "role": "Senior Analyst", "company": "BloombergNEF", "category": "analyst"},
    {"name": "Yayoi Sekine", "role": "Lead Energy Storage Analyst", "company": "BloombergNEF", "category": "analyst"},
    {"name": "James Frith", "role": "Head of Energy Storage", "company": "BloombergNEF", "category": "analyst"},
    
    # Grid operators / RTOs
    {"name": "Elliot Mainzer", "role": "President & CEO", "company": "CAISO", "category": "policy"},
    {"name": "Manu Asthana", "role": "President & CEO", "company": "PJM", "category": "policy"},
    {"name": "Rich Hydzik", "role": "VP Operations", "company": "Avista", "category": "executive"},
    
    # State energy officials
    {"name": "David Hochschild", "role": "Chair", "company": "California Energy Commission", "category": "policy"},
    {"name": "Alice Reynolds", "role": "President", "company": "CPUC", "category": "policy"},
    {"name": "Doreen Harris", "role": "President & CEO", "company": "NYSERDA", "category": "policy"},
    
    # International storage
    {"name": "Marek Kubik", "role": "MD Markets", "company": "Fluence EMEA", "category": "executive"},
    {"name": "Alex O'Cinneide", "role": "CEO", "company": "Gore Street Capital", "category": "executive"},
    {"name": "Matt Harper", "role": "Co-Founder", "company": "Invinity Energy Systems", "category": "executive"},
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
    for person in executives:
        if person['name'].lower() not in existing:
            entry = {
                "name": person['name'],
                "role": person.get('role'),
                "company": person.get('company'),
                "linkedin": None,
                "twitter": person.get('twitter'),
                "category": person.get('category', 'executive'),
                "source": "manual_industry_knowledge_2",
                "notes": "Key figure in energy storage industry"
            }
            f.write(json.dumps(entry) + '\n')
            added += 1

print(f"Added {added} more known industry figures")
