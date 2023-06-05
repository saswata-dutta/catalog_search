import json
import asyncio
import aiohttp
import aiofiles
from urllib.parse import urlparse

query_params = {"height": 300, "width": 300}


async def download(session, url, file):
    async with session.get(url, params=query_params) as response:
        async with aiofiles.open(f"./images/{file}", "wb") as f:
            await f.write(await response.read())
            return True


async def main():
    urls_files = get_urls_files()
    urls_files = urls_files[:10]

    tasks = [None] * len(urls_files)
    timeout = aiohttp.ClientTimeout(total=2)
    connector = aiohttp.TCPConnector(limit=50)
    base_url = "https://dpy2z8n9cxui1.cloudfront.net/"

    async with aiohttp.ClientSession(
        base_url=base_url, timeout=timeout, connector=connector, raise_for_status=True
    ) as session:
        for i, url, file in urls_files:
            urlPath = urlparse(url).path
            tasks[i] = asyncio.create_task(download(session, urlPath, file))

        results = await asyncio.gather(*tasks, return_exceptions=True)

    for r in results:
        if r is not True:
            print(r)


def get_urls_files():
    with open("lam.json", "r") as f:
        data = json.load(f)
        return [(item["i"], item["url"], item["file"]) for item in data]


if __name__ == "__main__":
    asyncio.run(main())
