import csv
import json
import re

def parse_trainer_csv(csv_path):
    trainers = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        battle_order = 1
        current_trainer = None

        for row in reader:
            name = row[''].strip() if row[''] else ''
            location = row['Route'].strip() if row['Route'] else ''
            species = row['Pokémon'].strip() if row['Pokémon'] else ''
            level = row['Level'].strip() if row['Level'] else ''
            moves = [row['Attack 1'], row['Attack 2'], row['Attack 3'], row['Attack 4']]
            moves = [m.strip() for m in moves if m and m.strip()]

            # If there's a trainer name, start a new trainer
            if name:
                if current_trainer:
                    trainers.append(current_trainer)
                current_trainer = {
                    "name": name,
                    "location": location,
                    "battle_order": battle_order,
                    "team": []
                }
                battle_order += 1

            # If there's a Pokémon, add it to the current trainer's team
            if species and current_trainer:
                # Extract numeric level
                try:
                    level_int = int(re.findall(r'\d+', level)[0])
                except (IndexError, ValueError):
                    level_int = None
                poke = {
                    "species": species,
                    "level": level_int,
                    "moves": moves
                }
                current_trainer["team"].append(poke)

        # Add the last trainer
        if current_trainer:
            trainers.append(current_trainer)
    return trainers

if __name__ == "__main__":
    trainers = parse_trainer_csv("PokemonEmeraldTrainers.csv")
    with open("trainers.json", "w", encoding="utf-8") as f:
        json.dump(trainers, f, indent=2)