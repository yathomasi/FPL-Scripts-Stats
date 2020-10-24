import aiohttp
import asyncio
import csv
import argparse
import logging
import sys
import os
import re

from yaspin import yaspin
from tqdm import tqdm
from prettytable import PrettyTable

from pathlib import Path
from fpl import FPL
from dotenv import load_dotenv

from utils import fetch

load_dotenv()

# LOGIN INFORMATION IS REQUIRED TO FETCH DATA FROM API
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


# Function Definations
async def event_finished_status(session):
    GW = 0
    status = await fetch(session, "https://fantasy.premierleague.com/api/event-status/")
    if status:
        for s in status["status"]:
            GW = s["event"]
            if not s["bonus_added"]:
                return False, GW
        if not status["leagues"] == "Updated":
            return False, GW
        return True, GW
    else:
        raise ("Error getting data")


async def fpl_league_standing(league_id, table):
    async with aiohttp.ClientSession() as session:
        with yaspin(text="Fetching data from FPL api", color="yellow") as spinner:
            fpl = FPL(session)
            await fpl.login(USERNAME, PASSWORD)

            classic_league = await fpl.get_classic_league(league_id)
            spinner.write(f">>  {classic_league}")
            page = 1
            page_new_entries = 1
            phase = 1
            all_standings = []
            try:
                event_status, GW = await event_finished_status(fpl.session)
                Path(f"GW{GW}").mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logging.error(e)
            if event_status:
                spinner.write(f">> Gameweek {GW} is finished ")
            else:
                spinner.write(
                    f"!!! Gameweek {GW} is not finished or it's updating... !!"
                )

            while True:
                standings = await classic_league.get_standings(
                    page=page, page_new_entries=page_new_entries, phase=phase
                )
                all_standings.extend(standings["results"])
                if not standings["has_next"]:
                    spinner.ok("✅ ")
                    break
                page += 1
        spinner.stop()

    player_table = PrettyTable()
    player_table.field_names = [
        "SN",
        "Manager",
        "Team Name",
        "GW",
        "Total",
        "Rank",
        "Previous Rank",
        "Team ID",
    ]
    player_table.align["GW"] = "l"

    gw_sort_standings = sorted(
        all_standings, key=lambda x: x["event_total"], reverse=True
    )
    # print(gw_sort_standings)
    csv_file = f"{classic_league}-GW{GW}.csv"
    file = re.sub(r"[^\w .\d-]", "_", csv_file)
    gw_file = f"GW{GW}/{file}"
    try:
        with open(gw_file, "w+") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "SN",
                    "Manager",
                    "Team Name",
                    "GW",
                    "Total",
                    "Rank",
                    "Previous Rank",
                    "Team ID",
                ]
            )
            for i, player in enumerate(tqdm(gw_sort_standings), start=1):
                sn = i
                manager = player["player_name"]
                team_name = player["entry_name"]
                gw = player["event_total"]
                total = player["total"]
                rank = player["rank"]
                previous_rank = player["last_rank"]
                team_id = player["entry"]
                player_table.add_row(
                    [sn, manager, team_name, gw, total, rank, previous_rank, team_id]
                )
                writer.writerow(
                    [sn, manager, team_name, gw, total, rank, previous_rank, team_id]
                )

    except IOError as e:
        print(e)
        print("I/O error")

    if table:
        print(player_table)


# Main Script
parser = argparse.ArgumentParser(
    description="Get sorted list of manager in mini-league in current GW"
)
parser.add_argument(
    "-l", "--league", help="league entry id", nargs="+", type=int, required=True
)
parser.add_argument(
    "-nt",
    "--notable",
    action="store_false",
    help="do not show table on console",
)
parser.add_argument("-d", "--debug", action="store_true", help="deubg mode on")
args = vars(parser.parse_args())

if args["debug"]:
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

try:
    league_ids = args["league"]
    p_table = args["notable"]
    for league_id in league_ids:
        asyncio.run(fpl_league_standing(league_id, p_table))
except Exception as e:
    print("Error occured")
    logging.error(e)
