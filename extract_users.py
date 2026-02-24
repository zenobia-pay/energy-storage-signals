#!/usr/bin/env python3
"""Extract Reddit usernames from scraped data and save to JSONL."""
import re
import json
import sys
from datetime import datetime

# All users collected from scraping
users_data = []

def add_user(username, subreddits=None, karma=None, source_post=None, comment_text=None):
    """Add a user to the collection."""
    if username and username != "[deleted]" and not username.startswith("["):
        users_data.append({
            "username": username,
            "subreddits": subreddits or [],
            "karma": karma,
            "source_post": source_post,
            "comment_text": comment_text[:500] if comment_text else None,
            "scraped_at": datetime.now().isoformat()
        })

# Users from r/energy posts
energy_users = [
    "mafco", "Economy-Fee5830", "404mediaco", "Simpleximo", "InsaneSnow45",
    "New-Grapefruit-7467", "arcgiselle", "sksarkpoes3", "Pale_Masterpiece4466",
    "Edinbatteries", "LingonberryUpset482", "Ok-Revenue-8223", "FullMoonBurning",
    "cabs84", "Phil_Timmons", "spinelssinvrtebrate", "Stunning-Use-7052",
    "MisterMofoSFW", "25TiMp", "bfire123", "aquarain", "Ateist", "Ok_Calligrapher8165",
    "Luxpreliator", "MPeters43", "SupermarketIcy4996", "myaaa_tan",
    "EnvironmentalRound11", "Mradr", "skwirly715", "tommysteakbone", "animatedb",
    "Savings-Particular-9", "Hefforama", "jemicarus", "Appropriate-Art-829",
    "howtoreadspaghetti", "Aranthos-Faroth", "HowHoward", "NegativeSemicolon",
    "CriticalUnit", "JBe4r", "d57heinz", "EnergyResearch28484", "tmac4969",
    "Kaurifish", "RichardsLeftNipple", "Grand_False", "RandomWorthlessDude",
    "Space_Monkey_42", "Obvious-Project-1186", "davidellis23", "TheSherlockCumbercat",
    "steffur", "UpperAd5715", "immigrantviking", "ours", "freedomgeek",
    "ginger_and_egg", "Schemen123", "throwawaynl001", "PmMeYourBestComment",
    "NotAcutallyaPanda", "Bontus", "iqisoverrated", "MarianCostabrava",
    "Sarcastic-Potato", "Tinosdoggydaddy", "thegreatpotatogod", "I_gotcha_again",
    "Emotional_Fact_7672", "3knuckles", "Any-Information6261", "corgi-king",
    "manzanita2", "GranPino", "OveVernerHansen", "marmaviscount",
    "Lopsided_Quarter_931", "OkTry9715", "negetivex", "121310", "wtfduud",
    "roygbivasaur", "youstillhavehope", "Particular_Ticket_20", "rellett",
    "Low-Rip3678", "cogit4se", "krakenbear", "CRoss1999", "GunterVonBloom",
    "unique3", "ol-gormsby"
]

# Users from r/UpliftingNews California battery storage post
upliftingnews_users = [
    "sg_plumber", "CDN-Social-Democrat", "ProStrats", "kinboyatuwo",
    "the_quark", "PiccoloAwkward465", "AnomalyFriend", "vineyardmike",
    "Stiggalicious", "Illustrious_Read8038", "justwantedtoview", "Dear_Chasey_La1n",
    "So_HauserAspen", "know_limits", "joemaniaci", "Marston_vc", "rocket_randall",
    "GuyanaFlavorAid", "Agent-Blasto-007", "pagerussell", "Many_Advice_1021",
    "seattleJJFish", "jedi2155", "destructormuffin", "Mr_Salmon_Man", "MIT_Engineer",
    "angels_exist_666", "Katyafan", "Roflkopt3r", "gruey", "Lfsnz67", "livious1",
    "Brok3n_", "JJAsond", "Rabidschnautzu", "vahntitrio", "p00p3rz", "92373",
    "Melicor", "StephTheBot", "kn3cht", "EastwoodBrews", "inthegarden5",
    "Cake-Over", "ceelogreenicanth", "JRR_Tokin54", "bell-town", "maciver6969",
    "Swingerella", "blade740", "iHeartmydogsHead", "Drewggles", "Alucard661",
    "foster-child", "RusefoxGhost", "ConfessSomeMeow", "xjeeper", "anonyfool",
    "cpufreak101", "BigAcanthocephala637", "OhGr8WhatNow", "SaltyDogBill",
    "Valuable-Building446", "Playful-Appearance56", "cloudncali", "Itsalive555",
    "thelingeringlead", "Pikeman212a6c", "xFirnen", "fiqar", "rusty_programmer",
    "Terseity", "istirling01", "ScottE77", "h3adbangerboogie", "beermaker",
    "swenbearswen", "itskdog", "WoodyTheWorker", "jelloslug", "drftwdtx",
    "Jolly_Ad2446", "Prohibitorum", "MrdnBrd19", "tlmw2001", "spitdragon2",
    "10thflrinsanity", "Meanteenbirder", "Valuable_Ad_4916", "Deemarvelousone",
    "Appleslicer", "mrdavidrt", "AJDillonsThirdLeg", "bitwise97"
]

# Users from r/Futurology Oxford University clean energy post
futurology_users = [
    "lughnasadh", "facherone", "jon_010", "bdcp", "dosedatwer", "noelcowardspeaksout",
    "RCMW181", "granular_quality", "Yasirbare", "count023", "1fastdak",
    "nonzeroday_tv", "kevlarbuns", "Darryl_Lict", "interpellation", "Rocinante-25",
    "mypetclone", "Imatwork12", "benmck90", "Osato", "Aethelric", "deck_hand",
    "daperson1", "LeCrushinator", "dedicated-pedestrian", "dos8s", "fiesta-pantalones",
    "m12345n", "googlemehard", "helm", "aphinity_for_reddit", "Luxalpa",
    "riskinhos", "goodsam2", "b2ct", "WorkO0", "FirstPlebian", "PiersPlays",
    "Gordon_Explosion", "bad_lurker_", "zenconkhi", "HecateEreshkigal",
    "realbigbob", "LeastCoordinatedJedi", "minimix18", "AllenKll", "BenderRodriquez",
    "revax", "Cloaked42m", "GreatBigJerk", "auramancer1247", "CaptainCupcakez",
    "MrMike", "nitekroller", "FromBeyond", "tarkadahl", "diamond"
]

# Users from r/science lithium-sulphur battery post
science_users = [
    "mvea", "MacAndShits", "uber1337h4xx0r", "gbrahah", "_jumpstoconclusions_",
    "supified", "Mike312", "JoeBidensLegHair", "WhyHulud", "HaloHowAreYa",
    "KingVolsung", "qwert45", "physics515", "salgat", "Huge-Yakmen", "demintheAF",
    "havinit", "longdrivehome", "Dag-nabbitt", "PineappleBoots", "nxcrosis",
    "DaoFerret", "Dethraivn", "AMSolar", "IAmNotNathaniel", "lightofthehalfmoon",
    "thisnameismeta", "mlsandahl", "Dragon_Fisting", "victoryhonorfame", "omniuni",
    "gomurifle", "AxeLond", "RandomizedRedditUser", "THICC_DICC_PRICC",
    "reddit25", "TheBlack_Swordsman", "xatava", "m4potofu", "boforbojack",
    "DASK", "im_a_dr_not_", "_teslaTrooper", "cancerousiguana", "Rubythief",
    "nebulousmenace", "OSKSuicide", "Toxic_Planet", "m-p-3", "DoubleWagon",
    "Apollo_Wolfe", "ReasonablyBadass", "Flextt", "Dydey", "MrTobor99"
]

# Users from r/energy sodium ion CATL post
catl_users = [
    "Notevenstreaming", "Vegetable_Ad6075", "Splenda", "Another_Slut_Dragon",
    "Pyroburner", "Express_Position5624", "Competitive-Tap-6111", "CoolBadDad71",
    "cstlyi", "nplant", "AdvancedBattle1503", "GlitteringLock9791",
    "GlitchInTheMatrix5", "SirWillae", "MOBrierley", "chris92315", "Known_Lack_7262",
    "MotelSans17", "AdNo2342", "Jared_Usbourne", "S7LEVIN_SHAFE7", "NJdestroyed",
    "jeterix7387", "tyranicalteabagger", "Broken_Atoms", "davidm2232", "Myjunkisonfire",
    "Own_Situation7316", "lastofthevegas", "sancho_sk", "EventAccomplished976",
    "vjjiiihhvv", "timohtea", "zero0n3", "csukoh78", "dinosaurkiller", "Muffinateher",
    "PSYCHOMETRE", "onetimeataday", "Gold_Map_236", "randomOldFella", "gododium",
    "iqisoverrated", "Hour_Bit_5183", "donpurrito", "LithoSlam", "jrbuck95",
    "Eastern37", "AmusingVegetable", "TheS4ndm4n", "Deep_Car4658", "ThroatEducational271",
    "ketamarine", "West-Abalone-171", "gljames24", "Dhegxkeicfns", "thallazar",
    "MonoMcFlury", "obanite", "leoyoung1", "Beiben", "CriticalUnit", "Tesseract91",
    "NetZeroDude", "chfp"
]

# Users from r/solar posts
solar_users = [
    "v4ss42", "Absolutelynotpolice", "Open-Reveal3378", "yankinwaoz",
    "Embarrassed_Top9480", "thinkB4WeSpeak", "terppatyyppi", "Glow350",
    "Western-Kiwi3798", "heyjatin", "pithy-pants", "insight_energy"
]

# Users from r/electricvehicles posts
ev_users = [
    "Roux_My_Burgundy", "RuggedHank", "magenta_placenta", "b0b3rman",
    "Dandaban", "farrrtttttrrrrrrrrtr", "ApprehensiveSize7662", "SpriteZeroY2k",
    "SapphosLemonBarEnvoy"
]

# Users from r/EnergyStorage posts
energystorage_users = [
    "Edinbatteries", "LostSoul5", "SolarAllTheWayDown", "Legitimate-Interest5",
    "Life-Strategy4490", "Impossible-Face-2673", "PolyNode_2030",
    "modelmakereditor", "KoopChantal1", "EducationalMango1320", "Vailhem"
]

# Users from r/batteries posts
batteries_users = [
    "Effective_Pool_3050", "Stoical69", "catboy519", "Sea-Anxiety6491",
    "Stepho_62", "voidarix", "Square-Singer", "supermariofunshine",
    "Fuzzy_Accident666", "Divisible_by_0"
]

# Users from r/renewable and r/sustainability
sustainability_users = [
    "randolphquell", "LivingMoreWithLess", "James_Fortis", "Sauerkrautkid7",
    "abcnews_au", "King-Meister", "Sentient_Media", "InspecteurC",
    "Low-Elevator2850", "team_pv", "Milanakiko", "prototyperspective",
    "naiveshit", "CanadianDoc2019", "Max_Arbuzov", "Chartlecc", "renewable_insights"
]

# Add all users
for u in energy_users:
    add_user(u, ["energy"], source_post="energy_various")
for u in upliftingnews_users:
    add_user(u, ["UpliftingNews"], source_post="california_battery_storage")
for u in futurology_users:
    add_user(u, ["Futurology"], source_post="oxford_clean_energy")
for u in science_users:
    add_user(u, ["science"], source_post="lithium_sulphur_battery")
for u in catl_users:
    add_user(u, ["energy"], source_post="catl_sodium_ion")
for u in solar_users:
    add_user(u, ["solar"], source_post="solar_posts")
for u in ev_users:
    add_user(u, ["electricvehicles"], source_post="ev_posts")
for u in energystorage_users:
    add_user(u, ["EnergyStorage"], source_post="energystorage_posts")
for u in batteries_users:
    add_user(u, ["batteries"], source_post="batteries_posts")
for u in sustainability_users:
    add_user(u, ["renewable", "sustainability"], source_post="sustainability_posts")

# Write to JSONL
output_path = "/Users/ryanprendergast/.openclaw/workspace/intelligence-briefings/data/energy-storage/reddit-users.jsonl"
with open(output_path, "a") as f:
    for user in users_data:
        f.write(json.dumps(user) + "\n")

print(f"Added {len(users_data)} users to {output_path}")
