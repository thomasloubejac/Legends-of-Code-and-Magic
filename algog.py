#!/usr/bin/python3
import random as rd
import json
import os
from datetime import datetime

size = 10

def change_weights(bot1, bot2):
    bot =  []
    for i in range(len(bot1)):
        op = rd.randint(1,3)
        if op==1:
            bot += [(bot1[i]+bot2[i])/2]
        if op==2:
            bot += [bot1[i]]
        if op==3:
            bot += [bot2[i]]
    return bot

def read_file():
    with open('ordered_players.json','r') as f:
        dic = json.loads(f.read())
    return dic

def read_bot(player):
    with open("genbots/{}".format(player),'r') as f:
        str_bot = f.read()
    return str_bot

def read_weights(player):
    bot  =  read_bot(player)
    weights  = []
    with open("genbots/{}".format(player),'r') as f:
        cdoc = f.readlines()
        for line in cdoc:
            if line.startswith("weight_"):
                value = line.split("= ")[-1]
                weights += [float(value)]
    return weights

def write_bot(bot,player):
    with open("genbots/{}".format(player),'r') as f:
        i = 0
        cdoc = f.readlines()
    with open("genbots/{}".format(player),'w') as f:
        for line in cdoc:
            if line.startswith("weight_"):
                key = line.split(" ")[0]
                value = bot[i]
                i += 1
                f.write("{} = {}\n".format(key, str(value)))
            else:
                f.write(line)

def chose_bots(dic):
    bots = dic["players"]
    scores  = dic["scores"]
    tot = sum(scores)
    dist  = [k/tot if k>0 else 0 for k in scores]
    chosen =  rd.choices(bots,dist,k=size-1)+[bots[-1]]
    mutate_with = []
    for i in range(size):
        j = rd.randint(0, size-1)
        while i == j:
            j = rd.randint(0, size-1)
        mutate_with += [chosen[j]]
    return chosen, mutate_with

def change_bots(chosen,mutate_with,dic):
    weights = [read_weights(bot) for bot in chosen]
    mut_weights = [read_weights(bot) for bot in mutate_with]
    for i in range(size):
        print("player{}.py".format(str(i)) +  " will store " + "{}".format(chosen[i]))
        write_bot(weights[i],"player{}.py".format(str(i)))
    for i in range(size):
        new_weights = change_weights(weights[i],mut_weights[i])
        write_bot(new_weights,"player{}.py".format(str(i+size)))

def eval_perf():
    cmd = "time $(./eval.py > /dev/null 2>&1)"
    os.system(cmd)

def test():
    cmd = "./championnat2.py > /dev/null 2>&1"
    os.system(cmd)
    dic = read_file()
    print(json.dumps(dic))
    chosen,mutate_with =  chose_bots(dic)
    print("mutating bots!")
    change_bots(chosen,mutate_with,dic)
    print("done!")
    eval_perf()

def not_test():
    while datetime.now().hour*100  + datetime.now().minute < 1953:
        test()

not_test()

