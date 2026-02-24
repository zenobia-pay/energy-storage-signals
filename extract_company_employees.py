#!/usr/bin/env python3
"""Extract company employees from existing scraped data for energy storage companies."""

import json
import re
from pathlib import Path

# Target companies (normalized lowercase for matching)
TARGET_COMPANIES = {
    # Battery/Cell Manufacturers
    'catl': 'CATL',
    'contemporary amperex': 'CATL',
    'byd': 'BYD',
    'lg energy': 'LG Energy',
    'lg chem': 'LG Energy',
    'lgensol': 'LG Energy',
    'samsung sdi': 'Samsung SDI',
    'panasonic': 'Panasonic',
    'sk on': 'SK On',
    'sk innovation': 'SK On',
    'aesc': 'AESC',
    'envision aesc': 'AESC',
    # ESS Integrators
    'fluence': 'Fluence',
    'tesla': 'Tesla Energy',
    'tesla energy': 'Tesla Energy',
    'sungrow': 'Sungrow',
    'wartsila': 'Wärtsilä',
    'wärtsilä': 'Wärtsilä',
    'powin': 'Powin',
    'ess inc': 'ESS Inc',
    'ess tech': 'ESS Inc',
    # Utilities
    'nextera': 'NextEra Energy',
    'nextera energy': 'NextEra Energy',
    'fpl': 'NextEra Energy',
    'florida power': 'NextEra Energy',
    'duke energy': 'Duke Energy',
    'duke': 'Duke Energy',
    'southern company': 'Southern Company',
    'georgia power': 'Southern Company',
    'aes': 'AES',
    'aes corporation': 'AES',
    'enel': 'Enel',
    'dominion': 'Dominion Energy',
    'dominion energy': 'Dominion Energy',
    # Developers
    'plus power': 'Plus Power',
    'pluspower': 'Plus Power',
    'jupiter power': 'Jupiter Power',
    'key capture': 'Key Capture Energy',
    'key capture energy': 'Key Capture Energy',
    'broad reach': 'Broad Reach Power',
    'broad reach power': 'Broad Reach Power',
    # Consultants
    'wood mackenzie': 'Wood Mackenzie',
    'woodmac': 'Wood Mackenzie',
    'bloombergnef': 'BloombergNEF',
    'bnef': 'BloombergNEF',
    'bloomberg nef': 'BloombergNEF',
    'guidehouse': 'Guidehouse',
    'navigant': 'Guidehouse',  # Guidehouse acquired Navigant
    'icf': 'ICF',
    # Material Suppliers
    'albemarle': 'Albemarle',
    'sqm': 'SQM',
    'livent': 'Livent',
    # Additional energy storage companies
    'redwood materials': 'Redwood Materials',
    'form energy': 'Form Energy',
    'eos energy': 'Eos Energy',
    'quantumscape': 'QuantumScape',
    'solid power': 'Solid Power',
    'electric era': 'Electric Era Technologies',
    'amprius': 'Amprius',
    'ion storage': 'ION Storage Systems',
    'energy vault': 'Energy Vault',
    'stem': 'Stem Inc',
    'stem inc': 'Stem Inc',
    'freyr': 'FREYR Battery',
    'northvolt': 'Northvolt',
    'american battery': 'American Battery Technology',
    'nrg': 'NRG Energy',
    'vistra': 'Vistra',
    'calpine': 'Calpine',
    'orsted': 'Ørsted',
    'rwe': 'RWE',
    'iberdrola': 'Iberdrola',
    'engie': 'ENGIE',
    'strata solar': 'Strata Clean Energy',
    'strata clean': 'Strata Clean Energy',
    '8minute': '8minute Solar Energy',
    'invenergy': 'Invenergy',
    'recurrent': 'Recurrent Energy',
    'longroad': 'Longroad Energy',
    'intersect power': 'Intersect Power',
    'pine gate': 'Pine Gate Renewables',
}

def normalize_company(company_str):
    """Match company string to target companies."""
    if not company_str:
        return None
    company_lower = company_str.lower().strip()
    for key, normalized in TARGET_COMPANIES.items():
        if key in company_lower:
            return normalized
    return None

def extract_from_people():
    """Extract from people.jsonl."""
    employees = []
    try:
        with open('people.jsonl', 'r') as f:
            for line in f:
                try:
                    person = json.loads(line.strip())
                    company = person.get('company', '')
                    normalized = normalize_company(company)
                    if normalized:
                        employees.append({
                            'name': person.get('name', ''),
                            'company': normalized,
                            'title': person.get('title', ''),
                            'source': person.get('source', 'people.jsonl')
                        })
                    # Also check bio for company mentions
                    bio = person.get('bio', '')
                    if bio and not normalized:
                        normalized = normalize_company(bio)
                        if normalized:
                            employees.append({
                                'name': person.get('name', ''),
                                'company': normalized,
                                'title': person.get('title', ''),
                                'source': person.get('source', 'people.jsonl')
                            })
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass
    return employees

def extract_from_twitter():
    """Extract from twitter-accounts.jsonl."""
    employees = []
    try:
        with open('twitter-accounts.jsonl', 'r') as f:
            for line in f:
                try:
                    account = json.loads(line.strip())
                    bio = account.get('bio', '')
                    normalized = normalize_company(bio)
                    if normalized:
                        employees.append({
                            'name': account.get('name', ''),
                            'company': normalized,
                            'title': '',
                            'source': f"twitter.com/{account.get('handle', '')}"
                        })
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass
    return employees

def extract_from_github():
    """Extract from github-users.jsonl."""
    employees = []
    try:
        with open('github-users.jsonl', 'r') as f:
            for line in f:
                try:
                    user = json.loads(line.strip())
                    company = user.get('company', '')
                    normalized = normalize_company(company)
                    if normalized:
                        employees.append({
                            'name': user.get('name', '') or user.get('login', ''),
                            'company': normalized,
                            'title': '',
                            'source': f"github.com/{user.get('login', '')}"
                        })
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass
    return employees

def extract_from_podcast_people():
    """Extract from podcast-people.jsonl."""
    employees = []
    try:
        with open('podcast-people.jsonl', 'r') as f:
            for line in f:
                try:
                    person = json.loads(line.strip())
                    company = person.get('company', '') or person.get('affiliation', '')
                    normalized = normalize_company(company)
                    if normalized:
                        employees.append({
                            'name': person.get('name', ''),
                            'company': normalized,
                            'title': person.get('title', ''),
                            'source': person.get('source', 'podcast-people.jsonl')
                        })
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass
    return employees

def extract_from_government():
    """Extract from government-people.jsonl."""
    employees = []
    try:
        with open('government-people.jsonl', 'r') as f:
            for line in f:
                try:
                    person = json.loads(line.strip())
                    company = person.get('organization', '') or person.get('company', '')
                    normalized = normalize_company(company)
                    if normalized:
                        employees.append({
                            'name': person.get('name', ''),
                            'company': normalized,
                            'title': person.get('title', ''),
                            'source': person.get('source', 'government-people.jsonl')
                        })
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        pass
    return employees

def main():
    all_employees = []
    
    # Extract from all sources
    print("Extracting from people.jsonl...")
    all_employees.extend(extract_from_people())
    
    print("Extracting from twitter-accounts.jsonl...")
    all_employees.extend(extract_from_twitter())
    
    print("Extracting from github-users.jsonl...")
    all_employees.extend(extract_from_github())
    
    print("Extracting from podcast-people.jsonl...")
    all_employees.extend(extract_from_podcast_people())
    
    print("Extracting from government-people.jsonl...")
    all_employees.extend(extract_from_government())
    
    # Deduplicate by name + company
    seen = set()
    unique_employees = []
    for emp in all_employees:
        key = (emp['name'].lower().strip(), emp['company'])
        if key not in seen and emp['name']:
            seen.add(key)
            unique_employees.append(emp)
    
    # Write to company-employees.jsonl
    print(f"\nWriting {len(unique_employees)} employees to company-employees.jsonl...")
    with open('company-employees.jsonl', 'a') as f:  # Append to existing
        for emp in unique_employees:
            f.write(json.dumps(emp) + '\n')
    
    # Count by company
    company_counts = {}
    for emp in unique_employees:
        company = emp['company']
        company_counts[company] = company_counts.get(company, 0) + 1
    
    # Write companies.jsonl
    print("Writing companies.jsonl...")
    with open('companies.jsonl', 'w') as f:
        for company, count in sorted(company_counts.items(), key=lambda x: -x[1]):
            f.write(json.dumps({
                'company': company,
                'type': get_company_type(company),
                'employee_count': count
            }) + '\n')
    
    # Print summary
    print("\n=== COMPANY EMPLOYEE COUNTS ===")
    for company, count in sorted(company_counts.items(), key=lambda x: -x[1]):
        print(f"  {company}: {count}")
    print(f"\nTotal unique employees: {len(unique_employees)}")

def get_company_type(company):
    """Get company type/category."""
    manufacturers = ['CATL', 'BYD', 'LG Energy', 'Samsung SDI', 'Panasonic', 'SK On', 'AESC', 'Northvolt', 'FREYR Battery']
    integrators = ['Fluence', 'Tesla Energy', 'Sungrow', 'Wärtsilä', 'Powin', 'ESS Inc', 'Stem Inc', 'Energy Vault']
    utilities = ['NextEra Energy', 'Duke Energy', 'Southern Company', 'AES', 'Enel', 'Dominion Energy', 'NRG Energy', 'Vistra']
    developers = ['Plus Power', 'Jupiter Power', 'Key Capture Energy', 'Broad Reach Power', 'Invenergy', 'Intersect Power']
    consultants = ['Wood Mackenzie', 'BloombergNEF', 'Guidehouse', 'ICF']
    materials = ['Albemarle', 'SQM', 'Livent', 'Redwood Materials']
    
    if company in manufacturers:
        return 'Battery/Cell Manufacturer'
    elif company in integrators:
        return 'ESS Integrator'
    elif company in utilities:
        return 'Utility'
    elif company in developers:
        return 'Developer'
    elif company in consultants:
        return 'Consultant'
    elif company in materials:
        return 'Material Supplier'
    else:
        return 'Energy Storage'

if __name__ == '__main__':
    main()
