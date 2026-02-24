#!/usr/bin/env python3
"""Parse IESNA speakers and add to people.jsonl"""

import json
from pathlib import Path

BASE_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")

speakers = [
    {"name": "Maram Al-Daraiseh", "role": "Renewable Energy & AI Specialist", "company": None},
    {"name": "Gaby Alvayay Olson", "role": "Director Sales & Sourcing NA", "company": "Redwood Materials"},
    {"name": "Douglas Amarhanow", "role": "Product Manager", "company": "FranklinWH"},
    {"name": "Jason Anderson", "role": "President and CEO", "company": "Cleantech San Diego"},
    {"name": "Shannon Anderson", "role": "Distributed Power Plant Policy Director", "company": "Solar United Neighbors"},
    {"name": "Stein Arntson", "role": "Enterprise Account Manager", "company": "Aurora Solar/HelioScope"},
    {"name": "Tristan Bannon", "role": "Chief Commercial Officer", "company": "CellCube Energy Storage, Inc."},
    {"name": "Teresa Barnes", "role": "NCPV and DuraMAT Director", "company": "National Lab of the Rockies"},
    {"name": "Karen Bazela", "role": "SVP, Sales", "company": "Shoals Technologies"},
    {"name": "Todd Beeby", "role": "Director of Performance Engineering", "company": "Key Capture Energy"},
    {"name": "Carrie Bentley", "role": "Co-founder and CEO", "company": "Gridwell Consulting"},
    {"name": "Helge Biernath", "role": "CEO", "company": "Sunstall Inc."},
    {"name": "Matthew Boms", "role": "Executive Director, TAEBA", "company": "Advanced Energy United"},
    {"name": "Aron Bowman", "role": "President", "company": "ELM MicroGrid"},
    {"name": "Leah Brams", "role": "Manager, Market Development", "company": "Highland Electric Fleets"},
    {"name": "Timothy Brightbill", "role": "Partner", "company": "Wiley"},
    {"name": "Claire Broido Johnson", "role": "President", "company": "Sunrock Distributed Generation"},
    {"name": "Bill Brooks", "role": "Principal", "company": "Brooks Engineering"},
    {"name": "Cameron Brooks", "role": "Executive Director", "company": "Think Microgrid"},
    {"name": "Marshall Brunson", "role": "Curriculum Developer & Trainer", "company": "Solar Energy International"},
    {"name": "Doug Bryan", "role": "Senior Power and Energy Systems Modeler", "company": "Carbon Direct"},
    {"name": "Olivia Burton", "role": "Sr. Manager, Engineering Operations", "company": "Tesla"},
    {"name": "Evelyn Carpenter", "role": "President & CEO", "company": "Invera Energy / Solas Energy"},
    {"name": "Melissa Chan", "role": "Senior Director of Ecosystem Development", "company": "Analog Devices"},
    {"name": "Brooks Chiongbian", "role": "Director of Business Operations", "company": "Sylvatex"},
    {"name": "Andrew Cifala", "role": "Principal, Strategy & Solutions - Grid Modernization", "company": "Keysight Technologies"},
    {"name": "Barry Cinnamon", "role": "CEO", "company": "Cinnamon Energy Systems"},
    {"name": "Jessie Ciulla-Shea", "role": "Director of Regulatory & Policy", "company": "Energy Dome"},
    {"name": "Scott Clavenna", "role": "CEO", "company": "Latitude Media, Inc."},
    {"name": "Sterling Clifford", "role": "Director of State Policy", "company": "Jinko Solar"},
    {"name": "Jonathan Colbert", "role": "VP of Marketing & Business Development", "company": "Voltera"},
    {"name": "Kate Collardson", "role": "Co-Founder", "company": "Solar Service of Colorado"},
    {"name": "Finlay Colville", "role": "Founder", "company": "Terawatt PV Research"},
    {"name": "Beth Crouchet", "role": "Director Energy Markets & Resource Planning", "company": "Budderfly"},
    {"name": "Mark Crowdis", "role": "CEO", "company": "127 Energy"},
    {"name": "Sriram Das", "role": "Co-Founder", "company": "DYCM Power"},
    {"name": "Paul Denholm", "role": "Research Fellow", "company": "NLR (formerly NREL)"},
    {"name": "Bonnie Doggett", "role": "Environmental Project Manager", "company": "HDR"},
    {"name": "Josh Dorfman", "role": "President", "company": "American Wire Group"},
    {"name": "Richard Dovere", "role": "CEO", "company": "Dispatch Energy"},
    {"name": "Suzi Emmerling", "role": "Founder", "company": "Calina Strategies"},
    {"name": "Stacy J. Ettinger", "role": "Senior Vice President, Supply Chain & Trade", "company": "SEIA"},
    {"name": "Karim Farhat", "role": "Revenue Growth & Partnerships Lead, Retail EV Charging", "company": "Walmart"},
    {"name": "Ty Fenton", "role": "Director of Data Analytics", "company": "FlexGen"},
    {"name": "Rocky Fernandez", "role": "Senior Director, Policy", "company": "Center for Sustainable Energy"},
    {"name": "Jessica Fishman", "role": "Marketing Consultant", "company": "Clean Energy Marketing Consulting"},
    {"name": "Thomas Folker", "role": "Chief Strategy Officer", "company": "Leap"},
    {"name": "Ryan Franks", "role": "Director, Product Management", "company": "SES AI Corp"},
    {"name": "Sean Gallagher", "role": "Senior Vice President, Policy", "company": "SEIA"},
    {"name": "Vish Ganti", "role": "President", "company": "DER Security Corp"},
    {"name": "Lance Gloss", "role": "Global Business Development Manager", "company": "Colorado OEDIT"},
    {"name": "Russell Gold", "role": "EVP-Strategic Communications", "company": "T1 Energy"},
    {"name": "Jack Groarke", "role": "Director of Government Relations", "company": "Qcells"},
    {"name": "Eva Guadamillas", "role": "Senior Advisory Manager", "company": "Carbon Direct"},
    {"name": "Anna Gusel", "role": "Director, Market Strategy and Business Development", "company": "enSights"},
    {"name": "Joanna Hamblin", "role": "Senior Marketing Consultant", "company": "Iron Core Marketing"},
    {"name": "Amy Harder", "role": "National Energy Correspondent", "company": "Axios"},
    {"name": "Doreen Harris", "role": "President and CEO", "company": "NYSERDA"},
    {"name": "Naphtal Haya", "role": "Practice Lead, Emerging Energy Storage Technologies", "company": "DNV"},
    {"name": "Brad Heavner", "role": "Executive Director", "company": "CA Solar & Storage Association"},
    {"name": "Geoffrey Hebertson", "role": "Lead Renewables Analyst", "company": "Rystad Energy"},
    {"name": "Kristen Helsel", "role": "CEO", "company": "Liberty Plugins"},
    {"name": "Lennart Hinrichs", "role": "Executive Vice President & General Manager Americas", "company": "TWAICE"},
    {"name": "Peggy Hock", "role": "Director, Utility Scale Project Sales", "company": "JA Solar USA"},
    {"name": "Connor Hogan", "role": "CFO", "company": "OnePlanet"},
    {"name": "Logan Hotz", "role": "Market Analyst", "company": "Modo Energy"},
    {"name": "Rebekah Hren", "role": "Senior Consultant", "company": "Solar Tech Collective"},
    {"name": "Iola Hughes", "role": "Head of Research", "company": "Benchmark (Rho Motion)"},
    {"name": "Alex Jahp", "role": "Senior Consultant", "company": "Solar Tech Collective"},
    {"name": "Kate Johnson", "role": "Executive Director", "company": "New England Women in Energy and the Environment"},
    {"name": "Michael Judge", "role": "Undersecretary of Energy", "company": "Massachusetts Executive Office of Energy"},
    {"name": "Brittany Kaplan", "role": "Head of Enterprise Sales", "company": "Electric Era"},
    {"name": "Ben Kaun", "role": "Chief Commercial Officer", "company": "Inlyte Energy"},
    {"name": "Ryan Kennedy", "role": "Senior Editor", "company": "pv magazine"},
    {"name": "Maxwell Kushner-Lenhoff", "role": "Chief Commercial Officer (CCO)", "company": "Mitra Chem"},
    {"name": "Richard Kwan", "role": "Engineer", "company": "Southern California Edison"},
    {"name": "Craig Lewis", "role": "Executive Director", "company": "Clean Coalition"},
    {"name": "Neil Maguire", "role": "CTO", "company": "Scale Microgrids"},
    {"name": "Jimena Martinez", "role": "Manager Operations Engineer", "company": "Lightsourcebp"},
    {"name": "Nick Matthes", "role": "Creator/CEO", "company": "Illumination Solar"},
    {"name": "Claire McConnell", "role": "Vice President of Business Development, Energy Storage", "company": "Redwood Materials"},
    {"name": "John McDonnell", "role": "CEO", "company": "WattHub Renewables"},
    {"name": "Whitley McGovern", "role": "Senior Account Executive", "company": "Virtual Peaker"},
    {"name": "Brian Mehalic", "role": "Senior Consultant", "company": "Solar Tech Collective"},
    {"name": "Adam Miller", "role": "CRO", "company": "Solarity"},
    {"name": "Emmitt Muckles", "role": "Founder & Principal Consultant", "company": "S. E. Power Consulting"},
    {"name": "Ashok Nair", "role": "Sr Vice President & Head of Sales", "company": "Waaree Solar Americas Inc"},
    {"name": "Robert Ngabesong", "role": "Senior Product Controls Manager", "company": "ON.Energy"},
    {"name": "Mike Nicholas", "role": "Energy Storage Specialist & Fire Consultant", "company": "Hiller"},
    {"name": "Mohammed Njie", "role": "CEO", "company": "Janta Power"},
    {"name": "Carolina Nunez-Barrera", "role": "Head of Legal & Compliance", "company": "BayWa r.e. Americas"},
    {"name": "Meghan O'Brien", "role": "Of Counsel", "company": "Van Ness Feldman LLP"},
    {"name": "Emilie O'Leary", "role": "CEO/Owner", "company": "Green Clean Solar"},
    {"name": "Heather O'Neill", "role": "President and CEO", "company": "Advanced Energy United"},
    {"name": "Cody Oliver", "role": "Director of Sales and Strategy", "company": "Comstock Metals"},
    {"name": "Mark Ortiz", "role": "Sr. Director, Chief Architect Power & Grid", "company": "Schneider Electric"},
    {"name": "Simon Ouellette", "role": "CEO", "company": "ChargeHub"},
    {"name": "Zack Overfield", "role": "South Central Cultural Resources Practice Leader", "company": "HDR"},
    {"name": "Arnab Pal", "role": "Executive Director", "company": "Deploy Action"},
    {"name": "Jon Parrella", "role": "Founder, Chief Executive Officer", "company": "TerraFlow Energy"},
    {"name": "Alex Pasanen", "role": "Manager, Policy & Regulatory Affairs", "company": "Solstice Power Technologies LLC"},
    {"name": "Natalie Patton", "role": "CEO", "company": "The Nth Degree Studio"},
    {"name": "Calvin Preston", "role": "Lead Renewable Energy Engineer", "company": "Verde Solutions"},
    {"name": "Adam Probolsky", "role": "President", "company": "Probolsky Research"},
    {"name": "Masih Qutb", "role": "Sr Director of Civil Engineering", "company": "Apex Clean Energy"},
    {"name": "Attilio Ravani", "role": "Senior Associate", "company": "Orennia"},
    {"name": "Bhaskar Ray", "role": "VP and Head of Transmission, Interconnection & Performance Engineering", "company": "Hanwha Renewables"},
    {"name": "John Wayne Rejebian", "role": "HEAD OF ENGINEERING / PARTNER", "company": "BLENDED POWER LLC"},
    {"name": "Joe Ritter", "role": "Chief Development Officer", "company": "Seminole Financial Services"},
    {"name": "Phil Roberts", "role": "Manager", "company": "NetZero Energy Systems, Inc."},
    {"name": "Marty Rogers", "role": "General Manager, North America", "company": "SolarEdge"},
    {"name": "Louise Ronaldson", "role": "Project Manager", "company": "Salka Energy"},
    {"name": "Christian Roselund", "role": "Senior Policy Analyst", "company": "Intertek CEA"},
    {"name": "Sammy Roth", "role": "Independent writer", "company": "Climate-Colored Goggles"},
    {"name": "David Sacci", "role": "Strategy & Operations Lead for EV Charging", "company": "Slate Auto"},
    {"name": "JC Sandberg", "role": "Chief Policy Officer", "company": "American Clean Power"},
    {"name": "Laureen Sanderson", "role": "CCO", "company": "CubicPV"},
    {"name": "Aric Saunders", "role": "EVP, Commercialization", "company": "Noon Energy"},
    {"name": "Andrea Saxenhofer", "role": "Senior Communications Strategist", "company": "Wright On Communications"},
    {"name": "Dante Sblendorio", "role": "Head of Software & Product Development", "company": "Critical Loop, Inc."},
    {"name": "Ben Schwartz", "role": "Policy Director", "company": "Clean Coalition"},
    {"name": "Emma Searson", "role": "Managing Policy Director", "company": "GRID Alternatives"},
    {"name": "Pooja Shah", "role": "Practice Lead, Tax Credit Technical Due Diligence", "company": "DNV"},
    {"name": "Alex Shoer", "role": "Managing Partner", "company": "GridVest"},
    {"name": "Tal Sholklapper", "role": "CEO and Co-Founder", "company": "Voltaiq"},
    {"name": "Anna J. Siefken", "role": "Director for Policy & Markets, North America", "company": "LDES Council"},
    {"name": "Daniel Sottosanti", "role": "VP, Business Development", "company": "XL Batteries"},
    {"name": "Valessa Souter-Kline", "role": "Managing Director", "company": "Advanced Energy United"},
    {"name": "Julian Spector", "role": "Senior Reporter", "company": "Canary Media"},
    {"name": "Chris Squitieri", "role": "Sr. Director, Power & Renewables Business Development", "company": "Encompass Energy Services"},
    {"name": "Mike Tabrizi", "role": "President / Chief Engineer", "company": "Zero-Emission Grid"},
    {"name": "Dylan Tansy", "role": "Executive Director", "company": "SunSpec Alliance"},
    {"name": "Michael Thomas", "role": "Founder and CEO", "company": "Cleanview"},
    {"name": "Bryan Thomas", "role": "CCPO", "company": "Stormentum"},
    {"name": "Nicole Tomasin", "role": "Sr. Director of Strategic Partnerships", "company": "Energy Access Innovations"},
    {"name": "Brian Turner", "role": "Senior Director, Western Regulatory", "company": "Advanced Energy United"},
    {"name": "Elizabeth Hughes", "role": "VP of Vehicle Grid Integration", "company": "The Mobility House"},
    {"name": "Brandt Vermillion", "role": "US Market Lead", "company": "Modo Energy"},
    {"name": "Spencer Wells", "role": "CEO", "company": "Wells Energy Development LLC"},
    {"name": "Eric Wesoff", "role": "Executive Director", "company": "Canary Media"},
    {"name": "Jonathan Whelan", "role": "Vice President of Onsite Energy", "company": "Optony Inc"},
    {"name": "Sean White", "role": "Solar Energy Professor/Consultant/Author", "company": "HeatSpring / White House Energy"},
    {"name": "Lynnae Willette", "role": "Director", "company": "EDF power solutions"},
    {"name": "Zach Woogen", "role": "Executive Director", "company": "Vehicle-Grid Integration Council (VGIC)"},
    {"name": "Julie Wright", "role": "President", "company": "(W)right On Communications"},
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
    for speaker in speakers:
        if speaker['name'].lower() not in existing:
            person = {
                "name": speaker['name'],
                "role": speaker['role'],
                "company": speaker['company'],
                "linkedin": None,
                "twitter": None,
                "category": "executive" if "CEO" in speaker['role'] or "President" in speaker['role'] or "Director" in speaker['role'] else "speaker",
                "source": "iesna_conference_speakers",
                "notes": f"Speaker at Intersolar & Energy Storage North America 2026"
            }
            f.write(json.dumps(person) + '\n')
            added += 1

print(f"Added {added} speakers from IESNA conference")
