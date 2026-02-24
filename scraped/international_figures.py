#!/usr/bin/env python3
"""Add international energy storage and clean energy figures"""

import json
from pathlib import Path

BASE_DIR = Path("/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage")

figures = [
    # European storage executives
    {"name": "Christoph Ostermann", "role": "Founder", "company": "Sonnen (Germany)", "category": "executive"},
    {"name": "Peter Carlsson", "role": "CEO", "company": "Northvolt (Sweden)", "category": "executive"},
    {"name": "Paolo Cerruti", "role": "Co-Founder", "company": "Northvolt", "category": "executive"},
    {"name": "Harald Mix", "role": "Co-Founder", "company": "Northvolt / Vargas", "category": "investor"},
    {"name": "Carl-Erik Lagercrantz", "role": "Co-Founder", "company": "Northvolt", "category": "executive"},
    {"name": "Lars Carlstrom", "role": "CEO", "company": "Italvolt", "category": "executive"},
    {"name": "Karlheinz Kaul", "role": "CEO", "company": "VARTA AG", "category": "executive"},
    {"name": "Herbert Schein", "role": "CEO", "company": "VARTA AG", "category": "executive"},
    {"name": "Michael Tojner", "role": "Chairman", "company": "VARTA AG", "category": "executive"},
    {"name": "Frank Blome", "role": "CEO", "company": "PowerCo (VW)", "category": "executive"},
    {"name": "Thomas Schmall", "role": "Board Member", "company": "Volkswagen", "category": "executive"},
    {"name": "Markus Duesmann", "role": "CEO", "company": "Audi", "category": "executive"},
    {"name": "Oliver Zipse", "role": "CEO", "company": "BMW", "category": "executive"},
    {"name": "Ola Källenius", "role": "CEO", "company": "Mercedes-Benz", "category": "executive"},
    
    # UK storage market
    {"name": "Matt Harper", "role": "Co-Founder", "company": "Invinity Energy Systems", "category": "executive"},
    {"name": "Larry Maybaum", "role": "CEO", "company": "Invinity Energy Systems", "category": "executive"},
    {"name": "Alex O'Cinneide", "role": "CEO", "company": "Gore Street Capital", "category": "executive"},
    {"name": "David Newman", "role": "Partner", "company": "Gresham House", "category": "investor"},
    {"name": "Ben Guest", "role": "Co-Founder", "company": "Gresham House BSI Fund", "category": "investor"},
    {"name": "Rupert Sherbrooke", "role": "CEO", "company": "Zenobe", "category": "executive"},
    {"name": "Steven Mayall", "role": "CEO", "company": "Zenobe", "category": "executive"},
    {"name": "Jonathan Sherbrooke", "role": "Co-Founder", "company": "Zenobe", "category": "executive"},
    {"name": "Tim le Pavoux", "role": "CEO", "company": "Harmony Energy", "category": "executive"},
    
    # Australian storage market
    {"name": "Louis de Sambucy", "role": "MD", "company": "Neoen Australia", "category": "executive"},
    {"name": "Xavier Barbaro", "role": "CEO", "company": "Neoen", "category": "executive"},
    {"name": "Romain Desrousseaux", "role": "Deputy CEO", "company": "Neoen", "category": "executive"},
    {"name": "Audrey Zibelman", "role": "Former CEO", "company": "AEMO", "category": "policy"},
    {"name": "Daniel Westerman", "role": "CEO", "company": "AEMO", "category": "policy"},
    {"name": "Miles George", "role": "CEO", "company": "Infigen Energy", "category": "executive"},
    {"name": "Ross Rolfe", "role": "CEO", "company": "Powerlink Queensland", "category": "executive"},
    
    # Asian storage market
    {"name": "Robin Zeng", "role": "Founder & Chairman", "company": "CATL", "category": "executive"},
    {"name": "Huang Shilin", "role": "Vice Chairman", "company": "CATL", "category": "executive"},
    {"name": "Zhou Jia", "role": "Vice President", "company": "CATL", "category": "executive"},
    {"name": "Wang Chuanfu", "role": "Founder & President", "company": "BYD", "category": "executive"},
    {"name": "Stella Li", "role": "EVP", "company": "BYD Americas", "category": "executive"},
    {"name": "Liyuan Li", "role": "VP", "company": "BYD", "category": "executive"},
    {"name": "Pan Jian", "role": "Chairman", "company": "EVE Energy", "category": "executive"},
    {"name": "Liu Jincheng", "role": "CEO", "company": "EVE Energy", "category": "executive"},
    {"name": "Li Ping", "role": "President", "company": "CALB", "category": "executive"},
    {"name": "Cui Dongshu", "role": "Secretary General", "company": "CPCA", "category": "policy"},
    {"name": "Robin Chen", "role": "VP", "company": "Gotion High-Tech", "category": "executive"},
    {"name": "Li Zhen", "role": "CEO", "company": "Gotion High-Tech", "category": "executive"},
    
    # Korean battery makers
    {"name": "Youngcho Chi", "role": "President & CIO", "company": "SK Group", "category": "executive"},
    {"name": "Dong-seob Jee", "role": "CEO", "company": "SK On", "category": "executive"},
    {"name": "Lee Won-hee", "role": "CEO", "company": "SK On", "category": "executive"},
    {"name": "Kim Dong-myung", "role": "CEO", "company": "LG Energy Solution", "category": "executive"},
    {"name": "Kwon Young-soo", "role": "CEO", "company": "LG Energy Solution", "category": "executive"},
    {"name": "Choi Yoon-ho", "role": "CEO", "company": "Samsung SDI", "category": "executive"},
    {"name": "Jun Young-hyun", "role": "CEO", "company": "Samsung SDI", "category": "executive"},
    
    # Japanese battery/storage
    {"name": "Kenichiro Yoshida", "role": "CEO", "company": "Sony", "category": "executive"},
    {"name": "Kazuo Tadanobu", "role": "President", "company": "Panasonic Energy", "category": "executive"},
    {"name": "Yuki Kusumi", "role": "CEO", "company": "Panasonic Holdings", "category": "executive"},
    {"name": "Allan Swan", "role": "EVP", "company": "Panasonic Energy of North America", "category": "executive"},
    {"name": "Masakazu Masujima", "role": "President", "company": "Toshiba ESS", "category": "executive"},
    
    # European energy agencies
    {"name": "Fatih Birol", "role": "Executive Director", "company": "IEA", "category": "policy"},
    {"name": "Laura Cozzi", "role": "Director of Sustainability", "company": "IEA", "category": "policy"},
    {"name": "Tim Gould", "role": "Chief Energy Economist", "company": "IEA", "category": "analyst"},
    {"name": "Francesco La Camera", "role": "Director General", "company": "IRENA", "category": "policy"},
    {"name": "Rabia Ferroukhi", "role": "Director", "company": "IRENA", "category": "policy"},
    {"name": "Dolf Gielen", "role": "Director", "company": "IRENA Innovation", "category": "researcher"},
    
    # European utilities
    {"name": "Jean-Bernard Lévy", "role": "Former CEO", "company": "EDF", "category": "executive"},
    {"name": "Luc Rémont", "role": "CEO", "company": "EDF", "category": "executive"},
    {"name": "Leonhard Birnbaum", "role": "CEO", "company": "E.ON", "category": "executive"},
    {"name": "Markus Krebber", "role": "CEO", "company": "RWE", "category": "executive"},
    {"name": "Michael Lewis", "role": "CEO", "company": "E.ON UK", "category": "executive"},
    {"name": "Ignacio Galán", "role": "CEO", "company": "Iberdrola", "category": "executive"},
    {"name": "Jose Ignacio Sánchez Galán", "role": "Executive Chairman", "company": "Iberdrola", "category": "executive"},
    {"name": "Francesco Starace", "role": "Former CEO", "company": "Enel", "category": "executive"},
    {"name": "Flavio Cattaneo", "role": "CEO", "company": "Enel", "category": "executive"},
    {"name": "Miguel Stilwell d'Andrade", "role": "CEO", "company": "EDP", "category": "executive"},
    {"name": "António Mexia", "role": "Former CEO", "company": "EDP", "category": "executive"},
    {"name": "Vincent de Rivaz", "role": "Former CEO", "company": "EDF UK", "category": "executive"},
    
    # Cleantech VCs / investors (international)
    {"name": "Martin Skancke", "role": "Chair", "company": "TCFD", "category": "investor"},
    {"name": "Mark Carney", "role": "UN Special Envoy", "company": "GFANZ / Brookfield", "category": "investor"},
    {"name": "Christiana Figueres", "role": "Former Executive Secretary", "company": "UNFCCC", "category": "policy"},
    {"name": "Patricia Espinosa", "role": "Former Executive Secretary", "company": "UNFCCC", "category": "policy"},
    {"name": "Simon Stiell", "role": "Executive Secretary", "company": "UNFCCC", "category": "policy"},
    {"name": "Laurence Tubiana", "role": "CEO", "company": "European Climate Foundation", "category": "policy"},
    {"name": "John Kerry", "role": "Former Special Envoy", "company": "US State Department", "category": "policy"},
    {"name": "John Podesta", "role": "Climate Envoy", "company": "US State Department", "category": "policy"},
    
    # International researchers
    {"name": "Michael Grubb", "role": "Professor", "company": "UCL Energy Institute", "category": "researcher"},
    {"name": "Jim Skea", "role": "Chair", "company": "IPCC", "category": "researcher"},
    {"name": "Hoesung Lee", "role": "Former Chair", "company": "IPCC", "category": "researcher"},
    {"name": "Valérie Masson-Delmotte", "role": "Co-Chair", "company": "IPCC Working Group I", "category": "researcher"},
    {"name": "Hans-Otto Pörtner", "role": "Co-Chair", "company": "IPCC Working Group II", "category": "researcher"},
    {"name": "Priyadarshi Shukla", "role": "Co-Chair", "company": "IPCC Working Group III", "category": "researcher"},
    {"name": "Jim Hansen", "role": "Professor", "company": "Columbia University", "category": "researcher"},
    {"name": "Michael Mann", "role": "Professor", "company": "University of Pennsylvania", "category": "researcher"},
    {"name": "Katharine Hayhoe", "role": "Professor", "company": "Texas Tech University", "category": "researcher"},
    {"name": "Gavin Schmidt", "role": "Director", "company": "NASA GISS", "category": "researcher"},
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
                "source": "manual_international_figures",
                "notes": "International energy storage / clean energy figure"
            }
            f.write(json.dumps(entry) + '\n')
            added += 1

print(f"Added {added} international figures")
