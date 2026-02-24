#!/usr/bin/env python3
"""Add more energy sector figures across categories"""

import json
from pathlib import Path

BASE_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")

figures = [
    # More cleantech investors / PE
    {"name": "David Giampaolo", "role": "CEO", "company": "Pi Labs / Energy Impact Partners", "category": "investor"},
    {"name": "Andy Karsner", "role": "Managing Partner", "company": "Elemental Impact", "category": "investor"},
    {"name": "Hemant Taneja", "role": "Managing Partner", "company": "General Catalyst", "category": "investor"},
    {"name": "Dawn Lippert", "role": "CEO", "company": "Elemental Excelerator", "category": "investor"},
    {"name": "Wal van Lierop", "role": "Founder", "company": "Chrysalix Venture Capital", "category": "investor"},
    {"name": "John O'Farrell", "role": "Partner", "company": "Andreessen Horowitz", "category": "investor"},
    {"name": "Katie Hall", "role": "Co-Founder", "company": "Giving Green", "category": "investor"},
    {"name": "Sunil Paul", "role": "Managing Partner", "company": "Spring Ventures", "category": "investor"},
    {"name": "Tom Steyer", "role": "Founder", "company": "NextGen America", "category": "investor"},
    {"name": "Nat Simons", "role": "Co-Founder", "company": "Sea Change Foundation", "category": "investor"},
    {"name": "Michael Bloomberg", "role": "Founder", "company": "Bloomberg Philanthropies", "category": "investor"},
    {"name": "Russ Wilcox", "role": "Partner", "company": "Pillar VC", "category": "investor"},
    {"name": "Varun Sivaram", "role": "Senior VP", "company": "IEA (former Fix Climate)", "category": "researcher"},
    
    # More NREL/national lab researchers
    {"name": "Peregrine Wolff", "role": "Director", "company": "NREL (materials)", "category": "researcher"},
    {"name": "Daniel Ginosar", "role": "Director", "company": "INL", "category": "researcher"},
    {"name": "John Wagner", "role": "Director", "company": "INL", "category": "researcher"},
    {"name": "Michael Zarnstorff", "role": "Deputy Director", "company": "PPPL", "category": "researcher"},
    {"name": "Dennis Whyte", "role": "Director", "company": "MIT PSFC", "category": "researcher"},
    {"name": "Bob Mumgaard", "role": "CEO", "company": "Commonwealth Fusion Systems", "category": "executive"},
    
    # More transmission/grid developers
    {"name": "Hunter Armistead", "role": "CEO", "company": "Pattern Energy", "category": "executive"},
    {"name": "Brian Lawson", "role": "CFO", "company": "Invenergy", "category": "executive"},
    {"name": "Ted Brandt", "role": "CEO", "company": "Marathon Capital", "category": "executive"},
    {"name": "Kurt Ziegler", "role": "MD", "company": "KeyBanc Capital Markets", "category": "executive"},
    {"name": "Andy Redinger", "role": "MD", "company": "KeyBanc Capital Markets", "category": "executive"},
    
    # Energy storage software
    {"name": "Sean Casten", "role": "Former CEO / Congressman", "company": "Recycled Energy Development", "category": "executive"},
    {"name": "Brian Janous", "role": "VP Energy", "company": "Meta (Facebook)", "category": "executive"},
    {"name": "Michael Terrell", "role": "Director of Energy", "company": "Google", "category": "executive"},
    {"name": "Noelle Simmons", "role": "Head of Energy", "company": "Google", "category": "executive"},
    {"name": "Caroline Golin", "role": "Head of Sustainability", "company": "Apple", "category": "executive"},
    {"name": "Lisa Jackson", "role": "VP Environment", "company": "Apple", "category": "executive"},
    {"name": "Ken Salazar", "role": "Chairman", "company": "WilmerHale (Former DOI)", "category": "policy"},
    
    # Energy law / consulting
    {"name": "Bruce Huber", "role": "Partner", "company": "Kirkland & Ellis", "category": "analyst"},
    {"name": "Joe Shorin", "role": "Partner", "company": "Latham & Watkins", "category": "analyst"},
    {"name": "Patricia Wozniak", "role": "Partner", "company": "Kirkland & Ellis", "category": "analyst"},
    {"name": "Ken Stern", "role": "Partner", "company": "Akin Gump", "category": "analyst"},
    {"name": "Nicole Sitaraman", "role": "SVP Policy", "company": "Salesforce", "category": "policy"},
    
    # More solar/wind executives
    {"name": "Arno Harris", "role": "Founder", "company": "Recurrent Energy", "category": "executive"},
    {"name": "Russ Dyk", "role": "CEO", "company": "Sky Solar", "category": "executive"},
    {"name": "Suvi Sharma", "role": "CEO", "company": "Solaria", "category": "executive"},
    {"name": "Bill Stein", "role": "CEO", "company": "Digital Realty", "category": "executive"},
    {"name": "Cris Eugster", "role": "President", "company": "CPS Energy", "category": "executive"},
    {"name": "Paula Gold-Williams", "role": "Former CEO", "company": "CPS Energy", "category": "executive"},
    
    # Hydrogen / decarbonization
    {"name": "Arshad Mansoor", "role": "CEO", "company": "EPRI", "category": "researcher"},
    {"name": "Mike Howard", "role": "President & CEO", "company": "EPRI", "category": "researcher"},
    {"name": "Sunita Satyapal", "role": "Director", "company": "DOE Hydrogen & Fuel Cell", "category": "policy"},
    {"name": "Laura Luce", "role": "CEO", "company": "Shell New Energies", "category": "executive"},
    {"name": "Wael Sawan", "role": "CEO", "company": "Shell", "category": "executive"},
    {"name": "Darren Woods", "role": "CEO", "company": "ExxonMobil", "category": "executive"},
    {"name": "Mike Wirth", "role": "CEO", "company": "Chevron", "category": "executive"},
    {"name": "Ryan Lance", "role": "CEO", "company": "ConocoPhillips", "category": "executive"},
    {"name": "Bernard Looney", "role": "Former CEO", "company": "BP", "category": "executive"},
    {"name": "Murray Auchincloss", "role": "CEO", "company": "BP", "category": "executive"},
    {"name": "Patrick Pouyanné", "role": "CEO", "company": "TotalEnergies", "category": "executive"},
    
    # Grid modernization / smart grid
    {"name": "Katherine Hammack", "role": "Executive", "company": "Grid Assurance", "category": "executive"},
    {"name": "Chris Shelton", "role": "CEO", "company": "Uplight", "category": "executive"},
    {"name": "Tom Siebel", "role": "CEO", "company": "C3.ai", "category": "executive"},
    {"name": "Peter Csathy", "role": "CEO", "company": "Creatv Media", "category": "executive"},
    {"name": "Michael Jung", "role": "CEO", "company": "Electrify America", "category": "executive"},
    {"name": "Giovanni Palazzo", "role": "CEO", "company": "Electrify America", "category": "executive"},
    {"name": "Jeff Cohen", "role": "CEO", "company": "EVgo", "category": "executive"},
    {"name": "Cathy Zoi", "role": "CEO", "company": "EVgo", "category": "executive"},
    {"name": "Brendan Jones", "role": "CEO", "company": "ChargePoint", "category": "executive"},
    {"name": "Pasquale Romano", "role": "Former CEO", "company": "ChargePoint", "category": "executive"},
    
    # Environmental justice / community solar
    {"name": "Keith Welks", "role": "CEO", "company": "Apollo Solar", "category": "executive"},
    {"name": "Nicole Steele", "role": "Executive Director", "company": "The Hive Fund", "category": "policy"},
    {"name": "Anthony Giancatarino", "role": "Program Director", "company": "Center for Social Inclusion", "category": "policy"},
    {"name": "Jacqueline Patterson", "role": "Founder", "company": "Chisholm Legacy Project", "category": "policy"},
    {"name": "Donnel Baird", "role": "Founder", "company": "BlocPower", "category": "executive"},
    {"name": "Valencia Gunder", "role": "Co-Founder", "company": "Urban Energy Institute", "category": "policy"},
    {"name": "Robert Bullard", "role": "Professor", "company": "Texas Southern University", "category": "researcher"},
    {"name": "Mustafa Santiago Ali", "role": "EVP", "company": "National Wildlife Federation", "category": "policy"},
    
    # More media covering energy
    {"name": "Adam Vaughan", "role": "Environment Correspondent", "company": "New Scientist", "category": "media"},
    {"name": "John Timmer", "role": "Science Editor", "company": "Ars Technica", "category": "media"},
    {"name": "Dana Hull", "role": "Reporter", "company": "Bloomberg", "category": "media"},
    {"name": "Tom Randall", "role": "Editor", "company": "Bloomberg Green", "category": "media"},
    {"name": "Akshat Rathi", "role": "Reporter", "company": "Bloomberg", "category": "media"},
    {"name": "Naureen Malik", "role": "Reporter", "company": "Bloomberg", "category": "media"},
    {"name": "Javier Blas", "role": "Columnist", "company": "Bloomberg", "category": "media"},
    {"name": "Brian Eckhouse", "role": "Reporter", "company": "Bloomberg", "category": "media"},
    {"name": "Laura Millan", "role": "Reporter", "company": "Bloomberg", "category": "media"},
    {"name": "Chris Martin", "role": "Reporter", "company": "Bloomberg", "category": "media"},
    
    # Energy think tanks
    {"name": "Jason Bordoff", "role": "Dean", "company": "Columbia SIPA / CGEP", "category": "researcher"},
    {"name": "Samantha Gross", "role": "Director", "company": "Brookings Energy Security", "category": "researcher"},
    {"name": "Sarah Ladislaw", "role": "Managing Director", "company": "RMI (former CSIS)", "category": "researcher"},
    {"name": "Nikos Tsafos", "role": "Director", "company": "CSIS Energy & Climate", "category": "researcher"},
    {"name": "David Goldwyn", "role": "Chairman", "company": "Goldwyn Global Strategies", "category": "analyst"},
    {"name": "Paula Gant", "role": "SVP", "company": "AGA", "category": "policy"},
    {"name": "Amy Myers Jaffe", "role": "Research Professor", "company": "NYU", "category": "researcher"},
    {"name": "Meghan O'Sullivan", "role": "Professor", "company": "Harvard Kennedy School", "category": "researcher"},
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
                "source": "manual_energy_figures",
                "notes": "Energy sector figure"
            }
            f.write(json.dumps(entry) + '\n')
            added += 1

print(f"Added {added} more energy sector figures")
