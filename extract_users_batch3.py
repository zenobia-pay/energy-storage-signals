#!/usr/bin/env python3
"""Extract more Reddit usernames - batch 3."""
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

# Users from r/wallstreetbets Ford EV post
wsb_ford_users = [
    "toydan", "varyingopinions", "Budget-Ocelots", "tunisia3507", "ShoulderPainCure",
    "DukeofNormandy", "StonedBooty", "hackjob", "BGM1988", "707e", "Aidrox",
    "RedditsFullofShit", "Nice_Marmot_7", "raz-0", "gorram1mhumped", "Brashagent",
    "flexonyou97", "HereForTheComments57", "malfane", "anachronofspace", "sneaky-pizza",
    "novwhisky", "1badh0mbre", "zzedisonzz", "ResidentComplaint19", "TritiumNZlol",
    "rajinis_bodyguard", "TheSeedLied", "FeverTreeCloud", "NuclearPopTarts",
    "No-Breakfast-8154", "friendshabitsfamily", "Kismet-IT", "BoozyMcBoozehound",
    "ea9ea", "craiginphoenix", "ChaseballBat", "Whatstrendynow", "R12Labs",
    "PrimeIntellect", "DBTroll", "ohlayohlay", "your_grandmas_FUPA", "blurfgh",
    "aeric67", "mermaidhunter42", "Southern-Garbage6226", "RJ5R", "bsiu",
    "insidiousfruit", "PM_Me_Titties-n-Ass", "babybunny1234", "FewHorror1019",
    "Curious-Package-9429", "bsmitty358", "FakeTunaFromSubway", "Responsible-Mail2558",
    "BringbacktheFocusRS", "xDarknal", "EsotericSpaceBeaver", "ANewOddity",
    "GrumblyData3684", "hv876", "Clear-Fan7963", "PresidentKraznov", "westside222",
    "HoweHaTrick", "UFuked", "steave44", "RockyPi", "packpride85", "Ohgodwatdoplshelp",
    "juiced911", "djsmith89", "veerKg_CSS_Geologist", "SuperConfused", "liftingshitposts",
    "LeaderElectrical8294", "Thiswas2hard", "engi-nerd_5085", "eldelshell",
    "redditmodsRrussians", "Suspended-Again", "DaStompa", "J3diMind", "XSC",
    "man_lizard", "IThinkRightLeft", "timshel_life", "ThatLooksRight", "baneofthesmurf",
    "ExtraSmooth", "Euler007", "MotoEnduro", "L3g3ndary-08", "Halefire", "elysiansaurus"
]

# Users from r/singularity 5D glass storage post
singularity_glass_users = [
    "BuildwithVignesh", "ThunderBeanage", "ceramicatan", "QLaHPD", "Right-Hall-6451",
    "machyume", "Anen-o-me", "DrPoontang", "Chop1n", "AndrewH73333", "attempt_number_3",
    "kowdermesiter", "RonocNYC", "KaleidoscopeFar658", "Saalor100", "Savings_Midnight_555",
    "des_the_furry", "Pop-Huge", "JackInSights", "gofilterfish", "bigsmokaaaa",
    "AccountOfMyAncestors", "johnjmcmillion", "Intelligent-Rule-397", "uniquelyavailable",
    "larswo", "Sterling_-_Archer", "strange_geometer", "odc100", "KarlHungas",
    "Trotskyist", "PM_Me_Your_Deviance", "Fast-Satisfaction482", "Ormusn2o", "subdep",
    "Seidans", "Choice_Isopod5177", "PandorasBoxMaker", "WhisperFray", "IronWhitin",
    "TRoLolo-_-", "zero0n3", "BenevolentCheese", "CoffeeSnakeAgent", "TheOnlyFallenCookie",
    "baseketball", "MydnightWN", "LimiDrain", "ps-PxL", "FoeHammer99099", "egg_breakfast",
    "anonuemus", "AmusingVegetable", "DigSignificant1419", "alternative5", "mocityspirit",
    "MyDogIsCalledMilo", "0x077777", "redfacedquark", "merlin211111", "flavorfox",
    "herpetic-whitlow", "ServeAlone7622", "giYRW18voCJ0dYPfz21V", "Lopsided_Army6882",
    "barrygateaux", "Original_Sedawk", "Electrical_Rabbit_88", "ArmNo7463", "lastcallhall",
    "Probodyne", "u_3WaD", "GatePorters", "sirtrogdor", "chosen_zero", "redit3rd",
    "morphemass", "theresapattern"
]

# Users from search results
search_result_users = [
    "PanzerWatts", "lughnasadh", "snooshoe"
]

# Add all users
for u in wsb_ford_users:
    add_user(u, ["wallstreetbets"], source_post="ford_ev_pivot")
for u in singularity_glass_users:
    add_user(u, ["singularity"], source_post="5d_glass_storage")
for u in search_result_users:
    add_user(u, ["Futurology", "OptimistsUnite", "tech"], source_post="lithium_grid_search")

# Write to JSONL
output_path = "/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage/reddit-users.jsonl"
with open(output_path, "a") as f:
    for user in users_data:
        f.write(json.dumps(user) + "\n")

print(f"Added {len(users_data)} users to {output_path}")
