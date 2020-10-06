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
