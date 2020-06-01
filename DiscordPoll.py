import discord
from discord.ext import commands
import json
import datetime
import time
import asyncio


class Polls(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="poll", description="creates a poll", usage="title; amount of options; option1; option2; option3(etc.)(max = 10); ExpirationTime(defaults to 12h)(formatted like [2h 32m]) ")
    async def poll(self, ctx):
        if not ctx.message.author.bot:
            try:
                MsgContent = ctx.message.content
                MsgContentList = MsgContent.split('; ')
                title = ''
                for i in MsgContentList[0].split(' '):
                    if i != ">poll" and i != "<@!716640483471917176> poll":
                        title += i + ' '
                AmountOfOptions = int(MsgContentList[1])
                Options = MsgContentList[2:]
                Options = Options[:AmountOfOptions]
                Expiration = MsgContentList[-1]
                TotalTime = 0
                minutes = 0
                hours = 0
                try:
                    ListExpiration = Expiration.split(" ")
                    if len(ListExpiration) == 1:
                        if ListExpiration[0].endswith("h"):
                            hours = int(ListExpiration[0].strip("h"))
                            TotalTime = hours * 60 * 60
                        elif ListExpiration[0].endswith("m"):
                            minutes = int(ListExpiration[0].strip("m"))
                            if minutes > 60:
                                hours += round(minutes/60)
                                minutes -= hours*60
                                TotalTime = minutes * 60 + hours * 60 * 60
                            TotalTime = minutes * 60
                    elif len(ListExpiration) == 2:
                        if ListExpiration[0].endswith("h") and ListExpiration[1].endswith("m"):
                            hours = int(ListExpiration[0].strip("h"))
                            minutes = int(ListExpiration[1].strip("m"))
                            TotalTime = hours * 60 * 60 + minutes * 60
                    else:
                        await ctx.channel.send("invalid expiration time, did you format it like 'xh ym'? [ex. 2h 30m]")
                        return
                except:
                    await ctx.channel.send("invalid expiration time, did you format it like 'Xh Ym'? [ex. 2h 30m]")
                    return
                if TotalTime == 0:
                    TotalTime = 12 * 60 * 60
                    hours = 12
                    minutes = 0
                PollEmbed = discord.Embed(title=title, color=0x9B59B6)
                PollEmbed.set_thumbnail(url=self.client.user.avatar_url)
                OptionCounter= 0
                Emotes = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
                for i in Options:
                    OptionCounter += 1
                    PollEmbed.add_field(name="\u200b", value=f"`{OptionCounter}:` {i}", inline=False)
                PollEmbed.set_footer(text=f"expires in {hours}h {minutes}m")
                message = await ctx.channel.send(embed=PollEmbed)
                for i in range(OptionCounter):
                    await message.add_reaction(Emotes[i])
                TimeMessageCreated = time.time()
                timeleft = TotalTime
                while round(time.time() - TimeMessageCreated) < TotalTime:
                    await asyncio.sleep(60)
                    timeleft -= 60
                    workingTime = timeleft
                    ReFormatHours = 0
                    if workingTime/60 >= 60:
                        ReFormatHours += round(timeleft/60/60)
                        workingTime -= 60*60*ReFormatHours
                        ReformatMinutes = round(workingTime/60)
                        if ReformatMinutes < 0:
                            ReFormatHours -= 1
                            ReformatMinutes += 60
                        
                    else:
                        ReFormatHours = 0
                        ReformatMinutes = round(workingTime/60)
                    PollEmbed.set_footer(text=f"Expires in {ReFormatHours}h {ReformatMinutes}m")
                    await message.edit(embed=PollEmbed)
                await ctx.channel.send(f"<@!{ctx.message.author.id}>, the poll has finished.")

            except Exception as e:
                await ctx.channel.send("Error, did you use the correct format? (>help Polls for help)")


def setup(client):
    client.add_cog(Polls(client))