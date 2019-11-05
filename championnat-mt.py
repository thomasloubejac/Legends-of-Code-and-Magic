#!/usr/bin/python3
  
import os
import json
from multiprocessing.dummy import Pool as ThreadPool
import time
thread_number = 8

players = os.listdir("genbots")

scores = [0]*len(players)

count = 0

def take_everyone(playerid):
    global players
    global scores
    global count
    count += 1
    if count -  1 < thread_number:
        time.sleep(count - 1)
    for player2id in range(len(players)):
        if player2id==playerid:
            pass
        else:
            match = str(playerid) + '-' + str(player2id)
            # make match
            cmd = "./make_match.py {} {} {} > /dev/null 2>&1".format(players[playerid],players[player2id],
                    match)
            os.system(cmd)
            # read results
            result = json.loads(open("../LegendsOfCodeAndMagic/logs/game{}.json".format(match,'r')).read())
            score1 = result["scores"]["0"]
            score2 = result["scores"]["1"]
            # adjust scores
            scores[playerid] += score1
            scores[player2id] += score2
            print(players[playerid],players[player2id])
            print(score1)
            print(score2)

pool = ThreadPool(thread_number)
pool.map(take_everyone, range(len(players)))
#print(results)
#scores = [sum([k[j] for k in results]) for j in range(len(results[0]))]
# scores = map(sum, zip(results))

ordered_scores = sorted(scores,reverse=True)
ordered_players = []
for i in list(set(ordered_scores)):
    isp = [index for index, value in enumerate(scores) if value == i]
    ordered_players += [players[j] for j in isp]

print(ordered_players)
print(scores)

with open('ordered_players.json','w') as f:
    f.write(json.dumps(ordered_players))
