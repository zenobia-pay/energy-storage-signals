#!/usr/bin/env python3
"""Extract more Reddit usernames - batch 4 from high engagement posts."""
import json
from datetime import datetime

users_data = []

def add_user(username, subreddits=None, source_post=None):
    if username and username != "[deleted]" and not username.startswith("["):
        users_data.append({
            "username": username,
            "subreddits": subreddits or [],
            "source_post": source_post,
            "scraped_at": datetime.now().isoformat()
        })

# Users from r/Damnthatsinteresting California solar bill post
damn_solar_users = [
    "Mdizzle29", "BrokenXeno", "ben1481", "MDFan4Life", "chrissilich",
    "TriedCaringLess", "IWentHam", "Deathwatch72", "Luxpreliator", "LongJohnSelenium",
    "Excellent_Ad_3090", "melperz", "posthamster", "hamburgerstakes", "nickwhomer",
    "Stoopid-Stoner", "arcaninos", "CLANGALANGALANGA", "lobeline", "Gr33nanmerky13",
    "cajun_hammer", "oleada87", "trackdaybruh", "iamintheforest", "hmspain",
    "lordaddament", "Whole_Ad6438", "bebeco5912", "aDarkDarkNight", "Bulky-Fun-3108",
    "xplally1", "jh937hfiu3hrhv9", "Fangs_0ut", "gucknbuck", "JerryVanNuys",
    "Embarrassed_Alarm450", "NotJeff_Goldblum", "learn2die101", "Hax_", "heartwarriordad",
    "freddotu", "iiitme", "umop_aplsdn", "ElFarts", "flonky_guy", "mickifree12",
    "NinjahBob", "mckulty", "sweetlevels", "grandpassacaglia", "Jokeswithmito",
    "lothar74", "pinupcthulhu", "Clanmcallister", "JellyfishQuiet7944", "SnakeDoctor00",
    "therobshow", "jonesy422", "forakora", "braiker", "jumpyxwizard", "LaUNCHandSmASH",
    "cholnic", "imma_go_take_a_nap", "Lone_survivor87", "chorkinsrkewl",
    "mrjake777", "New_Awareness4075", "Justskatelala", "TobysGrundlee", "BondJames-Bond-007",
    "rusty1066", "dannydg17", "BlueJeansandWhiteTs", "CragMcBeard", "cool-beans-yeah",
    "mrbipty"
]

# Users from r/technology China solar post
tech_china_solar_users = [
    "chrisdh79", "WhiteRaven42", "defenestrate_urself", "the_snook", "jstam26",
    "blankarage", "Money-Ad-545", "WhereIsMyPancakeMix", "williafx", "Anastariana",
    "florinandrei", "Past-Direction9145", "tanstaafl90", "Bonerballs", "LiGuangMing1981",
    "kermityfrog2", "lgx", "KayItaly", "Darkstar197", "DavidBrooker", "JoshuaIAm",
    "StrangerNumerous5056", "Pupienus2theMaximus", "UBC145", "PoorFishKeeper",
    "ChrisDornerFanCorner", "TibiaKing", "shanghainese88", "LookAtYourEyes",
    "Seagull84", "IsThatAll", "mother_a_god", "Hive_Tyrant7", "avdpos",
    "2mustange", "blastradii", "MrTreize78", "alpharetroid", "Mr_YUP",
    "soulflaregm", "jnads", "simple_test", "tuc-eert", "SpanishMoleculo",
    "tanzmeister", "GeraltOfRivia2023", "tuckedfexas", "Old_Personality3136",
    "HotelKarma", "Wutang4TheChildren23", "gizamo", "kappakai", "powercow",
    "machbike", "PlayingTheWrongGame", "Worish", "Mental-Cut-8078", "Delphizer",
    "luk__", "AlsoInteresting"
]

# Users from r/technology Tesla Powerwall virtual power plant post
tech_tesla_vpp_users = [
    "mvea", "Aardvark_Man", "disgruntledpenguins", "iamdimpho", "ilikeme1",
    "Decyde", "Nyxtia", "president2016", "HisHolyNoodliness", "radixie",
    "BMStroh", "be-happier", "stealstea", "SlendyIsBehindYou", "hal2k1",
    "cursedTinker", "O_Heck", "Thehumblepiece", "GeorgePantsMcG", "cephas_rock",
    "JagerBaBomb", "uniptf", "VLDT", "murkush", "variaati0", "leeresgebaeude",
    "relevant__comment", "MaXxUser", "timelord09", "AEsirTro", "bennwalton",
    "eiketsujinketsu", "thegreenluple", "synergyiskey", "tlubz", "mad_bison",
    "mofobreadcrumbs", "asmodeanreborn", "WorldwideTauren", "Hunterbunter",
    "wgc123", "doggy_lipschtick", "JWGhetto", "stop_the_broats", "Mysticpoisen",
    "linh_nguyen", "perthguppy", "aahhii", "The_Rox", "ruetoesoftodney",
    "Dangerous-Dave", "GFandango", "SpanningForever", "engineerforthefuture",
    "judgej2", "Luckster36", "SicSevens", "brownyR31", "Mr_Reddit_Green",
    "binarygamer", "macadamiamin", "furto", "donaldtrumptwat", "tomdarch",
    "FearLeadsToAnger", "karma3000"
]

# Users from r/Futurology US molten salt battery post
futurology_molten_salt_users = [
    "lughnasadh", "DazzlingLeg", "Smedlington", "UnfinishedProjects", "twec21",
    "DmYouMyPenis", "Cantflyneedhelp", "Mounta1nK1ng", "MoogProg", "Tommix11",
    "Khutuck", "Digital_Human82", "TheDapperYank", "ElectrikDonuts", "PromiscuousMNcpl",
    "i_lost_my_password", "ajtrns", "LebronKDHGH", "victorvscn", "darkmatterisfun",
    "Humblebee89", "Mazzaroppi", "Dwarfdeaths", "TheRealLXC", "Wolfwillrule",
    "CrazyDudeWithATablet", "ronburgandyfor2016", "graveybrains", "aQuackInThePark",
    "pyrrhios", "John-D-Clay", "Future_Software5444", "fowlraul", "jj4211",
    "Xylomain", "pleasetrimyourpubes", "HellBlazer_NQ", "frothyundergarments",
    "Faysight", "Rik07", "NastyNugs", "cybercuzco", "Snibes1", "Gitmfap",
    "dylan21502", "Crackorjackzors", "MagicaItux", "goran_788", "chuckangel",
    "unskilledplay", "RollinThundaga", "Zarathustra30", "hedoeswhathewants",
    "Activehannes", "Tech_AllBodies", "Jamato-sUn", "NinjaKoala", "fricks_and_stones",
    "Party_Python", "ValyrianJedi", "Tepigg4444"
]

# Add all users
for u in damn_solar_users:
    add_user(u, ["Damnthatsinteresting"], source_post="california_solar_bill")
for u in tech_china_solar_users:
    add_user(u, ["technology"], source_post="china_solar_panels")
for u in tech_tesla_vpp_users:
    add_user(u, ["technology"], source_post="tesla_virtual_power_plant")
for u in futurology_molten_salt_users:
    add_user(u, ["Futurology"], source_post="molten_salt_battery")

# Write to JSONL
output_path = "/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage/reddit-users.jsonl"
with open(output_path, "a") as f:
    for user in users_data:
        f.write(json.dumps(user) + "\n")

print(f"Added {len(users_data)} users to {output_path}")
