import asyncio
import aiohttp

from threads import save_flag, BASE_URL, show, main


async def download_one(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    async with aiohttp.request("GET", url) as resp:
        image = await resp.read()
        show(cc)
        save_flag(image, cc.lower() + '.gif')


def download_many(cc_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(cc) for cc in sorted(cc_list)]
    wait_coro = asyncio.wait(to_do)
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()
    return len(res)


if __name__ == '__main__':
    main(download_many)