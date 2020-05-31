import discord
from discord.ext import commands
import json
import datetime

class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message_edit(self, old_message, new_message):
    	print(old_message.content)
    	print(new_message.content)


    @commands.command(name = 'ping', description = 'basic ping command lol', aliases = ['p'])
    async def ping(self, ctx):
        await ctx.send(f":ping_pong: in {round(self.client.latency * 1000, 2)}ms")

def setup(client):
    client.add_cog(Basic(client))