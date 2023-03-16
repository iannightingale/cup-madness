from bracketology import Bracket, Game, Team, SubBracket16, simulators
import re
import random

weights = []

with open('data/cups.txt', 'r') as f:
    order = f.read().splitlines()

regions = []

all_teams = []

def sim_func(the_game):
    team1 = the_game.top_team
    team2 = the_game.bottom_team

    team1_seed = team1.seed
    team2_seed = team2.seed
    
    lower_seed = team2 if (team1_seed <= team2_seed) else team1
    is_upset = (random.random() < .5)
    
    pos = all_teams.index(lower_seed)
    print(order[pos])
    return lower_seed
    

for region_name in ["east", "midwest", "south", "west"]:
    print(region_name)
    with open(f'data/{region_name}.txt', 'r') as f:
        lines = f.read().splitlines()

    games = []
    teams = []

    for line in lines:
        match = re.match(r'^No\. (\d+) (.*) vs. No. (\d+) (.*)$', line)
        team1 = Team(seed = int(match.group(1)), name=match.group(2))
        team2 = Team(seed = int(match.group(3)), name=match.group(4))
        teams.append(team1)
        teams.append(team2)

    teams.sort(key=lambda x: x.seed)

    print(teams)

    all_teams.extend(teams)

    region = SubBracket16(region_name).initialize_first_round(teams)
    regions.append(region)

for region in regions:
    region.run_bracket(sim_func)
    print(region.region, region.winner)