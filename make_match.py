#!/usr/bin/python3

import os

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("p1")
parser.add_argument("p2")
parser.add_argument("match_id")


args = parser.parse_args()

os.chdir("../LegendsOfCodeAndMagic")
cmd = "java -jar -Dleague.level=4 target/LegendsOfCodeAndMagic-1.0.jar -p1 \"python3 /home/gabelin/Legends-of-Code-and-Magic/genbots/{}\" -p2 \"python3 /home/gabelin/Legends-of-Code-and-Magic/genbots/{}\" -l ./logs/game{}.json".format(args.p1, args.p2, args.match_id)

print(cmd)

os.system(cmd)
