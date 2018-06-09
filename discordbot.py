from discord.ext.commands import Bot
import time
import datetime
import random
import discord
import asyncio
import pytz
import os

Client = discord.Client()
client = Bot(command_prefix="$")

RapGod_id = "324332386219327488"

urls = ["https://media.giphy.com/media/9pCESofHVLvcA/giphy.gif",
        "https://media.giphy.com/media/iAQFuaZSrDnBuVCdZO/giphy.gif",
        "https://media.discordapp.net/attachments/291284109232308226/454794855021805578/raw.gif",
        "https://media.giphy.com/media/5Yl6uqC0YQHejTKi7Q/giphy.gif",
        "https://media.giphy.com/media/5UH4ZEelyBwwIW8E2k/giphy.gif",
        "https://media.giphy.com/media/26Ff0l4TARWjMTSKs/giphy.gif"]

with open("swear.txt", "rt") as fp:
    filter = fp.readlines()
    filter = [x.strip() for x in filter]
# print(filter)


async def background_loop():
    Time = datetime.datetime.now(pytz.timezone("US/Central"))  # Gets time when the message was sent
    print(str(Time.minute))
    if Time.minute % 5 == 0:
        embed = discord.Embed(title="GIF of the Hour", color=0x059789)
        embed.set_image(url=random.choice(urls))  # Displays gif
        # await client.send_message(discord.Object("454027523270115358"), embed=embed)
        # await client.send_message(discord.Object("454369180951511051"), embed=embed)
        await client.send_message(discord.Object("454393067974426637"), embed=embed)
        await asyncio.sleep(60)


@client.event
async def on_ready():
    embed = discord.Embed(title="Updated!", color=0xBA00AA)
    await client.send_message(discord.Object("454027523270115358"), embed=embed)
    await client.send_message(discord.Object("454369180951511051"), embed=embed)
    await client.send_message(discord.Object("454393067974426637"), embed=embed)


@client.event
async def on_message(message):
    Time = datetime.datetime.now(pytz.timezone("US/Central"))  # Gets time when the message was sent
    if message.content.upper().startswith("$TIME"):
        hours = 19 - Time.hour - 1  # Defines Hour
        if hours < 0:
            hours = 19 + 4 - Time.hour % 19  # Redefines hour if hour is less than 0 (past 7pm cdt)
        minutes = 60 - Time.minute  # Defines minute
        embed = discord.Embed(title="Time", color=0x61ff69)
        if minutes == 60:
            embed.add_field(name="Time until next stream:", value="{} hour(s)".format(hours + 1))  # If no minutes only show hour
        elif hours == 0:
            embed.add_field(name="Time until next stream:", value="{} minute(s)!".format(minutes))  # If < 0 hours only show minute
        else:
            embed.add_field(name="Time until next stream:", value="{} hour(s)\n{} minute(s)!".format(hours, minutes))   # Show Normal Time
        await client.send_message(message.channel, embed=embed)

    elif message.author.id == "159985870458322944" and message.content.startswith("Hey @everyone!") or message.content.upper().startswith("$LIVE"):
        try:
            await client.delete_message(message)  # Detects message from Mee6 bot announcing live and replaces with StreamBot live announcement
        except discord.errors.Forbidden:
            await client.send_message(message.channel, "***Missing Permissions***")
        await client.send_message(message.channel, "@everyone")
        embed = discord.Embed(title="New Stream", color=0xff1ff3)
        embed.add_field(name="NinjaNube_Gaming is livestreaming!", value="Visit Twitch: http://twitch.tv/ninjanube_gaming\nVisit Mixer: http://mixer.com/NinjaNube_Gaming\nVisit YouTube: http://www.youtube.com/channel/UCS4NeZkk0B8gkK5uGKxIo2w")
        await client.send_message(message.channel, embed=embed)

    elif message.content.upper().startswith("$GIF"):
        args = message.content.split(" ")  # Makes parameter list
        args.append("end")
        embed = discord.Embed(title="GIF", color=0x059789)
        if args[1] == "list":  # if '$gif list' is entered
            embed.add_field(name="List of gif links that can be sent", value="\n".join(urls))  # Shows urls of all gifs
        else:
            embed.set_image(url=random.choice(urls))  # Displays gif
        await client.send_message(message.channel, embed=embed)

    elif message.content.upper().startswith("$HELP"):
        args = message.content.split(" ")  # Makes parameter list
        args.append("end")  # Adds 'end' to the end of the list to prevent errors
        embed = discord.Embed(title="Help", color=0x15f3ff)
        if args[1] == "commands":  # if '$help commands'
            embed.add_field(name="StreamBot Help commands", value="StreamBot Commands start with $.\nCommands are NOT case sensitive\nExisting commands are:\n\t$time\n\t$help (accepts command as parameter)\n\t$gif (accepts list as a parameter)")
        elif args[1] == "time" or args[1] == "$time":  # if '$help time' or '$help $time' entered
            embed.add_field(name="StreamBot Help time", value="Time shows you the time until the next livestream from NinjaNube Gaming.\nThis command is NOT case sensitive\nThis command has no parameters")
        elif args[1] == "gif" or args[1] == "$gif":  # if '$help gif' or '$help $gif' entered
            embed.add_field(name="StreamBot Help gif", value="Gif sends a random gif\nThis command is NOT case sensitive\nParameters: list\n\tList lists the links to the chosen gifs")
        else:  # if '$help' entered
            embed.add_field(name="StreamBot Help", value="StreamBot commands start with $ to avoid accidental calls from other bot.\nTry \'$help $time\' or \'$help commands\'")
        await client.send_message(message.channel, embed=embed)

    elif message.content.startswith("$"):
        embed = discord.Embed(title="ERROR", color=0xff4444)  # ff4444
        embed.add_field(name="That command doesn\'t exist", value="Use $help for help")
        await client.send_message(message.channel, embed=embed)

    else:
        contents = message.content.split(" ")
        for word in contents:
            if word.upper() in filter:
                try:
                    await client.delete_message(message)  # Deletes message if it contains a banned word
                except discord.errors.Forbidden:  # Not enough permissions
                    await client.send_message(message.channel, "***Missing Permissions***")
                embed = discord.Embed(title="Watch it!", color=0x000000)  # 000000
                embed.add_field(name="That word has been blacklisted", value="Common swear words or racial slurs have been banned")
                await client.send_message(message.channel, embed=embed)

Bot.loop.create_task()
client.run(str(os.environ.get('BOT_TOKEN')))
