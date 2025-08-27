import csv
import re
from collections import OrderedDict
import pprint

def parse_team_row(row):
    team = []
    for cell in row:
        if cell:
            match = re.match(r'([A-Za-z0-9\'\-\.]+) \((\w)\)', cell)
            if match:
                species, gender = match.groups()
                team.append({"species": species, "gender": gender})
            else:
                match = re.match(r'([A-Za-z0-9\'\-\.]+)', cell)
                if match:
                    species = match.group(1)
                    team.append({"species": species, "gender": None})
    return team

def parse_level_row(row, team):
    for i, cell in enumerate(row):
        if cell and i < len(team):
            match = re.match(r'(?:Lv\. )?(\d+)(?: \((\w+)\))?', cell)
            if match:
                level = int(match.group(1))
                nature = match.group(2) if match.group(2) else None
                team[i]["level"] = level
                team[i]["nature"] = nature
    return team

def parse_csv(filename):
    trainers = OrderedDict()
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        i = 0
        while i < len(rows):
            row = rows[i]
            if row and row[0] and not row[0].startswith("Note"):
                trainer_name = row[0]
                ai_flags = ["7"]
                double_battle = "Double Battle" in trainer_name
                team = []
                # Check next rows for AI_FLAG and team info
                j = i + 1
                while j < len(rows) and (not rows[j][0] or rows[j][0].startswith("AI_FLAG:") or rows[j][0].startswith(",")):
                    if rows[j][1:2] and rows[j][1] == "AI_FLAG:":
                        ai_flags = [rows[j][2]] if rows[j][2] else ["7"]
                    elif any(re.match(r'.*\((m|f)\)', cell) for cell in rows[j]):
                        team = parse_team_row(rows[j])
                        # Next row should be levels/nature
                        if j + 1 < len(rows):
                            team = parse_level_row(rows[j+1], team)
                    j += 1
                trainers[trainer_name] = {
                    "double_battle": double_battle,
                    "ai_flags": ai_flags,
                    "team": team
                }
                i = j
            else:
                i += 1
    return trainers

if __name__ == "__main__":
    trainers = parse_csv("TrainerSheet.csv")
    with open("trainers.py", "w", encoding="utf-8") as f:
        f.write("from collections import OrderedDict\n\n")
        f.write("trainers = ")
        pprint.pprint(trainers, stream=f, width=120)