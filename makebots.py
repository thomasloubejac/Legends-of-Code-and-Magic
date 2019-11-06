#!/usr//bin/python3

import random as rd
import argparse
import os

os.system("rm genbots/*")

parser = argparse.ArgumentParser()
parser.add_argument("size")


args = parser.parse_args()

with open('main.py','r') as f:
    doc = f.readlines()

cdoc = []
for line in doc:
    if "player_health, player_mana, player_deck, player_rune, player_draw = \\" in line:
        cdoc += ["        player_health, player_mana, player_deck, player_rune = \\\n"]

    elif line.strip()=="player_rune, player_draw)":
        cdoc += ["      player_rune, 0)\n"]

    elif line.strip() == "opponent_hand, opponent_actions = [int(i) for i in input().split()]":
        cdoc += ["    opponent_hand = [int(i) for i in input().split()]\n"]
        cdoc += ["    bdmger.add_opponent_informations(opponent_hand, 0)\n"]

    elif line.strip() in ["for i in range(opponent_actions):",
            "card_numbers_and_actions += [input()]",
            "bdmger.add_opponent_informations(opponent_hand, card_numbers_and_actions)"                         ]:
        pass
    elif line.strip() == "result += (len(self.get_my_hand()) - self.opponent_hand)*hand_weight":
        cdoc += "        result += (len(self.get_my_hand()) - len(self.opponent_hand))*hand_weight\n"
    elif line.strip()  ==  "with timeout(0.099):":
        cdoc += "   with timeout(0.095):\n"

    else:
        cdoc += [line]

for i in range(int(args.size)-1):
    with open('genbots/player{}.py'.format(str(i)),'w') as f:
        for line in cdoc:
            if line.startswith("weight_"):
                rep = line.split(" ")[0]
                value = rd.random()*5
                f.write("{} = {}\n".format(rep, str(value)))
            else:
                f.write(line)

with open('corrected_main.py'.format(str(i)),'w') as f:
    for line in cdoc:
        f.write(line)
