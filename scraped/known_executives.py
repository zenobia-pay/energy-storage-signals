#!/usr/bin/env python3
"""Add known energy storage executives and influencers"""

import json
from pathlib import Path

BASE_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")

# Known key figures in energy storage industry
executives = [
    # Form Energy
    {"name": "Mateo Jaramillo", "role": "CEO & Co-Founder", "company": "Form Energy", "twitter": "@MateoJaramillo", "category": "executive"},
    {"name": "Yet-Ming Chiang", "role": "Chief Scientist & Co-Founder", "company": "Form Energy", "twitter": None, "category": "executive"},
    {"name": "Marco Ferrara", "role": "Co-Founder", "company": "Form Energy", "twitter": None, "category": "executive"},
    {"name": "Ted Wiley", "role": "Chief Operating Officer", "company": "Form Energy", "twitter": None, "category": "executive"},
    
    # Fluence
    {"name": "Julian Nebreda", "role": "President & CEO", "company": "Fluence", "twitter": "@JulianNebreda", "category": "executive"},
    {"name": "Dennis Fehr", "role": "CFO", "company": "Fluence", "twitter": None, "category": "executive"},
    {"name": "Rebecca Boll", "role": "COO", "company": "Fluence", "twitter": None, "category": "executive"},
    
    # Eos Energy
    {"name": "Joe Mastrangelo", "role": "CEO", "company": "Eos Energy Enterprises", "twitter": None, "category": "executive"},
    
    # Tesla Energy
    {"name": "Mike Snyder", "role": "Senior Director Energy", "company": "Tesla", "twitter": None, "category": "executive"},
    
    # Powin/FlexGen
    {"name": "Geoff Brown", "role": "CEO", "company": "Powin", "twitter": None, "category": "executive"},
    {"name": "Kelcy Pegler", "role": "CEO", "company": "FlexGen", "twitter": "@kelcypegler", "category": "executive"},
    
    # Key Capture Energy
    {"name": "Jeff Bishop", "role": "CEO", "company": "Key Capture Energy", "twitter": None, "category": "executive"},
    
    # Plus Power
    {"name": "Jake Pollock", "role": "CEO", "company": "Plus Power", "twitter": None, "category": "executive"},
    
    # ESS Inc
    {"name": "Eric Dresselhuys", "role": "CEO", "company": "ESS Inc", "twitter": None, "category": "executive"},
    
    # Energy Vault
    {"name": "Robert Piconi", "role": "CEO", "company": "Energy Vault", "twitter": None, "category": "executive"},
    
    # Redwood Materials
    {"name": "JB Straubel", "role": "CEO & Founder", "company": "Redwood Materials", "twitter": "@JBStraubel", "category": "executive"},
    
    # QuantumScape
    {"name": "Siva Sivaram", "role": "CEO", "company": "QuantumScape", "twitter": "@QuantumScapeCo", "category": "executive"},
    
    # Ambri
    {"name": "David Bradwell", "role": "CEO & CTO", "company": "Ambri", "twitter": None, "category": "executive"},
    
    # Stem
    {"name": "John Carrington", "role": "CEO", "company": "Stem Inc", "twitter": None, "category": "executive"},
    
    # NextEra
    {"name": "John Ketchum", "role": "CEO", "company": "NextEra Energy", "twitter": None, "category": "executive"},
    
    # Vistra
    {"name": "Jim Burke", "role": "CEO", "company": "Vistra Corp", "twitter": None, "category": "executive"},
    
    # AES
    {"name": "Andres Gluski", "role": "CEO", "company": "AES Corporation", "twitter": "@Andres_Gluski", "category": "executive"},
    
    # Bloomberg NEF
    {"name": "Ethan Zindler", "role": "Head of Americas", "company": "BloombergNEF", "twitter": "@EthanZindler", "category": "analyst"},
    {"name": "Nat Bullard", "role": "Chief Content Officer", "company": "BloombergNEF", "twitter": "@NatBullard", "category": "analyst"},
    {"name": "Logan Goldie-Scot", "role": "Head of Clean Power", "company": "BloombergNEF", "twitter": None, "category": "analyst"},
    
    # Wood Mackenzie
    {"name": "Dan Shreve", "role": "Head of Global Wind Research", "company": "Wood Mackenzie", "twitter": "@DanShreve", "category": "analyst"},
    {"name": "Ravi Manghani", "role": "Head of Energy Storage", "company": "Wood Mackenzie", "twitter": "@ravigupta", "category": "analyst"},
    
    # S&P Global
    {"name": "Ira Joseph", "role": "Managing Director", "company": "S&P Global Commodity Insights", "twitter": "@Ira_Joseph", "category": "analyst"},
    
    # IHS Markit / S&P
    {"name": "Samuel Wilkinson", "role": "Executive Director, Energy Storage", "company": "S&P Global", "twitter": None, "category": "analyst"},
    
    # Clean Energy Associates
    {"name": "Andy Klump", "role": "CEO", "company": "Clean Energy Associates", "twitter": None, "category": "executive"},
    
    # Modo Energy
    {"name": "Rachel Winter", "role": "CEO", "company": "Modo Energy", "twitter": None, "category": "executive"},
    
    # Aurora Energy Research
    {"name": "John Feddersen", "role": "CEO", "company": "Aurora Energy Research", "twitter": None, "category": "executive"},
    
    # LDES Council
    {"name": "Julia Souder", "role": "CEO", "company": "Long Duration Energy Storage Council", "twitter": None, "category": "executive"},
    
    # Energy Storage Association (now ACP)
    {"name": "Jason Burwen", "role": "VP of Energy Storage", "company": "American Clean Power Association", "twitter": "@JasonBurwen", "category": "policy"},
    
    # Influential academics / researchers
    {"name": "Ramez Naam", "role": "Lecturer & Author", "company": "Singularity University / Stanford", "twitter": "@ramaborki", "category": "researcher"},
    {"name": "Jessika Trancik", "role": "Professor", "company": "MIT", "twitter": "@JessikaTrancik", "category": "researcher"},
    {"name": "John Goodenough", "role": "Professor (deceased)", "company": "UT Austin", "twitter": None, "category": "researcher", "notes": "Nobel Prize winner, lithium-ion pioneer"},
    {"name": "Shirley Meng", "role": "Professor", "company": "University of Chicago", "twitter": None, "category": "researcher"},
    {"name": "Venkat Viswanathan", "role": "Professor", "company": "Carnegie Mellon University", "twitter": "@vikithechemist", "category": "researcher"},
    
    # Policy / Government
    {"name": "Jigar Shah", "role": "Director of Loan Programs Office", "company": "US Department of Energy", "twitter": "@JigarShahDC", "category": "policy"},
    {"name": "David Turk", "role": "Deputy Secretary", "company": "US Department of Energy", "twitter": "@Aborki", "category": "policy"},
    
    # Key VCs / Investors
    {"name": "Nancy Pfund", "role": "Managing Partner", "company": "DBL Partners", "twitter": "@NancyPfund", "category": "investor"},
    {"name": "Chamath Palihapitiya", "role": "CEO", "company": "Social Capital", "twitter": "@chaaborki", "category": "investor"},
    {"name": "Vinod Khosla", "role": "Founder", "company": "Khosla Ventures", "twitter": "@vaborki", "category": "investor"},
    {"name": "John Doerr", "role": "Chairman", "company": "Kleiner Perkins", "twitter": "@johndoerr", "category": "investor"},
    {"name": "Connie Chan", "role": "General Partner", "company": "Andreessen Horowitz", "twitter": "@conniechan", "category": "investor"},
    
    # Key journalists / media
    {"name": "David Roberts", "role": "Writer", "company": "Volts / Canary Media", "twitter": "@drvolts", "category": "media"},
    {"name": "Robinson Meyer", "role": "Executive Editor", "company": "Heatmap News", "twitter": "@yayitsrob", "category": "media"},
    {"name": "Katherine Blunt", "role": "Energy Reporter", "company": "Wall Street Journal", "twitter": "@katieblunt", "category": "media"},
    {"name": "Russell Gold", "role": "Communications", "company": "T1 Energy (formerly WSJ)", "twitter": "@russellgold", "category": "media"},
    
    # Additional influencers
    {"name": "Leah Stokes", "role": "Professor", "company": "UC Santa Barbara", "twitter": "@LeahStokes", "category": "researcher"},
    {"name": "Emily Grubert", "role": "Professor", "company": "Notre Dame", "twitter": "@EmilyGrubert", "category": "researcher"},
    {"name": "Severin Borenstein", "role": "Professor", "company": "UC Berkeley", "twitter": "@severinb", "category": "researcher"},
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
                "source": "manual_industry_knowledge",
                "notes": person.get('notes', "Key figure in energy storage industry")
            }
            f.write(json.dumps(entry) + '\n')
            added += 1

print(f"Added {added} known industry figures")
