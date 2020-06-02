import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions
import asyncio
import random

class Jokes(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(name = "Daneel", description="here you go, you xp-hungry mofo")
	async def Daneel(self, ctx):
		if ctx.message.author.bot == False:
			await ctx.channel.send(f"<@!{ctx.message.author.id}>, you gained {random.randint(10000, 100000)} xp")

	@commands.command(name="Gundalf", description="posts Triggered Gundalf")
	async def Gundalf(self, ctx):
		GundalfEmbed = discord.Embed(color=0xE74C3C)
		GundalfEmbed.set_image(url="https://media.discordapp.net/attachments/662052049827135520/717285561467142246/gundalf_deepfried.png")
		await ctx.channel.send(embed=GundalfEmbed)


def setup(client):
	client.add_cog(Jokes(client))