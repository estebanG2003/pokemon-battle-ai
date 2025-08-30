import pokebase as pb
import json
import time

# List of National Dex numbers for returning Pokémon in Hoenn Dex (Emerald)
returning_national_numbers = [
    63,64,65,118,119,129,130,183,184,74,75,76,41,42,169,72,73,66,67,
    68,81,82,100,101,43,44,45,182,84,85,218,219,88,89,109,110,27,28,
    227,174,39,40,120,121,37,38,172,25,26,54,55,202,177,178,203,231,
    232,127,214,111,112,222,170,171,116,117,230

]
# You may want to trim this list to only those that are actually catchable in Emerald's Hoenn Dex.

def get_pokemon_abilities(species_name):
    species = pb.pokemon(species_name.lower())
    return [ability.ability.name for ability in species.abilities]

def get_pokemon_moves(species_name):
    species = pb.pokemon(species_name.lower())
    moves = []
    for move in species.moves:
        for detail in move.version_group_details:
            if (
                detail.move_learn_method.name == "level-up"
                and detail.version_group.name == "emerald"
            ):
                moves.append({
                    "name": move.move.name,
                    "level": detail.level_learned_at
                })
    return moves

def get_pokemon_evolutions(species_name):
    species = pb.pokemon_species(species_name.lower())
    evo_chain = pb.evolution_chain(species.evolution_chain.id)
    evolutions = []

    def parse_chain(chain, from_species=None):
        species_name = chain.species.name
        if from_species:
            for evo_detail in chain.evolution_details:
                method = evo_detail.trigger.name
                min_level = evo_detail.min_level
                item = evo_detail.item.name if evo_detail.item else None
                evolutions.append({
                    "from": from_species,
                    "to": species_name,
                    "method": method,
                    "level": min_level,
                    "item": item
                })
        for next_evo in chain.evolves_to:
            parse_chain(next_evo, species_name)

    parse_chain(evo_chain.chain)
    return evolutions

if __name__ == "__main__":
    # Load your existing database
    with open("hoenn_pokedex.json", "r", encoding="utf-8") as f:
        database = json.load(f)

    for dex_num in returning_national_numbers:
        species = pb.pokemon_species(dex_num)
        name = species.name
        if name in database:
            continue  # Already present
        print(f"Adding {name}...")
        try:
            abilities = get_pokemon_abilities(name)
            moves = get_pokemon_moves(name)
            evolutions = get_pokemon_evolutions(name)
            database[name] = {
                "name": name,
                "abilities": abilities,
                "moves": moves,
                "evolutions": evolutions
            }
            time.sleep(0.5)
        except Exception as e:
            print(f"Error processing {name}: {e}")

    with open("hoenn_pokedex.json", "w", encoding="utf-8") as f:
        json.dump(database, f, indent=2)