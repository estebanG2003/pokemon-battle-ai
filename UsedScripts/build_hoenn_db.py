import pokebase as pb
import json
import time

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

def get_hoenn_pokedex_species():
    # Hoenn Pokédex is National Dex 252-386 (Treecko to Deoxys)
    # We'll use pokebase.pokemon_species with IDs 252 to 386
    species_names = []
    for i in range(252, 387):
        species = pb.pokemon_species(i)
        species_names.append(species.name)
    return species_names

def build_hoenn_database():
    species_names = get_hoenn_pokedex_species()
    database = {}
    for name in species_names:
        print(f"Processing {name}...")
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
            time.sleep(0.5)  # Be kind to the API
        except Exception as e:
            print(f"Error processing {name}: {e}")
    return database

if __name__ == "__main__":
    hoenn_db = build_hoenn_database()
    with open("hoenn_pokedex.json", "w", encoding="utf-8") as f:
        json.dump(hoenn_db, f, indent=2)