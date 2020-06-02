import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.errors import CommandOnCooldown, MissingPermissions, CheckFailure
import json
import datetime
import time
import asyncio


class Polls(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="poll", description="creates a poll", pass_context=True, usage="title; amount of options; option1; option2; option3(etc.)(max = 10); ExpirationTime(defaults to 12h)(formatted like [2h 32m]) ")
    @commands.cooldown(1, 60, BucketType.member)
    #@has_permissions(manage_messages=True)
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
                if AmountOfOptions > 10:
                    AmountOfOptions = 10
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
                        await ctx.channel.send("invalid expiration time, did you format it like '[hours]h [minutes]m'? [ex. 2h 30m]")
                        return
                except:
                    await ctx.channel.send("invalid expiration time, did you format it like '[hours]h [minutes]m'? [ex. 2h 30m]")
                    return
                await ctx.message.delete()
                if TotalTime == 0:
                    TotalTime = 12 * 60 * 60
                    hours = 12
                    minutes = 0
                PollEmbed = discord.Embed(title=f"__{title}__", color=0x9B59B6)
                PollEmbed.set_author(name=f"requested by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
                PollEmbed.set_thumbnail(url=self.client.user.avatar_url)
                OptionCounter= 0
                Emotes = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
                EmoteDict = {Emotes[0]:":one:", Emotes[1]:":two:", Emotes[2]:":three:", Emotes[3]:":four:", Emotes[4]:":five:", Emotes[5]:":six:", Emotes[6]:":seven:", Emotes[7]:":eight:", Emotes[8]:":nine:", Emotes[9]:":keycap_ten:"}
                for i in Options:
                    OptionCounter += 1
                    PollEmbed.add_field(name="\u200b", value=f"**{OptionCounter}**: {i}", inline=False)
                PollEmbed.set_footer(text=f"expires in {hours}h {minutes}m")
                message = await ctx.channel.send(embed=PollEmbed)
                MESSAGE_ID=message.id
                AddedReactions = []
                for i in range(OptionCounter):
                    await message.add_reaction(Emotes[i])
                    AddedReactions.append(Emotes[i])
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
                poll = await ctx.channel.fetch_message(MESSAGE_ID)
                Results_unrefined = {}
                Results = {}
                RefiningResultCounter = 0
                for i in poll.reactions:
                    if RefiningResultCounter < 3:
                        Results.update({EmoteDict[i.emoji]:i.count-1})
                    RefiningResultCounter += 1
                TotalScore = 0
                for i in [int(Results[i]) for i in list(Results.keys())]:
                    TotalScore += i
                EmbedResults = {}

                for i in Results.keys():
                    try:
                        EmbedResults.update({i:[Results[i], round(Results[i]/TotalScore*100, 2)]})
                    except DivisionByZero as e:
                        EmbedResults.update({i:[Results[i], 0]})
                        print(e)

                FinalPollEmbed = discord.Embed(title=title+"[POLL OVER]", color=0x9B59B6)
                PollEmbed.set_author(name=f"requested by {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
                FinalPollEmbed.set_thumbnail(url=self.client.user.avatar_url)
                OptionsToEmotes = {0:":one:", 1:":two:", 2:":three:", 3:":four:", 4:":five:", 5:":six:", 6:":seven:", 7:":eight:", 8:":nine:", 9:":keycap_ten:"}
                OptionCounter= 0
                for i in Options:
                    try:
                        FinalPollEmbed.add_field(name="\u200b", value=f"`{OptionCounter}:` {i}\t**{EmbedResults[OptionsToEmotes[OptionCounter]][1]}%** with **{EmbedResults[OptionsToEmotes[OptionCounter]][0]}** votes", inline=False)
                        OptionCounter += 1
                    except Exception as e:
                        print(e)
                FinalPollEmbed.set_footer(text="expired")
                await message.edit(embed=FinalPollEmbed)
                    

            except Exception as e:
                print(e)
                await ctx.channel.send("Error, did you use the correct format? (>help Polls for more info)")
    @poll.error
    async def poll_error(obj, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.channel.send(f"That command is on a cooldown, try again after **{round(error.retry_after, 2)}s**")
        elif isinstance(error, MissingPermissions):
            ToSend = ''
            for i in error.missing_perms:
                if error.missing_perms[0] == i:
                    ToSend += str(i)
                else:
                    ToSend += ', ' + str(i)
            if len(error.missing_perms) == 1:
                await ctx.channel.send(f"You are missing the following perm: **{ToSend}**", delete_after=3)
                await ctx.message.delete()
            else:
                await ctx.channel.send(f"You are missing the following perms: **{ToSend}**", delete_after=3)
                await ctx.message.delete()





def setup(client):
    client.add_cog(Polls(client))