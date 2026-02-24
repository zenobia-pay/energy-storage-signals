#!/usr/bin/env python3
"""Extract more Reddit usernames - batch 5 from massive posts."""
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

# Users from r/worldnews Norway phosphate post (64k upvotes, 3568 comments)
worldnews_norway_users = [
    "HelloSlowly", "That_random_guy-1", "throwaway490215", "Lower_Bullfrog_5138",
    "Phazon2000", "EmpTully", "MrPapillon", "GnarlyBear", "i_says_things",
    "batorbunko", "xSTSxZerglingOne", "PresumedSapient", "Nosferatatron",
    "PoL0", "screams_at_tits", "bjorna", "CrieDeCoeur", "sturla-tyr",
    "ForensicPathology", "Donigleus", "wirez62", "rugbyj", "explosiv_skull",
    "Freeloader_", "LastBite2901", "Hanzo_The_Ninja", "FuckFascismFightBack",
    "protomenace", "Hank_Heck", "BornBag8111", "CesarsWill", "lazy8s",
    "Orange-V-Apple", "immersemeinnature", "technicallynotlying", "Ok-Champ-5854",
    "brokenmcnugget", "mhkiwi", "ThanksToDenial", "Slaanesh_69", "swatsquat",
    "mukansamonkey", "IAmAQuantumMechanic", "tuort", "CQC_EXE", "DankVectorz",
    "itsjero", "3rdp0st", "Charming_Gift_9363", "Joseph20102011", "SEX_LIES_AUDIOTAPE",
    "vismundcygnus34", "Dreldan", "godtogblandet", "Laxxz", "BaronZhiro",
    "Rakgul", "Pumpkim", "Dr_barfenstein", "Zenadon"
]

# Users from r/Futurology EV battery longevity post
futurology_ev_battery_users = [
    "lunchboxultimate01", "Upset_Ant2834", "Hazel-Rah", "hlessi_newt", "mccoyn",
    "ThePromptWasYourName", "1200____1200", "NeedleArm", "GrynaiTaip", "series_hybrid",
    "BananaPalmer", "Fraegtgaortd", "thatguy425", "VikingBorealis", "shanebayer",
    "3DprintRC", "farmthis", "mr_clark1983", "AxemanACL", "Killfile",
    "Imnotkleenex", "Jesta23", "mobrocket", "firefighter26s", "rsta223",
    "Unhappy_Hedgehog_808", "born_again_atheist", "furry-borders", "TobysGrundlee",
    "murphymc", "opaz", "Disastrous-One7789", "chereddit", "Ancient_Persimmon",
    "GrunchWeefer", "wileecoyote1969", "couldbemage", "roamingandy",
    "Down_To_My_Last_Fuck", "kingmins", "afbmonk", "uncanny_mac", "AgentScreech",
    "N3rdProbl3ms", "psi-", "JimJam28", "ensoniq2k", "skwint", "orlyokthen",
    "HumpinPumpkin", "jaam01", "Gr33nbastrd", "whachamacallme", "Cedric_T",
    "Dez_Champs", "Thmelly_Puthy", "Andyb1000", "lecollectionneur"
]

# Users from search results for EV posts
ev_search_users = [
    "sg_plumber", "dannybluey", "Forward-Answer-4407", "citytiger", "ninadmg",
    "altmorty", "IntrepidGentian", "callsonreddit", "Wagamaga", "davidwholt",
    "Fwoggie2", "mistakes_maker", "Pastor_Richardian", "Sorin61", "SirOhsisOfTheLiver",
    "Epicurus-fan", "pnewell", "thispickleisntgreen", "PortableSunOfficial",
    "IndividualRevenue995", "Infamous_Spite_7715", "segasega89", "DragonflyNo6921"
]

# Add all users
for u in worldnews_norway_users:
    add_user(u, ["worldnews"], source_post="norway_phosphate")
for u in futurology_ev_battery_users:
    add_user(u, ["Futurology"], source_post="ev_battery_longevity")
for u in ev_search_users:
    add_user(u, ["various"], source_post="ev_solar_search")

# Write to JSONL
output_path = "/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage/reddit-users.jsonl"
with open(output_path, "a") as f:
    for user in users_data:
        f.write(json.dumps(user) + "\n")

print(f"Added {len(users_data)} users to {output_path}")
