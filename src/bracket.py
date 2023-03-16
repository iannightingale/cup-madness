import bracketology.brackets as bracketology
import re
import random
from collections import defaultdict

# Patch
bracketology.brackets_dict.clear()
bracketology.brackets_dict.update({
    "2023": {
        "Finals": {
            "game1": {
                "team1": "south",
                "team2": "east",
            },
            "game2": {
                "team1": "midwest",
                "team2": "west",
            },
        }
    }
})

weights = []

with open('data/cups.txt', 'r') as f:
    order = f.read().splitlines()

regions = []

all_teams = []

def sim_func(game):
    team1 = game.top_team
    team2 = game.bottom_team
    seed_diff = team1.seed - team2.seed

    lower, higher = (team2, team1) if seed_diff < 0 else (team1, team2)

    pos = all_teams.index(higher)
    upset_chance = (.5 * (pos / len(order)))
    return lower if random.random() < upset_chance else higher
    

for region_name in ["east", "west", "south", "midwest"]:
    with open(f'data/{region_name}.txt', 'r') as f:
        lines = f.read().splitlines()

    games = []
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

winners_by_region = {
    region.region: defaultdict(list) 
    for region in regions
}

def run_full_sim():
    for region in regions:
        region.run_bracket(sim_func)
        print(region)

    final_four = bracketology.FinalFour(2023)
    final_four.set_matches({
        region.region: region.winner for region in regions
    })
    final_four.run_final_four(sim_func)
    final_four.run_championship(sim_func)
    print(final_four)

run_full_sim()
