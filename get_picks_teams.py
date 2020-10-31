import argparse
import sys
import logging
import asyncio
import aiohttp
import csv

from pprint import pprint
from yaspin import yaspin
from pathlib import Path
from fpl import FPL

from utils import position_converter, team_converter

playing_players = {}
benched_players = {}
captained_players = {}


async def get_gameweek_picks(gw, teams):
    """
    gameweek picks
    """
    async with aiohttp.ClientSession() as session:
        with yaspin(text="Fetching data from FPL api", color="yellow") as spinner:
            for team in teams:
                fpl = FPL(session)
                user = await fpl.get_user(team)
                spinner.write(f">>  {user}")
                # current_event = user.current_event
                picks = await user.get_picks(gw)
                # entry_history = await user.get_user_history(gw)
                # print()
                # print(current_event)
                # print("Printing picks")
                # # playing_picks = list(filter(lambda x: x["position"] <= 11, picks[gw]))
                for pick in picks[gw]:
                    if pick["is_captain"]:
                        captained_players[pick["element"]] = (
                            captained_players.get(pick["element"], 0) + 1
                        )
                    if pick["position"] <= 11:
                        playing_players[pick["element"]] = (
                            playing_players.get(pick["element"], 0) + 1
                        )
                    else:
                        benched_players[pick["element"]] = (
                            benched_players.get(pick["element"], 0) + 1
                        )
            playing_players_sorted = sorted(
                playing_players.items(), key=lambda x: x[1], reverse=True
            )
            benched_players_sorted = sorted(
                benched_players.items(), key=lambda x: x[1], reverse=True
            )
            captained_players_sorted = sorted(
                captained_players.items(), key=lambda x: x[1], reverse=True
            )
            # pprint()
            # pprint()
            # pprint(benched_players)
            # pprint(entry_history)

            fpl = FPL(session)
            try:
                Path(f"results/GW{gw}").mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(e)
            captains_file = (
                f'results/GW{gw}/CAPTAINS_{gw}_{"_".join(str(t) for t in teams)}.csv'
            )
            playing_file = (
                f'results/GW{gw}/PLAYING_{gw}_{"_".join(str(t) for t in teams)}.csv'
            )
            benched_file = (
                f'results/GW{gw}/BENCHED_{gw}_{"_".join(str(t) for t in teams)}.csv'
            )
            try:
                with open(captains_file, "w+") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(
                        [
                            "SN",
                            "Player",
                            "Count",
                            "GW Points",
                            "Total Points",
                            "position",
                            "club",
                        ]
                    )
                    players = await fpl.get_players(
                        dict(captained_players_sorted).keys()
                    )
                    print("\nCAPTAINS")
                    for i, player in enumerate(players, start=1):
                        print(player.web_name, end=" ")
                        print("point=", player.event_points, end=" ")
                        print("count=", dict(captained_players_sorted)[player.id])
                        writer.writerow(
                            [
                                i,
                                player.web_name,
                                dict(captained_players_sorted)[player.id],
                                player.event_points,
                                player.total_points,
                                position_converter(player.element_type),
                                team_converter(player.team),
                            ]
                        )

            except IOError as e:
                print(e)
                print("I/O error")
            try:
                with open(playing_file, "w+") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(
                        [
                            "SN",
                            "Player",
                            "Count",
                            "GW Points",
                            "Total Points",
                            "position",
                            "club",
                        ]
                    )
                    players = await fpl.get_players(dict(playing_players_sorted).keys())
                    print("\nPLAYING")
                    for i, player in enumerate(players, start=1):
                        print(player.web_name, end=" ")
                        print("point=", player.event_points, end=" ")
                        print("count=", dict(playing_players_sorted)[player.id])
                        writer.writerow(
                            [
                                i,
                                player.web_name,
                                dict(playing_players_sorted)[player.id],
                                player.event_points,
                                player.total_points,
                                position_converter(player.element_type),
                                team_converter(player.team),
                            ]
                        )

            except IOError as e:
                print(e)
                print("I/O error")

            try:
                with open(benched_file, "w+") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(
                        [
                            "SN",
                            "Player",
                            "Count",
                            "GW Points",
                            "Total Points",
                            "position",
                            "club",
                        ]
                    )
                    players = await fpl.get_players(dict(benched_players_sorted).keys())
                    print("\nBENCHED")
                    for i, player in enumerate(players, start=1):
                        print(player.web_name, end=" ")
                        print("point=", player.event_points, end=" ")
                        print("count=", dict(benched_players_sorted)[player.id])
                        writer.writerow(
                            [
                                i,
                                player.web_name,
                                dict(benched_players_sorted)[player.id],
                                player.event_points,
                                player.total_points,
                                position_converter(player.element_type),
                                team_converter(player.team),
                            ]
                        )

            except IOError as e:
                print(e)
                print("I/O error")


# Main Script
parser = argparse.ArgumentParser(description="Get team picks for gw")
parser.add_argument("-g", "--gameweek", help="gameweek number", type=int, required=True)
parser.add_argument(
    "-t", "--team", help="team id one or more", nargs="+", type=int, required=True
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
    gameweek = args["gameweek"]
    team_ids = args["team"]
    p_table = args["notable"]
    # for team_id in team_ids:
    asyncio.run(get_gameweek_picks(gameweek, team_ids))
except Exception as e:
    print("Error occured")
    logging.error(e)
