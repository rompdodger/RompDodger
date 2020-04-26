import datetime
import platform
import discord
from utils.time import format_time
from discord.ext import commands

class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	async def avatar(self, ctx, *, member: discord.Member=None):
		"""Gives you the avatar of you nor the pinged member"""
		if not member:
			member = ctx.author
		img = member.avatar_url_as(format="png", size=2048)
		embed = discord.Embed(color=discord.Color.blurple())
		embed.set_image(url=img)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def botinfo(self, ctx):
		"""Shows info about a bot"""
		uptime = datetime.datetime.utcnow() - self.bot.load_time
		hrs, remainder = divmod(int(uptime.total_seconds()), 3600)
		mins, sec = divmod(remainder, 60)
		days, hrs = divmod(hrs, 24)
		fmt = f""
		if days:
			fmt += f"{days}d {hrs}h {mins}m {sec}s"
		else:
			fmt += f"{mins}m {hrs}h {mins}m {sec}s"
		ping = round(self.bot.latency * 1000)
		embed = discord.Embed(description="__**RompDodger is a discord bot that does some stuff**__", color=self.bot.main_color)
		embed.set_thumbnail(url=self.bot.user.avatar_url)
		embed.add_field(name="Bot Stats", value=f"Guilds: {len(self.bot.guilds)}\nUsers: {len(self.bot.users)}\nUptime: {fmt}\nPing: {ping}ms")
		embed.add_field(name="Code stats", value=f"Made using: discord.py({discord.__version__})\nCommands: {len(self.bot.commands)}\nCogs: {len(self.bot.cogs)}")
		await ctx.send(embed=embed)
		
	@commands.command()
	async def serverinfo(self, ctx):
		"""Shows info about the server"""
		guild = ctx.guild
		id = guild.id
		region = guild.region
		afk_timeout = guild.afk_timeout
		afk_channel = guild.afk_channel
		boost_tier = guild.premium_tier
		boost_count = guild.premium_subscription_count
		members = len(guild.members)
		bots = 0
		for member in guild.members:
			if member.bot:
				bots += 1
		created = format_time(guild.created_at)
		embed = discord.Embed(color=discord.Color.blurple())
		embed.set_thumbnail(url=guild.icon_url)
		embed.add_field(name="**General Info**", value=f"Name: {guild.name}\nID: {id}\nOwner: {guild.owner}\nRegion: {region}\nCreated: {created}\nChannels: Text: {len(guild.text_channels)} | Voice: {len(guild.voice_channels)}\nVC Bitrate Limit: {round(guild.bitrate_limit)}kbps\nFile Upload limit: {round(guild.filesize_limit)}mb\nEmoji limit: {guild.emoji_limit}(used: {len(guild.emojis)})")
		roles = ''.join(r.mention for r in ctx.guild.roles[:-11:-1] if not r.name == "@everyone")
		embed.add_field(name="**Role & Member Info**", value=f"Members: {members} and {bots} bots\nRoles: {roles}")
		await ctx.send(embed=embed)
		
	@commands.command()
	async def userinfo(self, ctx, *, member: discord.Member=None):
		"""Shows info about you/given menber"""
		if not member:
			member = ctx.author
			
		id = member.id
		name = member.name
		created = format_time(member.created_at)
		joined = format_time(member.joined_at)
		status = member.status
		embed = discord.Embed(title=f"{name}'s Information", color=ctx.author.top_role.color)
		embed.add_field(name="**General Information**", value=f"__Discord Name__: {name}\n__ID__: {id}\n__Created__: {created}")
		roles = ''.join([r.mention for r in member.roles[:-11:-1] if not r.name == "@everyone"])
		embed.add_field(name=f"**Server Information**", value=f"__Joined At__: {joined}\n__Nickname__: {member.nick}\n__Roles__: {roles}")
		embed.set_thumbnail(url=member.avatar_url)
		await ctx.send(embed=embed)
		
	@commands.command()
	async def joined(self, ctx, *, member: discord.Member=None):
		"""Shows the joined date of you/given member"""
		if not member:
			member = ctx.author
			
		joined = format_time(member.joined_at)
		embed = discord.Embed(color=ctx.author.top_role.color, description=f"{member.name} joined at {joined}")
		await ctx.send(embed=embed)
		
def setup(bot):
	bot.add_cog(Info(bot))