import bracketology.brackets as bracketology
import re
import random
from collections import defaultdict

# Patch
bracketology.brackets_dict.clear()
bracketology.brackets_dict.update({
    "2024": {
        "Finals": {
            "game1": {
                "team1": "east",
                "team2": "west",
            },
            "game2": {
                "team1": "south",
                "team2": "midwest",
            },
        }
    }
})

MAX_UPSET_CHANCE = .5

upset_chances = []

with open('data/cups.txt', 'r') as f:
    order = [int(x) for x in f.read().splitlines()]
    assert sorted(order) == list(range(1, 65)), f"Invalid order: {order}"
    for i in order:
        upset_chances.append(MAX_UPSET_CHANCE * i/len(order))

regions = []
all_teams = []

def sim_func(game):
    team1 = game.top_team
    team2 = game.bottom_team
    seed_diff = team1.seed - team2.seed

    if seed_diff == 0:
        worse, better = (team2, team1) if random.random() < .5 else (team1, team2)
    else:
        worse, better = (team2, team1) if seed_diff < 0 else (team1, team2)

    upset_chance = upset_chances[all_teams.index(better)]
    return worse if random.random() < upset_chance else better

for region_name in ["east", "west", "south", "midwest"]:
    with open(f'data/{region_name}.txt', 'r') as f:
        lines = f.read().splitlines()

    teams = []

    for line in lines:
        match = re.match(r'^No\. (\d+) (.*) vs. No. (\d+) (.*)$', line)
        team1 = bracketology.Team(seed = int(match.group(1)), name=match.group(2))
        team2 = bracketology.Team(seed = int(match.group(3)), name=match.group(4))
        teams.append(team1)
        teams.append(team2)

    teams.sort(key=lambda x: x.seed)

    all_teams.extend(teams)

    region = bracketology.SubBracket16(region_name).initialize_first_round(teams)
    regions.append(region)

teams_and_chances = [(upset_chances[i], team) for i, team in enumerate(all_teams)]
teams_and_chances.sort(key = lambda x: x[0], reverse=True)

print("Upset chances:")
for weight, team in teams_and_chances:
    print(f"{team}: {weight}")

winners_by_region = {
    region.region: defaultdict(list) 
    for region in regions
}

def run_full_sim():
    for region in regions:
        region.run_bracket(sim_func)
        print(region)

    final_four = bracketology.FinalFour(2024)
    final_four.set_matches({
        region.region: region.winner for region in regions
    })
    final_four.run_final_four(sim_func)
    final_four.run_championship(sim_func)
    print(final_four)

run_full_sim()
