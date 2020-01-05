ATTRIBUTES = [
    "Intelligence", "Wits", "Resolve",
    "Strength", "Dexterity", "Stamina",
    "Presence", "Manipulation", "Composure"
]

RESISTANCES = ["Resolve", "Stamina", "Composure"]


SKILLS = [
    "Academics", "Computer", "Crafts", "Investigation",
    "Medicine", "Occult", "Politics", "Science",
    "Athletics", "Brawl", "Drive", "Firearms",
    "Larceny", "Stealth", "Survival", "Weaponry",
    "Animal Ken", "Empathy", "Expression", "Intimidation",
    "Persuasion", "Socialize", "Streetwise", "Subterfuge"
]


PROF_SKILLS = {
    "Academic": ("Academics", "Science"),
    "Artist": ("Crafts", "Expression"),
    "Athlete": ("Athletics", "Medicine"),
    "Cop": ("Streetwise", "Firearms"),
    "Criminal": ("Larceny", "Streetwise"),
    "Detective": ("Empathy", "Investigation"),
    "Doctor": ("Empathy", "Medicine"),
    "Engineer": ("Crafts", "Science"),
    "Hacker": ("Computer", "Science"),
    "Hit Man": ("Firearms", "Stealth"),
    "Journalist": ("Expression", "Investigation"),
    "Laborer": ("Athletics", "Crafts"),
    "Occultist": ("Investigation", "Occult"),
    "Politician": ("Politics", "Subterfuge"),
    "Religious Leader": ("Academics", "Occult"),
    "Scientist": ("Investigation", "Science"),
    "Socialite": ("Politics", "Socialize"),
    "Stuntman": ("Athletics", "Drive"),
    "Survivalist": ("Animal Ken", "Survival"),
    "Soldier": ("Firearms", "Survival"),
    "Technician": ("Crafts", "Investigation"),
    "Thug": ("Brawl", "Intimidation"),
    "Vagrant": ("Streetwise", "Survival"),
}


PROFESSIONS = list(PROF_SKILLS.keys())


PROF_ATTRIBUTES = {
    "Academic": ("Intelligence", ),
    "Artist": ("Dexterity", ),
    "Athlete": ("Stamina", ),
    "Cop": ("Wits", ),
    "Criminal": ("Manipulation", ),
    "Detective": ("Wits", ),
    "Doctor": ("Intelligence", ),
    "Engineer": ("Dexterity", ),
    "Hacker": ("Intelligence", ),
    "Hit Man": ("Dexterity", ),
    "Journalist": ("Composure", ),
    "Laborer": ("Stamina", ),
    "Occultist": ("Composure", ),
    "Politician": ("Manipulation", ),
    "Religious Leader": ("Manipulation", ),
    "Scientist": ("Intelligence", ),
    "Socialite": ("Presence", ),
    "Stuntman": ("Strength", ),
    "Survivalist": ("Wits", ),
    "Soldier": ("Resolve", ),
    "Technician": ("Composure", ),
    "Thug": ("Strength", ),
    "Vagrant": ("Wits", ),
}


CONTACTS = [
    "Drug Dealers", "Bloggers", "Financial Speculators",
    "Legal Advisors", "Librarians", "Political Aides", "Contractors",
    "Fashion Models", "Caterers", "Private Security",
    "Police Officers", "First Responders", "Night Doctors",
    "Architects", "Bureucrats", "Scholars", "Book Publishers",
    "Broadcasters", "Journalists", "Taxi Drivers",
    "Celebrities", "Charities", "Music Scene", "Art Scene",
    "Entrepreneurs", "Sex Workers", "Weapon Dealers",
    "Private Investigators", "Clergy", "Criminal Bosses",
    "Homeless", "Labor Unions", "Hacker Rings",
]


VIRTUES = [
    "Patient", "Loving", "Ambitious", "Generous", "Just",
    "Tolerant", "Hopeful", "Courageous", "Confident"
]


VICES = [
    "Hateful", "Cruel", "Greedy", "Lustful", "Cowardly",
    "Arrogant", "Gluttonous", "Deceitful", "Reckless"
]


MERIT_DOTS = {
    "Anonymity": (1, 2, 3, 4, 5),
    "Fame": (1, 2, 3),
    "Barfly": (2, ),
    "Alternate Identity": (1, 2, 3),
    "Small-Framed": (2, ),
    "Giant": (3, ),
    "Area of Expertise": (1, ),
    "Common Sense": (3, ),
    "Eye for the Strange": (2, ),
    "Danger Sense": (2, ),
    "Direction Sense": (1, ),
    "Eidetic Memory": (2, ),
    "Encyclopedic Knowledge": (2, ),
    "Fast Reflexes": (1, 2, 3),
    "Good Time Management": (1, ),
    "Holistic Awareness": (1, ),
    "Indomitable": (2, ),
    "Language": (1, ),
    "Library": (1, 2, 3),
    "Meditative Mind": (1, 2, 3),
    "Multilingual": (1, ),
    "Tolerance for Biology": (2, ),
    "Trained Observer": (1, 3),
    "Crack Driver": (2, ),
    "Demolisher": (1, 2, 3),
    "Double Jointed": (2, ),
    "Fleet of Foot": (1, 2, 3),
    "Hardy": (1, 2, 3),
    "Iron Stamina": (1, 2, 3),
    "Parkour": (1, 2, 3, 4, 5),
    "Allies": (1, 2, 3, 4, 5),
    "Fast-Talking": (1, 2, 3, 4, 5),
    "Fixer": (2, ),
    "Hobbyist Clique": (2, ),
    "Inspiring": (3, ),
    "Iron Will": (2, ),
    "Mentor": (1, 2, 3, 4, 5),
    "Mystery Cult Initiation": (1, 2, 3, 4, 5),
    "Resources": (1, 2, 3, 4, 5),
    "Pusher": (1, ),
    "Retainer": (1, 2, 3, 4, 5),
    "Safe Place": (1, 2, 3, 4, 5),
    "Status": (1, 2, 3, 4, 5),
    "Staff": (1, 2, 3, 4, 5),
    "Striking Looks": (1, 2),
    "Sympathetic": (2, ),
    "Taste": (1, ),
    "True Friend": (3, ),
    "Untouchable": (1, ),
}

MERITS = list(MERIT_DOTS.keys())


ARCANA = [
    "Death", "Fate", "Forces", "Life", "Matter",
    "Mind", "Prime", "Space", "Spirit", "Time",
]

PATH_REAGENTS = {
    "Acanthus": ("Fate", "Time"),
    "Mastigos": ("Mind", "Space"),
    "Moros": ("Matter", "Death"),
    "Obrimos": ("Prime", "Forces"),
    "Thyrsus": ("Life", "Spirit"),
}

PATH_INFERIOR = {
    "Acanthus":  "Forces",
    "Mastigos": "Matter",
    "Moros": "Spirit",
    "Obrimos": "Death",
    "Thyrsus": "Mind",
}

PATHS = list(PATH_REAGENTS.keys())
