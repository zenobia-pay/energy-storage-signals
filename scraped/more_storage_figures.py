#!/usr/bin/env python3
"""Add more storage industry figures"""

import json
from pathlib import Path

BASE_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")

# More storage-specific figures
figures = [
    # More battery startups
    {"name": "Amir Rozwadowski", "role": "CEO", "company": "Moment Energy", "category": "executive"},
    {"name": "Edward Chiao", "role": "CEO", "company": "Moment Energy", "category": "executive"},
    {"name": "Gene Berdichevsky", "role": "CEO", "company": "Sila Nanotechnologies", "category": "executive"},
    {"name": "Qichao Hu", "role": "CEO", "company": "SolidEnergy Systems", "category": "executive"},
    {"name": "Holden Thorp", "role": "CEO", "company": "Lyten", "category": "executive"},
    {"name": "Dan Neff", "role": "CEO", "company": "Lyten", "category": "executive"},
    {"name": "Song Ci", "role": "CEO", "company": "Conamix", "category": "executive"},
    {"name": "Johanna Wolfson", "role": "CEO", "company": "Cyclotron Road / Activate", "category": "executive"},
    
    # More utility-scale storage developers
    {"name": "Paul Shorteno", "role": "CEO", "company": "FranklinWH", "category": "executive"},
    {"name": "Himanshu Saxena", "role": "CEO", "company": "Starwood Energy", "category": "executive"},
    {"name": "Terrence Burgie", "role": "CEO", "company": "esVolta", "category": "executive"},
    {"name": "Alex Mackay", "role": "CEO", "company": "esVolta", "category": "executive"},
    {"name": "Danny Kennedy", "role": "CEO", "company": "New Energy Nexus", "category": "executive"},
    {"name": "Arvin Ganesan", "role": "CEO", "company": "Borrego Solar / RPCS", "category": "executive"},
    
    # EPC / integrators
    {"name": "George Sakellaris", "role": "Founder & CEO", "company": "Ameresco", "category": "executive"},
    {"name": "Spencer Maughan", "role": "CEO", "company": "Ameresco", "category": "executive"},
    {"name": "Mark Ravi", "role": "CEO", "company": "Wärtsilä Energy Storage", "category": "executive"},
    {"name": "Rahul Walawalkar", "role": "CEO", "company": "India Energy Storage Alliance / Customized Energy Solutions", "category": "executive"},
    
    # More solar+storage
    {"name": "Bernadette Del Chiaro", "role": "Executive Director", "company": "CALSSA", "category": "policy"},
    {"name": "Ed Fenster", "role": "Founder", "company": "Sunrun", "category": "executive"},
    
    # Equipment/component manufacturers
    {"name": "Zach Carlin", "role": "CEO", "company": "Standard Lithium", "category": "executive"},
    {"name": "Kent Masters", "role": "CEO", "company": "Albemarle", "category": "executive"},
    {"name": "Paul Graves", "role": "CEO", "company": "Livent (now part of Arcadium)", "category": "executive"},
    {"name": "John Mitchell", "role": "CEO", "company": "American Lithium Energy", "category": "executive"},
    {"name": "Gene Saragnese", "role": "CEO", "company": "Saft (Total subsidiary)", "category": "executive"},
    
    # More research institutions
    {"name": "Bruce Dunn", "role": "Professor", "company": "UCLA", "category": "researcher"},
    {"name": "Ping Liu", "role": "Director", "company": "ARPA-E (former)", "category": "policy"},
    {"name": "Eric Toone", "role": "Director", "company": "ARPA-E (former)", "category": "policy"},
    {"name": "Ellen Williams", "role": "Director", "company": "ARPA-E (former)", "category": "policy"},
    {"name": "Evelyn Wang", "role": "Director", "company": "ARPA-E", "category": "policy"},
    
    # State regulators focused on storage
    {"name": "Carla Peterman", "role": "Former Commissioner", "company": "CPUC", "category": "policy"},
    {"name": "Genevieve Shiroma", "role": "Commissioner", "company": "CPUC", "category": "policy"},
    {"name": "John Reynolds", "role": "Commissioner", "company": "CPUC", "category": "policy"},
    {"name": "Karen Douglas", "role": "Commissioner", "company": "California Energy Commission", "category": "policy"},
    {"name": "Siva Gunda", "role": "Vice Chair", "company": "California Energy Commission", "category": "policy"},
    
    # Industry associations / advocates
    {"name": "James Adams", "role": "CEO", "company": "Protergia", "category": "executive"},
    {"name": "Gloria Juarez Salazar", "role": "Senior Director", "company": "SEIA", "category": "policy"},
    {"name": "Cody Hill", "role": "Senior Director", "company": "ACP", "category": "policy"},
    {"name": "Jeff Cramer", "role": "Executive Director", "company": "MEC", "category": "policy"},
    
    # More VCs focused on energy storage
    {"name": "David Danielson", "role": "Partner", "company": "Breakthrough Energy Ventures", "category": "investor"},
    {"name": "Emily Reichert", "role": "CEO", "company": "Greentown Labs", "category": "investor"},
    {"name": "Peter Longo", "role": "Co-Founder", "company": "Prelude Ventures", "category": "investor"},
    {"name": "Maura Lafferty", "role": "Partner", "company": "Prelude Ventures", "category": "investor"},
    {"name": "Jason Blumberg", "role": "Managing Partner", "company": "Energize Ventures", "category": "investor"},
    {"name": "John Tough", "role": "CEO", "company": "Energize Ventures", "category": "investor"},
    {"name": "Andrew Beebe", "role": "Managing Director", "company": "Obvious Ventures", "category": "investor"},
    {"name": "Gia Schneider", "role": "Co-Founder & CEO", "company": "Natel Energy", "category": "executive"},
    
    # Grid software/optimization
    {"name": "Audrey Lee", "role": "CEO", "company": "Autoform Energy", "category": "executive"},
    {"name": "Paul Shorteno", "role": "CEO", "company": "FranklinWH", "category": "executive"},
    {"name": "Suleman Khan", "role": "CEO", "company": "GridBeyond", "category": "executive"},
    {"name": "Rahul Kar", "role": "CEO", "company": "Enode", "category": "executive"},
    
    # More battery recycling
    {"name": "Ryan Melsert", "role": "CEO", "company": "American Battery Technology Company", "category": "executive"},
    {"name": "Douglas Linde", "role": "CEO", "company": "Ascend Elements", "category": "executive"},
    {"name": "Mike O'Kronley", "role": "CEO", "company": "Ascend Elements", "category": "executive"},
    {"name": "Ajay Kochhar", "role": "CEO", "company": "Li-Cycle", "category": "executive"},
    {"name": "Tim Johnston", "role": "Co-Founder", "company": "Li-Cycle", "category": "executive"},
    
    # European storage leaders
    {"name": "Christoph Ostermann", "role": "CEO", "company": "Sonnen", "category": "executive"},
    {"name": "Oliver Koch", "role": "CEO", "company": "Sonnen (new)", "category": "executive"},
    {"name": "Thomas Raffeiner", "role": "Founder", "company": "The Mobility House", "category": "executive"},
    
    # Australian storage market
    {"name": "Hornsdale Power Reserve Team", "role": "Project", "company": "Neoen/Tesla", "category": "executive"},
    {"name": "Louis de Sambucy", "role": "Managing Director", "company": "Neoen Australia", "category": "executive"},
    
    # More media/journalists covering storage
    {"name": "Dan Lowrey", "role": "Editor", "company": "Energy Storage News", "category": "media"},
    {"name": "Billy Ludt", "role": "Managing Editor", "company": "Solar Power World", "category": "media"},
    {"name": "Mark Chediak", "role": "Reporter", "company": "Bloomberg", "category": "media"},
    {"name": "Will Wade", "role": "Reporter", "company": "Bloomberg", "category": "media"},
    {"name": "Jennifer Hiller", "role": "Reporter", "company": "Wall Street Journal", "category": "media"},
    {"name": "Nichola Groom", "role": "Reporter", "company": "Reuters", "category": "media"},
    {"name": "Timothy Puko", "role": "Reporter", "company": "Washington Post", "category": "media"},
    {"name": "Brad Plumer", "role": "Reporter", "company": "New York Times", "category": "media"},
    {"name": "Ivan Penn", "role": "Reporter", "company": "New York Times", "category": "media"},
    {"name": "Umair Irfan", "role": "Reporter", "company": "Vox", "category": "media"},
    {"name": "Dave Cooke", "role": "Researcher", "company": "UCS", "category": "researcher"},
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
                "source": "manual_storage_figures",
                "notes": "Energy storage industry figure"
            }
            f.write(json.dumps(entry) + '\n')
            added += 1

print(f"Added {added} more storage industry figures")
