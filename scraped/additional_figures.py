#!/usr/bin/env python3
"""Add more known energy storage figures from various sources"""

import json
from pathlib import Path

BASE_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")

# Additional figures across various sectors
figures = [
    # More battery/storage startups
    {"name": "Suhas Kumar", "role": "CEO", "company": "Alsym Energy", "category": "executive"},
    {"name": "Mukesh Chatter", "role": "Co-Founder", "company": "Alsym Energy", "category": "executive"},
    {"name": "Ted Bilich", "role": "CEO", "company": "Electrovaya", "category": "executive"},
    {"name": "Sanjay Murthi", "role": "CEO", "company": "CMB Energy", "category": "executive"},
    {"name": "Tyler Lyman", "role": "CEO", "company": "Torus Clean Energy", "category": "executive"},
    {"name": "Greg Callman", "role": "CEO", "company": "Power Edison", "category": "executive"},
    {"name": "Craig Wilkins", "role": "CEO", "company": "Endurant Energy", "category": "executive"},
    {"name": "Marc Burdette", "role": "CEO", "company": "Aclara Resources", "category": "executive"},
    {"name": "Joe McGill", "role": "CEO", "company": "Convergent Energy + Power", "category": "executive"},
    {"name": "Johannes Rittershausen", "role": "CEO", "company": "Convergent Energy + Power", "category": "executive"},
    
    # Solar/storage integrated companies
    {"name": "Tom Werner", "role": "Former CEO", "company": "SunPower", "category": "executive"},
    {"name": "Peter Faricy", "role": "CEO", "company": "SunPower", "category": "executive"},
    {"name": "Badri Kothandaraman", "role": "CEO", "company": "Enphase Energy", "category": "executive"},
    {"name": "Mary Powell", "role": "CEO", "company": "Sunrun", "category": "executive"},
    {"name": "Lynn Jurich", "role": "Co-Founder", "company": "Sunrun", "category": "executive"},
    {"name": "Paul Shorteno", "role": "CEO", "company": "FranklinWH", "category": "executive"},
    
    # Project developers
    {"name": "John Carlin", "role": "CEO", "company": "intersect Power", "category": "executive"},
    {"name": "Sheldon Kimber", "role": "CEO", "company": "Recurrent Energy", "category": "executive"},
    {"name": "George Hershman", "role": "CEO", "company": "SOLV Energy", "category": "executive"},
    {"name": "Michael Rucker", "role": "CEO", "company": "Origis Energy", "category": "executive"},
    {"name": "Vikas Anand", "role": "CEO", "company": "Sungrow North America", "category": "executive"},
    
    # Trading / BESS optimization
    {"name": "John Zahurancik", "role": "CEO", "company": "REV Renewables", "category": "executive"},
    {"name": "Sean Hayes", "role": "CEO", "company": "Jupiter Power", "category": "executive"},
    {"name": "Kevin Walsh", "role": "CEO", "company": "Pattern Energy", "category": "executive"},
    
    # Hardware manufacturers
    {"name": "Robin Zeng", "role": "Founder & Chairman", "company": "CATL", "category": "executive"},
    {"name": "Wang Chuanfu", "role": "Founder & President", "company": "BYD", "category": "executive"},
    {"name": "Pan Jian", "role": "CEO", "company": "EVE Energy", "category": "executive"},
    {"name": "Li Ping", "role": "President", "company": "CALB", "category": "executive"},
    
    # More utility/IPP executives
    {"name": "Steve Berberich", "role": "Former CEO", "company": "CAISO", "category": "policy"},
    {"name": "Mark Ahlstrom", "role": "VP", "company": "NextEra Analytics", "category": "executive"},
    {"name": "Andrew Marsh", "role": "CEO", "company": "Plug Power", "category": "executive"},
    {"name": "Andy Marsh", "role": "CEO", "company": "Plug Power", "category": "executive"},
    
    # Finance / PE / Infrastructure funds
    {"name": "Michael Polsky", "role": "Founder & CEO", "company": "Invenergy", "category": "executive"},
    {"name": "Jim Robo", "role": "Former CEO", "company": "NextEra Energy", "category": "executive"},
    {"name": "Connor Teskey", "role": "CEO", "company": "Brookfield Renewable", "category": "executive"},
    {"name": "Nick Heymann", "role": "Research Lead", "company": "Wolfe Research", "category": "analyst"},
    
    # More researchers
    {"name": "Gerbrand Ceder", "role": "Professor", "company": "UC Berkeley", "category": "researcher"},
    {"name": "Jennifer Wilcox", "role": "Principal Deputy Assistant Secretary", "company": "DOE FECM", "category": "policy"},
    {"name": "Vanessa Chan", "role": "Chief Commercialization Officer", "company": "DOE", "category": "policy"},
    {"name": "Kelly Sims Gallagher", "role": "Professor", "company": "Tufts University", "category": "researcher"},
    {"name": "Daniel Schrag", "role": "Professor", "company": "Harvard University", "category": "researcher"},
    {"name": "Robert Stavins", "role": "Professor", "company": "Harvard Kennedy School", "category": "researcher"},
    
    # Grid/transmission
    {"name": "Rich Heidorn Jr.", "role": "Editor", "company": "RTO Insider", "category": "media"},
    {"name": "Rob Gramlich", "role": "President", "company": "Grid Strategies", "category": "analyst"},
    {"name": "John Peschon", "role": "Managing Partner", "company": "GridBridge", "category": "executive"},
    
    # State PUC commissioners
    {"name": "Willie Phillips", "role": "Chairman", "company": "FERC", "category": "policy"},
    {"name": "Mark Christie", "role": "Commissioner", "company": "FERC", "category": "policy"},
    {"name": "Allison Clements", "role": "Commissioner", "company": "FERC", "category": "policy"},
    {"name": "James Danly", "role": "Commissioner", "company": "FERC", "category": "policy"},
    
    # Influential thought leaders / writers
    {"name": "Bill Gates", "role": "Founder", "company": "Breakthrough Energy", "category": "investor"},
    {"name": "Carmichael Roberts", "role": "Board Member", "company": "Breakthrough Energy Ventures", "category": "investor"},
    {"name": "Kate Konschnik", "role": "Director", "company": "Duke Nicholas Institute", "category": "researcher"},
    {"name": "Harrison Fell", "role": "Professor", "company": "NC State / RFF", "category": "researcher"},
    {"name": "Dallas Burtraw", "role": "Senior Fellow", "company": "Resources for the Future", "category": "researcher"},
    {"name": "Karen Palmer", "role": "Senior Fellow", "company": "Resources for the Future", "category": "researcher"},
    
    # More international
    {"name": "Wang Fang", "role": "President", "company": "LONGi Green Energy", "category": "executive"},
    {"name": "Li Zhenguo", "role": "Founder & President", "company": "LONGi", "category": "executive"},
    {"name": "Cao Renxian", "role": "Chairman", "company": "Sungrow", "category": "executive"},
    {"name": "Huang Mingyao", "role": "CEO", "company": "Trina Solar", "category": "executive"},
    {"name": "Liu Yongzhi", "role": "CEO", "company": "JA Solar", "category": "executive"},
    {"name": "Chen Gang", "role": "CEO", "company": "JinkoSolar", "category": "executive"},
    
    # Consulting firm energy leads
    {"name": "Kingsmill Bond", "role": "Energy Strategist", "company": "RMI", "category": "analyst"},
    {"name": "Mark Lewis", "role": "Chief Sustainability Strategist", "company": "Andurand Capital", "category": "analyst"},
    {"name": "Julio Friedmann", "role": "Chief Scientist", "company": "Carbon Direct", "category": "researcher"},
    {"name": "Sarah Forbes", "role": "VP", "company": "Great Plains Institute", "category": "policy"},
    
    # Trade associations
    {"name": "Gregory Wetstone", "role": "CEO", "company": "American Council on Renewable Energy", "category": "policy"},
    {"name": "Tom Kiernan", "role": "Former CEO", "company": "American Wind Energy Association", "category": "policy"},
    {"name": "Gene Rodrigues", "role": "Assistant Secretary", "company": "DOE EERE", "category": "policy"},
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
                "source": "manual_industry_knowledge_3",
                "notes": "Key figure in energy storage/clean energy industry"
            }
            f.write(json.dumps(entry) + '\n')
            added += 1

print(f"Added {added} additional industry figures")
