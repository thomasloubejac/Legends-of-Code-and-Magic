#!/usr/bin/python3
  
import os
import json
from multiprocessing.dummy import Pool as ThreadPool
import time
thread_number = 8

players = os.listdir("genbots")

scores = 0 

interval = 2

count =  0

with open('ordered_players.json','r') as f:
    dic = json.loads(f.read())
player = dic["players"][-1]

def take_everyone(playerid):
    global player
    global scores
    global count
    count += 1
    if count-1 < thread_number :
        time.sleep((count-1)*interval)
    player2id  =  "../corrected_main.py"
#            while (datetime.now() - last_started).total_seconds() < 2:
#                pass
#            last_started = datetime.now()
    match = player
    # make match
    cmd = "./make_match.py {} {} {}".format(player,player2id,
            match)
    os.system(cmd)
    # read results
    result = json.loads(open("../LegendsOfCodeAndMagic/logs/game{}.json".format(match),'r').read())
    scores += result["scores"]["0"]

    # make match
    cmd = "./make_match.py {} {} {}".format(player2id, player,
            match)
    os.system(cmd)
    # read results
    result = json.loads(open("../LegendsOfCodeAndMagic/logs/game{}.json".format(match),'r').read())
    scores += result["scores"]["1"]

    time.sleep(interval)

pool = ThreadPool(thread_number)
pool.map(take_everyone, range(len(players)))
#print(results)
#scores = [sum([k[j] for k in results]) for j in range(len(results[0]))]
# scores = map(sum, zip(results))

print("performance against main.py")
print(scores/40)
with open('perfs','a') as f:
    f.write(str(scores/40) + "\n")
