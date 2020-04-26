import random
import urllib
import json
import io
import re
import asyncio
import dadjokes
import aiohttp
import discord
from utils.utilities import generate_embed
from discord.ext import commands

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.joke = dadjokes.Dadjoke()
		
	@commands.command()
	async def bitcoin(self, ctx):
		"""Shows bitcoin current price in USD($)"""
		r = await self.bot.session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json")
		r = await r.text()
		r = json.loads(r)
		await ctx.send(embed=await generate_embed(f"Bitcoin Price: {r['bpi']['USD']['rate']}$"))
		
	@commands.command()
	async def dadjoke(self, ctx):
		"""Sends you the dadjoke!"""
		joke = self.joke.joke
		await ctx.send(embed=await generate_embed(joke))

	@commands.command()
	async def fact(self, ctx):
		"""Sends some useless facts!"""
		r = await self.bot.session.get("https://useless-facts.sameerkumar.website/api")
		data = await r.json()
		await ctx.send(embed=await generate_embed(data["data"]))
		
	@commands.command()
	async def meme(self, ctx):
		"""Gives you a dankmeme from reddit"""
		r = await self.bot.session.get("https://www.reddit.com/r/dankmemes/top.json?sort=top&t=day&limit=500")
		r = await r.json()
		data = random.choice(r["data"]["children"])["data"]
		img = data["url"]
		title = data["title"]
		embed = discord.Embed(title=title, color=self.bot.main_color)
		embed.set_image(url=img)
		await ctx.send(embed=embed)
		
	@commands.command(aliases=['ss'])
	async def screenshot(self, ctx, *, site):
		"""Make screenshot of given site
		Must be a Valid Site"""
		match = re.search(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", site) # taken from dpy server(?tag url regex)
		if match:
			async with ctx.channel.typing():
				url = urllib.parse.quote(site)
				r = await self.bot.session.get(f"https://api.apiflash.com/v1/urltoimage?access_key=cdbb736cd448434d87a89239f63f8604&fresh=true&url={url}")
				buffer = io.BytesIO(await r.read())
				f = discord.File(buffer, filename="ss.png")
				embed = discord.Embed(coloer=discord.Color.blurple())
				embed.set_image(url="attachment://ss.png")
				await ctx.send(file=f, embed=embed)
		else:
			await ctx.send(embed=await generate_embed(f"{ctx.red_tick()} Not a valid URL or Internal Error"))
		
def setup(bot):
	bot.add_cog(Fun(bot))