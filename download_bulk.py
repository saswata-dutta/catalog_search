import json
import asyncio
import aiohttp
import aiofiles


query_params = {"height": 300, "width": 300}


async def download(sema, session, urlPath, fname):
    async with sema:
        async with session.get(urlPath, params=query_params) as response:
            body = await response.read()
            async with aiofiles.open(f"./images/{fname}", "wb") as f:
                await f.write(body)
                return True


async def main():
    urls_files = get_urls_files()
    urls_files = urls_files

    tasks = [None] * len(urls_files)
    timeout = aiohttp.ClientTimeout(total=5)
    connector = aiohttp.TCPConnector(limit=100)
    base_url = "https://dpy2z8n9cxui1.cloudfront.net"

    sema = asyncio.Semaphore(100)
    async with aiohttp.ClientSession(
        base_url=base_url, timeout=timeout, connector=connector, raise_for_status=True
    ) as session:
        for i, urlPath, fname in urls_files:
            tasks[i] = asyncio.create_task(download(sema, session, urlPath, fname))

        results = await asyncio.gather(*tasks, return_exceptions=True)

    for r in results:
        if r is not True:
            print(r)


def get_urls_files():
    with open("lam.json", "r") as f:
        data = json.load(f)
        return [(item["i"], item["url_path"], item["file"]) for item in data]


if __name__ == "__main__":
    asyncio.run(main())
