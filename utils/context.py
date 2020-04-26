import discord
from discord.ext import commands

class Context(commands.Context):
	"""Custom context"""
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
	@property
	def session(self):
		return self.bot.session
		
	@property
	def db(self):
		return self.bot.db
		
	def green_tick(self):
		return "<:greenTick:699877218779660338>"
		
	def red_tick(self):
		return "<:redTick:699877187758588024>"