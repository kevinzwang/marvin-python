import asyncio
import aiohttp

async def lmgtfy(message):
    session = aiohttp.ClientSession()
    params = {'q': message}
    resp = await session.get(url='https://lmgtfy.com/', params=params)
    return str(resp.url)