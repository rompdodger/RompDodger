import discord
from discord.ext import commands

class HelpCmd(commands.HelpCommand):
	def __init__(self):
		super().__init__(command_attrs={
			"help": "Shows help about the bot.\n\n"
			             "**<argument>** means the argument is **required**.\n"
			             "**[argument]** means the argument is **optional**.\n"
			             "**[a|b]** means it can be `a` or `b`.\n"
			             "**[argument...]** means you can have **multiple arguments**."
		})
		
	async def send_command_help(self, command):
		ctx = self.context
		
		embed = discord.Embed(color=discord.Color.blurple(), title=f"", description=f"")
		
		if command.signature:
			embed.title += f"{command.name} {command.signature}"
		else:
			embed.title += f"{command.name}"
			
		if command.help:
			embed.description += f"{command.help}"
		else:
			embed.description += "No help given"
			
		return await ctx.send(embed=embed)
		
	async def send_cog_help(self, cog):
		ctx = self.context
		
		embed = discord.Embed(title=f"", description=f"Use `{ctx.prefix}help [command]` for more info on command!\n\n", color=discord.Color.blurple())
		
		if ctx.author.id == ctx.bot.owner_id:
			cc = [cmd for cmd in cog.get_commands()]
		else:
			cc = [cmd for cmd in cog.get_commands() if cmd.hidden is False]
			
		if len(cc) == 0:
			return await ctx.send("No commands found on this cog")
			
		embed.title += f"{cog.qualified_name} Commands"
		
		for command in cc:
			embed.description += f"• {command.name} - {command.help}\n"
		
		return await ctx.send(embed=embed)
		
	async def send_group_help(self, group):
		ctx = self.context
		
		embed = discord.Embed(color=discord.Color.blurple(), title=f"", description=f"")
		
		if group.signature:
			embed.title += f"{group.qualified_name} {group.signature}"
		else:
			embed.title += f"{group.qualified_name}"
			
		gc = [cmd for cmd in group.commands() if cmd.hidden is False]
		if len(gc) == 0:
			return await ctx.send("This group has no sub-commands")
		
		if group.help:
			embed.description += f"{group.help}\n"
		else:
			embed.description += f"No help given\n"
			
		embed.description += f"{gc.name} - {gc.help}\n"
		
		return await ctx.send(embed=embed)
		
	async def send_bot_help(self, mapping):
		ctx = self.context
		
		embed = discord.Embed(title="RompDodger's help menu", description=f"Use `{ctx.prefix}help [category]` for more info!\n\n", color=discord.Color.blurple())
		
		def key(e):
			return len(e.get_commands())
			
		for cog in sorted(ctx.bot.cogs.values(), key=key, reverse=True):
			
			cc = [cmd for cmd in cog.get_commands() if cmd.hidden is False]
			
			if len(cc) == 0:
				continue
				
			embed.description += f"**• {cog.qualified_name}**\n"
			
		embed.description += "\nLinks: [Bot Invite](https://discordapp.com/api/oauth2/authorize?client_id=698040853767389215&permissions=281600&scope=bot) | [Support Server](https://discord.gg/uaQj5ex)"
			
		return await ctx.send(embed=embed)
		
class Help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		bot.help_command = HelpCmd()
		bot.help_command.cog = self
		
def setup(bot):
	bot.add_cog(Help(bot))