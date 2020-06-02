import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions, CheckFailure
import asyncio
from discord.ext.commands import has_permissions

# 706877664333660160: muted role id

class Listeners(commands.Cog):
	def __init__(self, client):
		self.client = client


			

	@commands.Cog.listener()
	async def on_message(self, message):
		try:
			if message.guild.id == 662052049248190504:
				def muted_check(user_id):
					with open("muted.txt", "r") as f:
						if f.readlines() != []:
							lines = [int(i.strip()) for i in f.readlines()]
							if lines == []:
								return False
							else:
								if i in lines:
									return True
								else:
									return False
						else:
							return False

				if message.channel.id != 699598809096912986 and message.channel.id != 689530345468592137:

					if message.author.bot == True and message.author.id != 716640483471917176:
						await message.delete()
				if "how" in message.content.lower() and "get" in message.content.lower() and "simp" in message.content.lower():
					await message.channel.send("1. Act like a simp\n2. Put Simp in your name\n3.Wait for an Admin to notice you and give you the role\n4. Be friendly and responsible")

				if muted_check(message.author.id) == True and random.randint(0, 100)%10 == 0:
					await message.delete()

		except Exception as e:
			print(e)

	@commands.command(name="random_delete", description="deletes the message of the given user randomly", aliases=["randdel","rand_del","randelete", "randomdel"], usage="member", pass_context=True)
	async def random_delete(self, ctx, member):
		try:
			member = member.strip("<@!").strip(">")
			if int(member) in [i.id for i in ctx.guild.members]:
				with open("muted.txt", "a+") as f:
					f.write(member)
			else:
				await ctx.channel.send("invalid user specified", delete_after=5)
		except Exception as e:
			print(e)
			await ctx.channel.send("Error", delete_after=5)

	@commands.command(name="cancel_random_delete", description="stops random deletion of given users messages", aliases=["cancelranddelete", "cancelrandomdelete", "cancelranddel", "crandel"], usage="muted_member", pass_context=True)
	async def cancel_random_delete(self, ctx, member):
		try:
			member = member.strip("<@!").strip(">")
			with open("muted.txt", "a+") as f:
				lines = [i.strip() for i in f.readlines()]
				if member in lines:
					lines.remove(member)
					f.truncate()
					for i in lines:
						f.write(i)
		except Exception as e:
			print(e)
			await ctx.channel.send("Error", delete_after=5)



def setup(client):
	client.add_cog(Listeners(client))