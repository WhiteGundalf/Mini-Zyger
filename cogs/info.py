import discord
from discord.ext import commands

class Info(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(name="bot_info", description="Displays bot info", aliases=["info", "botinfo", "binfo"])
	async def binfo(self, ctx):
		InfoEmbed = discord.Embed(title="__MiniZyger Info__", color=0x9B59B6, inline=False)
		InfoEmbed.add_field(name="\u200b", value=f"`Owner:` `therealdaneel#7028`, <@!307187938205237250>", inline=False)
		InfoEmbed.set_footer(text=f"requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
		InfoEmbed.set_thumbnail(url=self.client.user.avatar_url)
		InfoEmbed.add_field(name="\u200b", value="`Made For:` `Zyger,` [__Youtube Channel Here__](https://www.youtube.com/channel/UCvYUyKg7wDj760PippmWhig)")

		await ctx.channel.send(embed=InfoEmbed)

	@commands.command(name="server_info", description="Displays server info", aliases=["sinfo", "serverinfo"])
	async def server_info(self, ctx):
		GuildEmbed = discord.Embed(title=f"__{ctx.guild.name.capitalize()} Info__", color=0x9B59B6, inline=False)
		GuildEmbed.add_field(name="\u200b", value=f"`members:` `{len([i for i in ctx.guild.members if i.bot == False])}`", inline=False)
		GuildEmbed.add_field(name="\u200b", value=f"`bots:` `{len([i for i in ctx.guild.members if i.bot == True])}`", inline=False)
		GuildEmbed.add_field(name="\u200b", value=f"`roles:` `{len([i for i in ctx.guild.roles if i.managed == False])}`", inline=False)
		ActiveInvites = await ctx.guild.invites()
		SinfoInvites = [i for i in ActiveInvites if i.max_age == 0 or i.max_uses == 0]
		GuildEmbed.add_field(name="\u200b", value=f"`Invite URL:` [here]({SinfoInvites[0]})")
		BotDevCounter = 0
		for i in ctx.guild.members:
			for role in i.roles:
				if role.id == 671921944962138154:
					BotDevCounter += 1
		GuildEmbed.add_field(name="\u200b", value=f"`Bot Devs:` `{BotDevCounter}`", inline=False)
		GuildEmbed.set_thumbnail(url=ctx.guild.icon_url)
		GuildEmbed.set_footer(text=f"requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
		await ctx.channel.send(embed=GuildEmbed)

	@commands.command(name="role_stats", description="Displays info about a specified role", aliases=["rinfo", "roleinfo"], usage="role")
	async def role_info(self, ctx, *, rolename=None):
		if rolename == None:
			await ctx.channel.send("invalid role name")
			return
		Role=None
		for i in ctx.guild.roles:
			if i.name == rolename:
				Role = i
		if Role == None:
			await ctx.channel.send("invalid role name")
			return
		RoleEmbed = discord.Embed(title=f"{rolename} Stats", color=Role.color, inline=False)
		RoleEmbed.add_field(name="\u200b", value=f"`Role ID:` `{Role.id}`", inline=False)
		RoleEmbed.add_field(name="\u200b", value=f"`Role Color:` `{Role.color}`", inline=False)
		#RoleEmbed.add_field(name="\u200b", value=f"Role Perms: {Role.permissions}", inline=False)
		RoleEmbed.add_field(name="\u200b", value=f"`Member with Role:` `{len(Role.members)}`", inline=False)
		RoleEmbed.add_field(name="\u200b", value=f"`Created At:` `{Role.created_at}`", inline=False)
		RoleEmbed.set_thumbnail(url=self.client.user.avatar_url)
		RoleEmbed.set_footer(text=f"requested by {ctx.message.author}", icon_url= ctx.message.author.avatar_url)
		await ctx.channel.send(embed=RoleEmbed)




def setup(client):
	client.add_cog(Info(client))