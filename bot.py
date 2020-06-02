import discord
from discord.ext import commands

token = 'Token'

def get_prefix(client, message):
    prefixes = ['>']  # sets the prefixes, u can keep it as an array of only 1 item if you need only one prefix

    if not message.guild:
        prefixes = ['>']  # Only allow '==' as a prefix when in DMs, this is optional
    return commands.when_mentioned_or(*prefixes)(client, message)

#client = commands.AutoShardedBot(self_bot=False, command_prefix=">", case_insensitive=True, shard_count=2)
client = commands.Bot(command_prefix = get_prefix, owner_id=307187938205237250, case_insensitive = True)
cogs = ['cogs.basic', 'cogs.info', 'cogs.DiscordPoll', 'cogs.Listeners', 'cogs.joke']

@client.event
async def on_ready():
	print("connected and online")
	client.remove_command('help')
	for cog in cogs:
		try:
			client.load_extension(cog)
		except Exception as error:
			print(error)

client.run(token, bot=True, reconnect=True)
