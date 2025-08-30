import random
import json
from pokemonPools import pool_gym1

# Load Hoenn pokedex database
with open("hoenn_pokedex.json", "r", encoding="utf-8") as f:
    hoenn_db = json.load(f)

def random_team_string(level_cap):
    team_size = random.randint(3, 6)
    team = random.sample(pool_gym1, team_size)

    items = ["Leftovers", "Oran Berry", "Sitrus Berry", "Lum Berry", "Quick Claw", "Focus Band", "Shell Bell"]
    natures = [
    "Adamant", "Bashful", "Bold", "Brave", "Calm",
    "Careful", "Docile", "Gentle", "Hardy", "Hasty",
    "Impish", "Jolly", "Lax", "Lonely", "Mild",
    "Modest", "Naive", "Naughty", "Quiet", "Quirky",
    "Rash", "Relaxed", "Sassy", "Serious", "Timid"
    ]
    
    def format_pokemon(poke):
        species = poke["species"].lower()
        poke_data = hoenn_db.get(species)
        if not poke_data:
            return f"{species.title()} (M)\nAbility: ???\nLevel: {level_cap}\n??? Nature\n- ???\n- ???\n- ???\n- ???\n"

        ability = random.choice(poke_data["abilities"]) if poke_data["abilities"] else "???"
        item = random.choice(items)
        nature = random.choice(natures)

        # Get moves up to level_cap
        moves_up_to_cap = [m["name"].replace("-", " ").title() for m in poke_data["moves"] if m["level"] <= level_cap]
        if len(moves_up_to_cap) < 4:
            moves = moves_up_to_cap + ["Tackle"] * (4 - len(moves_up_to_cap))
        else:
            moves = random.sample(moves_up_to_cap, 4)
        moves_str = "\n".join(f"- {move}" for move in moves)

        gender = random.choice(["M", "F"])
        return f"""{species.title()} ({gender}) @ {item}
Ability: {ability.title()}
Level: {level_cap}
{nature} Nature
{moves_str}
"""

    team_str = "\n".join(format_pokemon(poke) for poke in team)
    return f'team_1 = """\n{team_str}"""'

if __name__ == "__main__":
    print(random_team_string(15))