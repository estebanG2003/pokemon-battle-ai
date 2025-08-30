import json

with open("trainers.json", "r", encoding="utf-8") as f:
    trainers = json.load(f)

for trainer in trainers:
    if "team" in trainer and trainer["team"]:
        levels = [poke.get("level", 0) for poke in trainer["team"] if "level" in poke]
        trainer["level_cap"] = max(levels) if levels else 0
    else:
        trainer["level_cap"] = 0

with open("trainers.json", "w", encoding="utf-8") as f:
    json.dump(trainers, f, indent=2)