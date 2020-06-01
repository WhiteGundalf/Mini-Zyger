import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions, CheckFailure
import asyncio

class Listeners(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self, message):
		try:
			if message.channel.id != 699598809096912986 and message.channel.id != 689530345468592137:
				if message.content.startswith("pls") or message.content.startswith("!"):
					role = message.guild.get_role(706877664333660160)
					# 716640483471917176 <--- my id
					# 706877664333660160 <--- muted role id
					await message.author.add_roles(role)
					await message.channel.send(f"muted <@!{message.author.id}> for using bot commands in the wrong channel. [10 minutes]")
					await asyncio.sleep(10*60)
					await message.author.remove_roles(role)
					await message.channel.send(f"unmuted <@!{message.author.id}>")

				if message.author.bot == True and message.author.id != 716640483471917176:
					await message.delete()
			if "how" in message.content.lower() and "get" in message.content.lower() and "simp" in message.content.lower():
				await message.channel.send("1. Act like a simp\n2. Put Simp in your name\nWait for an Admin to notice you and give you the role\n4. If you annoy the staff they *can* and *will* take it away")
		except Exception as e:
			print(e)

def setup(client):
	client.add_cog(Listeners(client))