import asyncio

headers = {"User-Agent": ""}


async def fetch(session, url, retries=5, cooldown=1):
    retries_count = 0

    while True:
        async with session.get(url, headers=headers, raise_for_status=True) as response:
            result = await response.json()
            return result
        retries_count += 1
        if retries_count > retries:
            raise Exception(f"Could not fetch {url} after {retries} retries")

        if cooldown:
            await asyncio.sleep(cooldown)


def position_converter(position):
    """Converts a player's `element_type` to their actual position."""
    position_map = {1: "Goalkeeper", 2: "Defender", 3: "Midfielder", 4: "Forward"}
    return position_map[position]


def team_converter(team_id):
    """Converts a team's ID to their actual name."""
    team_map = {
        1: "Arsenal",
        2: "Aston Villa",
        3: "Brighton",
        4: "Burnley",
        5: "Chelsea",
        6: "Crystal Palace",
        7: "Everton",
        8: "Fulham",
        9: "Leicester",
        10: "Leeds",
        11: "Liverpool",
        12: "Man City",
        13: "Man Utd",
        14: "Newcastle",
        15: "Sheffield Utd",
        16: "Southampton",
        17: "Spurs",
        18: "West Brom",
        19: "West Ham",
        20: "Wolves",
        None: None,
    }
    return team_map[team_id]
