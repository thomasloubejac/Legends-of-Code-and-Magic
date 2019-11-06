#!/usr/bin/python3
  
import os
import json
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime
import time
thread_number = 8

players = os.listdir("genbots")
players = sorted(players, key= lambda x : int(x.split(".")[0].split("r")[1]))

scores = [0]*len(players)

count = 0

interval = 2

last_started = datetime.now()

def take_everyone(playerid):
    global players
    global scores
    global count
    global last_started 
    count += 1
    if count-1 < thread_number :
        time.sleep((count-1)*interval)
    for player2id in range(len(players)):
        if player2id==playerid:
            pass
        else:
#            while (datetime.now() - last_started).total_seconds() < 2:
#                pass
#            last_started = datetime.now()
            match = str(playerid) + '-' + str(player2id)
            # make match
            cmd = "./make_match.py {} {} {}".format(players[playerid],players[player2id],
                    match)
            print(cmd)
            os.system(cmd)
            # read results
            result = json.loads(open("../LegendsOfCodeAndMagic/logs/game{}.json".format(match),'r').read())
            score1 = result["scores"]["0"]
            score2 = result["scores"]["1"]
            # adjust scores
            scores[playerid] += score1
            scores[player2id] += score2
            print(players[playerid],players[player2id])
            print(score1)
            print(score2)

            if -1 in (score1,score2):
                print(result["errors"])

            time.sleep(interval)

pool = ThreadPool(thread_number)
pool.map(take_everyone, range(len(players)))
#print(results)
#scores = [sum([k[j] for k in results]) for j in range(len(results[0]))]
# scores = map(sum, zip(results))

ordered_scores = sorted(scores)
ordered_players = []
for i in list(set(ordered_scores)):
    isp = [index for index, value in enumerate(scores) if value == i]
    ordered_players += [players[j] for j in isp]

print(ordered_players)
print(scores)

with open('ordered_players.json','w') as f:
    dic =  {}
    dic["players"] = ordered_players
    dic["scores"] = ordered_scores
    dic["dic"] = {players[i] :  scores[i] for i in range(len(players))}
    f.write(json.dumps(dic))
