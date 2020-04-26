import json
import discord
from utils.time import format_time
from utils import utilities
from discord.ext import commands
from discord import Embed

class Events(commands.Cog):
	"""Event Handler for RompDodger"""
	def __init__(self, bot):
		self.bot = bot
			
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		
		if hasattr(ctx.command, 'on_error'):
			return
			
		if isinstance(error, (commands.CommandNotFound, commands.NoPrivateMessage)):
			return
			
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.send(embed=await utilities.generate_embed(f"Command {ctx.prefix} {ctx.command} requires **{error.param.name}** argument, but you missed giving that"))
		elif isinstance(error, commands.BotMissingPermissions):
			perms = "".join(error.missing_perms)
			await ctx.send(embed=await utilities.generate_embed(f"To finish the command bot must have {perms} permission, give the bot appropriate permissions and re-try"))
		self.bot.logger.critical(f"Ignoring Exception in {ctx.command}\nError: {error}")
			
	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		#TODO: implement blacklist sytem
		self.bot.logger.info(f"Joined on {guild} > Total Guilds: {len(self.bot.guilds)}")
		
	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		self.bot.logger.info(f"Removed on {guild} > Total Guilds: {len(self.bot.guilds)}")
		
	@commands.Cog.listener()
	async def on_member_join(self, member):
		cursor = await self.bot.db.execute(f"SELECT channel FROM welcomer WHERE guild_id = {member.guild.id}")
		chrow = await cursor.fetchone()
		if chrow is None:
			return
		else:
			msgrow = await self.bot.db.execute(f"SELECT message FROM welcomer WHERE guild_id = {member.guild.id}")
			msg = await msgrow.fetchone()
			name = member.name
			mention = member.mention
			members = member.guild.member_count
			server = member.guild
			embed = discord.Embed(color=discord.Color.dark_green(), description=msg[0].format(name=name, mention=mention, members=members, server=server))
			embed.set_thumbnail(url=f"{member.avatar_url_as(format='png', size=2048)}")
			created = format_time(member.created_at)
			embed.set_footer(text=f"{member.name} Created on {created}")
			ch = self.bot.get_channel(int(chrow[0]))
			await ch.send(embed=embed)
		await cursor.close()
			
	@commands.Cog.listener()
	async def on_member_remove(self, member):
		cursor = await self.bot.db.execute(f"SELECT channel FROM leaver WHERE guild_id = {ctx.guild.id}")
		chrow = await cursor.fetchone()
		if chrow is None:
			return
		else:
			msg = await self.bot.db.execute(f"SELECT msg FROM leaver WHERE guild_id = {member.guild.id}")
			name = member.name
			mention = member.mention
			server = member.server
			members = member.guild.member_count
			embed.set_thumbnail(url=f"{member.avatar_url_as(format='png', size=2048)}")
			created = format_time(member.joined_at)
			embed.set_footer(text=f"{member.name} Created joined on {joined}")
			ch = self.bot.get_channel(int(chrow[0]))
			await ch.send(embed=embed)
		await cursor.close()
		
def setup(bot):
	bot.add_cog(Events(bot))