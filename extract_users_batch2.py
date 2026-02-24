#!/usr/bin/env python3
"""Extract more Reddit usernames from scraped data - batch 2."""
import json
from datetime import datetime

users_data = []

def add_user(username, subreddits=None, karma=None, source_post=None):
    if username and username != "[deleted]" and not username.startswith("["):
        users_data.append({
            "username": username,
            "subreddits": subreddits or [],
            "karma": karma,
            "source_post": source_post,
            "scraped_at": datetime.now().isoformat()
        })

# Users from r/Futurology battery price posts
futurology_battery_users = [
    "IntrepidGentian", "kosherbeans123", "Rodman930", "ceelogreenicanth",
    "greenskinmarch", "oandakid718", "UnifiedQuantumField", "WazWaz",
    "gomurifle", "Tribe303", "oneupme", "Gravitationsfeld", "ElektricEel",
    "Necoras", "ra1kk", "zkareface", "Etzix", "megaman821", "BrokkelPiloot",
    "mur-diddly-urderer", "Valuable_Associate54", "Optimistic-Bob01",
    "AlsoInteresting", "CryptikTwo", "Rage_Like_Nic_Cage", "unskilledplay",
    "Elsa_the_Archer", "West-Abalone-171", "DHFranklin", "farticustheelder",
    "agitatedprisoner", "Malawi_no", "jermain31299", "merryman1", "Sol3dweller",
    "DARKFiB3R", "ssylvan", "thodgson", "Rusty_Flutes", "vergorli",
    "Irisgrower2", "leaky_wand", "Subject-Career", "potat_infinity",
    "johannthegoatman", "GuqJ", "Valuable_Associate54", "Taqueria_Style",
    "BaQstein_", "Whiterabbit__", "lookamazed", "Hendlton", "OverSoft",
    "ARunningGuy", "Thesource674", "cavedave", "Roadkill997", "lurksAtDogs",
    "Baud_Olofsson", "BasvanS", "amicaze", "Joddodd", "likewut",
    "NonorientableSurface", "bfire123", "danyyyel", "Altruistic_Bell7884",
    "IpppyCaccy", "barder83", "eazy2x", "globalartwork", "ca1ibos", "Crenorz",
    "reddituseronebillion", "lazyFer", "aitorbk", "Think_Discipline_90",
    "Amazing-Mirror-3076", "Apprehensive_Air_940", "Mawootad", "Voidoli",
    "PitPost", "Freethecrafts", "testtdk", "Aelig_", "CouldBeMaybeIDK",
    "grambell789", "afurtivesquirrel", "CrunchingTackle3000", "timmg",
    "reelnigra", "PlaidPCAK", "chrisni66"
]

# Users from r/UpliftingNews China CO2 post
china_co2_users = [
    "johnn48", "secretdrug", "CaptainAsshat", "ErlendJ", "Morgannin09",
    "mouse_Brains", "Churchbushonk", "nauticalsandwich", "bug-hunter",
    "zer1223", "NotSovietSpy", "publicdefecation", "C45", "PersevereSwifterSkat",
    "LaughableIKR", "ph0on", "mragusa2", "BrotherRoga", "Jair-F-Kennedy",
    "RoRuRee", "Habba", "comeatmefrank", "ssthehunter", "FuttleScish",
    "rabbitwonker", "Mattbl", "DanteChurch", "siposbalint0", "sth128",
    "Key-Line5827", "braapstututu", "LeanderT", "Asrahn", "BlackWindBears",
    "throwawaynewc", "FartingBob", "JK_NC", "bongsforhongkong",
    "stdstaples", "Deurbel2222", "thetreat", "Multidream", "FinsFan305",
    "Dr_Jabroski", "wwarnout", "UncleSlim", "Sxualhrssmntpanda",
    "RagingTeenHormones", "FairDinkumMate", "ablacnk", "icelandichorsey",
    "PotatoesWillSaveUs", "Havanatha_banana", "No_Mercy_4_Potatoes",
    "Jarms48", "splashjlr", "PlasticExtreme4469", "PieInTheSkyNet",
    "0vl223", "Kryomon", "whydoyouneedanamenow", "MrHanfblatt",
    "AutisticGayBlackJew", "throwaway12junk", "Deatheturtle", "Supershadow30",
    "FriendshipNRainbows", "Cinnamon_Sauce", "Ulyks", "emmettiow",
    "Scottacus__Prime", "scorpions411", "melpheos", "Vozer_bros",
    "zobotrombie", "Lumbergh7"
]

# More users from $63/kWh battery storage post
battery_storage_users = [
    "Dullwittedfool", "Reddit-runner", "Valuable_Associate54", 
    "CharredWelderGuy", "Sieve-Boy", "nitePhyyre", "_CMDR_", "Kamizar"
]

# Add all users
for u in futurology_battery_users:
    add_user(u, ["Futurology"], source_post="battery_prices_china")
for u in china_co2_users:
    add_user(u, ["UpliftingNews"], source_post="china_co2_flat")
for u in battery_storage_users:
    add_user(u, ["Futurology"], source_post="63kwh_battery_storage")

# Write to JSONL
output_path = "/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage/reddit-users.jsonl"
with open(output_path, "a") as f:
    for user in users_data:
        f.write(json.dumps(user) + "\n")

print(f"Added {len(users_data)} users to {output_path}")
