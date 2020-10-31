# FPL-Scripts-Stats
Scripts for Fantasy Premier League(FPL) for making some tasks easy and also to get statistics using FPL api.

This will be collection of python scripts for Fantasy Premier League

## Current Features
- Get sorted mini-league managers based on points output to console and csv file

Note: League ID is the number you see on url on your browser when you open the mini-league.

Here is example: League ID on image below is 14476
<img src="https://i.imgur.com/jx2Fm8u.png" alt="fantasy_mini_leauge_on_browser"></img>
## How to run the script
1. Install python on your system and version should be `3.6+`
2. Clone the repository or download zip available by slecting download icon with code
```sh
#clone repo
git clone https://github.com/yathomasi/FPL-Scripts-Stats.git
#change directory
cd FPL-Scripts-Stats
```
3. Create Python Environment (based on your python setup, please use `python` or  `python3`)
```sh
python -m venv venv #or python3 -m venv venv
#source python to environment
source venv/bin/activate
```
4. Install all the python package requirements(`pip` or `pip3` based on your setup) 
```sh
pip install -r requirements.txt
```
5. Copy the `.env_example` and rename it to `.env` only (use GUI if you want or here is command)
```sh
cp .env_example .env
```
 if you open this environment file you can see two fields `USERNAME` and `PASSWORD`, currently there is a dummy account if you don't want to put yours 
but you can also put your account here and upon further features addition it would be better if you set your own account

6. You are ready to run the script (eg.league_gw_sorted.py)
```sh
#for help pass -h or --help tag
python league_gw_sorted.py -h
#provide leagues id by using -l or --league tag and you can even pass multiple league id
python league_gw_sorted.py -l 1234 2345
#by default it also prints table to console you can disable by passing -nt or --no-table tag
python league_gw_sorted.py -l 1123 -nt
# for no of players stat
 python get_picks_teams.py -g 7 -t 1234 2345
```
7. Find the respective Gameweek folder name `GW` and you will find the exported csv file and also by defaults you can see printed table on console too

## TODO features
- get sorted gw file for all the mini-league on my account

## Contributing
1. You can open [issue](https://github.com/yathomasi/FPL-Scripts-Stats/issues) if you find some error or want some help or contact directly to me at [@yathomasi](https://twitter.com/yathomasi)
2. Pull request are always welcome
3. If you have any idea and you want that to be implemented we can add that to our TODO.

### Thanks
Thanks @amosbastian for `fpl` a python wrapper for the api
