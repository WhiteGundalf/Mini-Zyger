import discord
from discord.ext import commands

token = 'NzAzMTk2MDQwMTQ0MzU1MzYx.XqP8nQ.LDsHzn9FLwFMYdeCR4OpdPRbG4I'

#client = commands.AutoShardedBot(self_bot=False, command_prefix=">", case_insensitive=True, shard_count=2)
client = commands.Bot(command_prefix = '>', case_insensitive = True)
cogs = ['cogs.basic']

@client.event
async def on_ready():
    print('connected and online')

if __name__ == '__main__':
    for cog in cogs:
        try:
            client.load_extension(cog)
        except Exception as error:
            print(f'cog {cog} failed to load. Error: {error}')

    client.run(token)