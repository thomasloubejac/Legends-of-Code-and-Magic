with open('main.py','r') as f:
    doc = f.readlines()

cdoc = []
for line in doc:
    if "player_health, player_mana, player_deck, player_rune, player_draw = \\" in line:
        cdoc += ["    player_health, player_mana, player_deck, player_rune = \\\n"]

    elif line.strip() == "opponent_hand, opponent_actions = [int(i) for i in input().split()]":
        cdoc += ["    opponent_hand = [int(i) for i in input().split()]\n"]
        cdoc += ["    bdmger.add_opponent_informations(opponent_hand, 0)\n"] 

    elif line.strip() in ["for i in range(opponent_actions):",
            "card_numbers_and_actions += [input()]",
            "bdmger.add_opponent_informations(opponent_hand, card_numbers_and_actions)"                         ]:
        pass
    else:
        cdoc += [line]

with open('corrected_main.py','w') as f:
    for line in cdoc:
        f.write(line)
