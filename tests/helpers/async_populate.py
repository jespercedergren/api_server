import asyncio
from aiohttp import ClientSession
import argparse

payloads = []

for i in range(100):
    payload = {f"key_{i}": i, f"key_{i+1}": {f"key_{i+1}_nested": i+1}}
    payloads.append(payload)


async def post_payload(session, payload, url):
    resp = await session.request(method="POST", url=url, json=payload)


async def main(url):
    async with ClientSession() as session:
        await asyncio.gather(*[post_payload(session, payload, url) for payload in payloads])


def parse_args():
    parser = argparse.ArgumentParser(description='Send payloads asyncronously to url.')
    parser.add_argument('--url', action='store', help='The url to send payloads to.')
    return parser.parse_args()


import time

if __name__ == "__main__":
    args = parse_args()
    s = time.perf_counter()
    #url = "http://0.0.0.0:80"
    #url = "http://0.0.0.0:80/api/ingest_data/firehose"
    url = args.url
    asyncio.run(main(url))
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")