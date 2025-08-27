# Pokémon Pool - Up to Roxanne (Gym 1)
pool_gym1 = [
    {
        "species": "Mudkip",
        "evolutions": [
            {"species": "Marshtomp", "method": "level", "level": 16},
            {"species": "Swampert", "method": "level", "level": 36}
        ]
    },
    {
        "species": "Poochyena",
        "evolutions": [
            {"species": "Mightyena", "method": "level", "level": 18}
        ]
    },
    {
        "species": "Zigzagoon",
        "evolutions": [
            {"species": "Linoone", "method": "level", "level": 20}
        ]
    },
    {
        "species": "Wurmple",
        "evolutions": [
            {"species": "Silcoon", "method": "level", "level": 7},
            {"species": "Cascoon", "method": "level", "level": 7}
        ]
    },
    {
        "species": "Silcoon",
        "evolutions": [
            {"species": "Beautifly", "method": "level", "level": 10}
        ]
    },
    {
        "species": "Cascoon",
        "evolutions": [
            {"species": "Dustox", "method": "level", "level": 10}
        ]
    },
    {
        "species": "Lotad",
        "evolutions": [
            {"species": "Lombre", "method": "level", "level": 14}
        ]
    },
    {
        "species": "Seedot",
        "evolutions": [
            {"species": "Nuzleaf", "method": "level", "level": 14}
        ]
    },
    {
        "species": "Taillow",
        "evolutions": [
            {"species": "Swellow", "method": "level", "level": 22}
        ]
    },
    {
        "species": "Wingull",
        "evolutions": [
            {"species": "Pelipper", "method": "level", "level": 25}
        ]
    },
    {
        "species": "Ralts",
        "evolutions": [
            {"species": "Kirlia", "method": "level", "level": 20},
            {"species": "Gardevoir", "method": "level", "level": 30}
        ]
    },
    {
        "species": "Shroomish",
        "evolutions": [
            {"species": "Breloom", "method": "level", "level": 23}
        ]
    },
    {
        "species": "Slakoth",
        "evolutions": [
            {"species": "Vigoroth", "method": "level", "level": 18},
            {"species": "Slaking", "method": "level", "level": 36}
        ]
    },
    {
        "species": "Abra",
        "evolutions": [
            {"species": "Kadabra", "method": "level", "level": 16}
        ]
    },
    {
        "species": "Nincada",
        "evolutions": [
            {"species": "Ninjask", "method": "level", "level": 20},
            {"species": "Shedinja", "method": "level", "level": 20}
        ]
    },
    {
        "species": "Whismur",
        "evolutions": [
            {"species": "Loudred", "method": "level", "level": 20},
            {"species": "Exploud", "method": "level", "level": 40}
        ]
    },
    {
        "species": "Marill",
        "evolutions": [
            {"species": "Azumarill", "method": "level", "level": 18}
        ]
    },
    {
        "species": "Skitty",
        "evolutions": []  # Evolves with Moon Stone (not available yet)
    }
]
# Pokémon Pool - Up to Brawly (Gym 2)
pool_gym2 = pool_gym1 + [
    {
        "species": "Makuhita",
        "evolutions": [
            {"species": "Hariyama", "method": "level", "level": 24}
        ]
    },
    {
        "species": "Goldeen",
        "evolutions": [
            {"species": "Seaking", "method": "level", "level": 33}
        ]
    },
    {
        "species": "Magikarp",
        "evolutions": [
            {"species": "Gyarados", "method": "level", "level": 20}
        ]
    },
    {
        "species": "Geodude",
        "evolutions": [
            {"species": "Graveler", "method": "level", "level": 25}
        ]
    },
    {
        "species": "Zubat",
        "evolutions": [
            {"species": "Golbat", "method": "level", "level": 22},
            {"species": "Crobat", "method": "friendship", "level": None}  # high friendship
        ]
    },
    {
        "species": "Tentacool",
        "evolutions": [
            {"species": "Tentacruel", "method": "level", "level": 30}
        ]
    },
    {
        "species": "Sableye",
        "evolutions": []  # No further evolutions
    },
    {
        "species": "Aron",
        "evolutions": [
            {"species": "Lairon", "method": "level", "level": 32},
            {"species": "Aggron", "method": "level", "level": 42}
        ]
    },
    {
        "species": "Electrike",
        "evolutions": [
            {"species": "Manectric", "method": "level", "level": 26}
        ]
    },
    {
        "species": "Plusle",
        "evolutions": []  # No evolutions
    },
    {
        "species": "Minun",
        "evolutions": []  # No evolutions
    },
    {
        "species": "Volbeat",
        "evolutions": []  # No evolutions
    },
    {
        "species": "Illumise",
        "evolutions": []  # No evolutions
    },
    {
        "species": "Oddish",
        "evolutions": [
            {"species": "Gloom", "method": "level", "level": 21}
            # Vileplume/Bellossom require stones, not available yet
        ]
    },
    {
        "species": "Gulpin",
        "evolutions": [
            {"species": "Swalot", "method": "level", "level": 26}
        ]
    }
]
# Pokémon Pool - Up to Wattson (Gym 3)
pool_gym3 = pool_gym2 + [
    {
        "species": "Nosepass",
        "evolutions": []  # No evolutions in Gen 3
    },
    {
        "species": "Delcatty",
        "evolutions": []  # Stone evo (Skitty → Delcatty with Moon Stone), assume already in pool
    },
    {
        "species": "Machop",
        "evolutions": [
            {"species": "Machoke", "method": "level", "level": 28}
            # Machamp requires trade, so ignored for Emerald
        ]
    },
    {
        "species": "Bellossom",
        "evolutions": []  # Gloom → Bellossom with Sun Stone, assume availability
    },
    {
        "species": "Numel",
        "evolutions": [
            {"species": "Camerupt", "method": "level", "level": 33}
        ]
    },
    {
        "species": "Slugma",
        "evolutions": [
            {"species": "Magcargo", "method": "level", "level": 38}
        ]
    },
    {
        "species": "Torkoal",
        "evolutions": []  # No evolutions
    },
    {
        "species": "Grimer",
        "evolutions": [
            {"species": "Muk", "method": "level", "level": 38}
        ]
    },
    {
        "species": "Koffing",
        "evolutions": [
            {"species": "Weezing", "method": "level", "level": 35}
        ]
    },
    {
        "species": "Spoink",
        "evolutions": [
            {"species": "Grumpig", "method": "level", "level": 32}
        ]
    },
    {
        "species": "Spinda",
        "evolutions": []  # No evolutions
    },
    {
        "species": "Skarmory",
        "evolutions": []  # No evolutions
    },
    {
        "species": "Swablu",
        "evolutions": [
            {"species": "Altaria", "method": "level", "level": 35}
        ]
    },
    {
        "species": "Seviper",
        "evolutions": []  # No evolutions
    },
    {
        "species": "Solrock",
        "evolutions": []  # No evolutions
    },
    {
        "species": "Wynaut",
        "evolutions": [
            {"species": "Wobbuffet", "method": "level", "level": 15}
        ]
    }
]
# Pokémon Pool - Up to Flannery (Gym 4) AND Up to Norman (Gym 5)
pool_gym4 = pool_gym3 + [
    {
        "species": "Sandshrew",
        "evolutions": [
            {"species": "Sandslash", "method": "level", "level": 22}
        ]
    },
    {
        "species": "Trapinch",
        "evolutions": [
            {"species": "Vibrava", "method": "level", "level": 35},
            {"species": "Flygon", "method": "level", "level": 45}
        ]
    },
    {
        "species": "Cacnea",
        "evolutions": [
            {"species": "Cacturne", "method": "level", "level": 32}
        ]
    },
    {
        "species": "Baltoy",
        "evolutions": [
            {"species": "Claydol", "method": "level", "level": 36}
        ]
    },
    {
        "species": "Lileep",
        "evolutions": [
            {"species": "Cradily", "method": "level", "level": 40}
        ]
    },
    {
        "species": "Anorith",
        "evolutions": [
            {"species": "Armaldo", "method": "level", "level": 40}
        ]
    }
]
# Pokémon Pool - Up to Winona (Gym 6)
pool_gym5 = pool_gym4 + [
    {
        "species": "Azurill",
        "evolutions": []
    },
    {
        "species": "Magnemite",
        "evolutions": [
            {"species": "Magneton", "method": "level", "level": 30}
        ]
    },
    {
        "species": "Voltorb",
        "evolutions": [
            {"species": "Electrode", "method": "level", "level": 30}
        ]
    },
    {
        "species": "Doduo",
        "evolutions": [
            {"species": "Dodrio", "method": "level", "level": 31}
        ]
    },
    {
        "species": "Carvanha",
        "evolutions": [
            {"species": "Sharpedo", "method": "level", "level": 30}
        ]
    },
    {
        "species": "Wailmer",
        "evolutions": [
            {"species": "Wailord", "method": "level", "level": 40}
        ]
    },
    {
        "species": "Barboach",
        "evolutions": [
            {"species": "Whiscash", "method": "level", "level": 30}
        ]
    },
    {
        "species": "Corphish",
        "evolutions": [
            {"species": "Crawdaunt", "method": "level", "level": 30}
        ]
    },
    {
        "species": "Igglybuff",
        "evolutions": []
    },
    {
        "species": "Jigglypuff",
        "evolutions": []
    },
    {
        "species": "Feebas",
        "evolutions": [
            {"species": "Milotic", "method": "beauty", "level": None}
        ]
    },
    {
        "species": "Castform",
        "evolutions": []
    },
    {
        "species": "Staryu",
        "evolutions": []
    },
    {
        "species": "Kecleon",
        "evolutions": []
    },
    {
        "species": "Shuppet",
        "evolutions": [
            {"species": "Banette", "method": "level", "level": 37}
        ]
    },
    {
        "species": "Duskull",
        "evolutions": [
            {"species": "Dusclops", "method": "level", "level": 37}
        ]
    },
    {
        "species": "Tropius",
        "evolutions": []
    },
    {
        "species": "Chimecho",
        "evolutions": []
    },
    {
        "species": "Absol",
        "evolutions": []
    },
    {
        "species": "Vulpix",
        "evolutions": [
            {"species": "Ninetales", "method": "stone", "level": None}
        ]
    },
    {
        "species": "Pichu",
        "evolutions": []
    },
    {
        "species": "Pikachu",
        "evolutions": [
            {"species": "Raichu", "method": "stone", "level": None}
        ]
    },
    {
        "species": "Psyduck",
        "evolutions": [
            {"species": "Golduck", "method": "level", "level": 33}
        ]
    },
    {
        "species": "Natu",
        "evolutions": [
            {"species": "Xatu", "method": "level", "level": 25}
        ]
    },
    {
        "species": "Girafarig",
        "evolutions": []
    },
    {
        "species": "Phanpy",
        "evolutions": [
            {"species": "Donphan", "method": "level", "level": 25}
        ]
    },
    {
        "species": "Pinsir",
        "evolutions": []
    },
    {
        "species": "Heracross",
        "evolutions": []
    },
    {
        "species": "Rhyhorn",
        "evolutions": [
            {"species": "Rhydon", "method": "level", "level": 42}
        ]
    },
    {
        "species": "Snorunt",
        "evolutions": [
            {"species": "Glalie", "method": "level", "level": 42}
        ]
    },
    {
        "species": "Spheal",
        "evolutions": [
            {"species": "Sealeo", "method": "level", "level": 32},
            {"species": "Walrein", "method": "level", "level": 44}
        ]
    },
    {
        "species": "Corsola",
        "evolutions": []
    },
    {
        "species": "Luvdisc",
        "evolutions": []
    },
    {
        "species": "Horsea",
        "evolutions": [
            {"species": "Seadra", "method": "level", "level": 32}
        ]
    },
    {
        "species": "Vileplume",
        "evolutions": []
    },
    {
        "species": "Shiftry",
        "evolutions": []
    }
]
# Pokémon Pool - Up to Tate&Liza (Gym 7)
pool_gym6 = pool_gym5 + [
    {
        "species": "Ludicolo",
        "evolutions": []  # Evolve Lombre with Water Stone
    },
    {
        "species": "Starmie",
        "evolutions": []  # Evolve Staryu with Water Stone
    },
    {
        "species": "Clamperl",
        "evolutions": []  # Underwater routes, no evolution info here
    },
    {
        "species": "Relicanth",
        "evolutions": []  # No evolutions
    },
    {
        "species": "Chinchou",
        "evolutions": [
            {"species": "Lanturn", "method": "level", "level": 27}
        ]
    },
    {
        "species": "Regirock",
        "evolutions": []  # Legendary, no evolutions
    },
    {
        "species": "Regice",
        "evolutions": []  # Legendary, no evolutions
    },
    {
        "species": "Registeel",
        "evolutions": []  # Legendary, no evolutions
    },
    {
        "species": "Rayquaza",
        "evolutions": []  # Legendary, no evolutions
    }
]

pool_gym7 = pool_gym6 + [
    {
        "species": "Mawile",
        "evolutions": []  # No evolutions
    },
    {
        "species": "Bagon",
        "evolutions": [
            {"species": "Shelgon", "method": "level", "level": 30},
            {"species": "Salamence", "method": "level", "level": 50}
        ]
    }
]
