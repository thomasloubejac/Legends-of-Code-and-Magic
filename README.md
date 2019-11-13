# Legends-of-Code-and-Magic
Our solution to this game on the platform Codingame.com

This led us to a bot that is ranking top 100 in Gold league.

How this works :
main.py is used as a template and a benchmark to evaluate the quality of a generated player.
This base player uses genetic algorithms to find a good enough move according to the evalutaion function.
The evaluation function gives a mark on the impact a certain combination of move will have.
It has a lot of parameters that were empirically chosen. The goal of these scripts is to optimise the evaluation function.
This then allows more accurate evaluation of moves, thus leading to better scores.

## prerequisites

* maven
* java
* python3
* git

## set environment 

In your working directory :
```
git clone https://github.com/thomasloubejac/Legends-of-Code-and-Magic # feel free to rename this one, makes things easier
git clone https://github.com/fala13/LegendsOfCodeAndMagic
cd LegendsOfCodeAndMagic
maven package
mkdir logs
```
The scripts are not that well thought when it comes to paths, rename the ones you come across to fit your situation.
In Legends-of-Code-and-Magic directory :
```
chmod +x make_match.py makebots.py algog.py eval.py championnat2.py
```
The `thread_number`parameter in championnat2.py and eval.py should be modified to fit your system. If your unsure how many threads you can use just ```cat /proc/cpuinfo``` and see what happens.
You also might want to play with the `interval` parameter in case you notice a lot of timeouts happening. These will appear when you comment every ``` > /dev/null 2>&1``` that appear in the `cmd` strings in the scripts.

## execute scripts
This happens in Legends-of-Code-and-Magic directory
### 1. generate random bots
```
mkdir genbots
./make_bots 20
```
this will generate 20 bots with randomized parameters.

### 2. run the algorithm
```
./algog.py
```

### 3. monitor where it's at
```
tail -f perfs
```
to print the win frequencies of the best bot in genbots against the empirical bot in main.py.
