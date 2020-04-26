import time
import discord
import aiohttp
import urllib
from discord import Embed

async def generate_embed(content: str):
	embed = Embed()
	embed.color = discord.Color.blurple()
	embed.description = content
	
	return embed

async def make_screenshot(site):
	encoded_url = urllib.parse.quote(site)
	base = f"https://api.apiflash.com/v1/urltoimage?access_key=cdbb736cd448434d87a89239f63f8604&fresh=true&url={encoded_url}"
	async with aiohttp.ClientSession() as session:
		async with session.get(base) as responce:
			data = await responce.json()
			
	return data["url"]
	
async def check_latency(site):
	start = time.monotonic()
	async with aiohttp.ClientSession() as session:
		async with session.get(site) as data:
			if data.status == 200:
				end = time.monotonic()
			else:
				end = "Failed to get ping!"
	final = round((end - start) * 1000)
	
	return final
	
async def post_to_hastebin(message):
	base = "https://hasteb.in"
	async with aiohttp.ClientSession() as session:
		async with session.post(base + "/documents", data=message) as responce:
			key = (await responce.json())["key"]
	
	return f"https://hasteb.in/{key}"