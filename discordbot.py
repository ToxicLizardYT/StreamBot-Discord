from discord.ext.commands import Bot
from datetime import datetime
from random import randint
import discord
import pytz
import os

Client = discord.Client()
client = Bot(command_prefix="$")

RapGod_id = "324332386219327488"
filter = ['NIGGER', 'FAGGOT', 'GAY', 'FUCK', 'SHIT', 'DAMN', 'NIGGERFAGGOT', 'GODDAMN']


@client.event
async def on_ready():
    embed = discord.Embed(title="Updated!", color=0xBA00AA)
    await client.send_message(discord.Object("454027523270115358"), embed=embed)
    await client.send_message(discord.Object("454369180951511051"), embed=embed)
    await client.send_message(discord.Object("454393067974426637"), embed=embed)


@client.event
async def on_message(message):
    if message.content.upper().startswith("$TIME"):
        time = datetime.now(pytz.timezone("US/Central"))  # Gets time when the message was sent
        hours = 19 - time.hour - 1  # Defines Hour
        if hours < 0:
            hours = 19 + 4 - time.hour % 19  # Redefines hour if hour is less than 0 (past 7pm cdt)
        minutes = 60 - time.minute  # Defines minute
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

    elif message.content.upper().startswith("$HELP"):
        args = message.content.split(" ")  # Makes parameter list
        args.append("end")  # Adds 'end' to the end of the list to prevent errors
        embed = discord.Embed(title="Help", color=0x15f3ff)
        if args[1] == "commands":
            embed.add_field(name="StreamBot help commands", value="StreamBot Commands start with $.\nCommands are NOT case sensitive\nExisting commands are:\n\t$time\n\t$help (accepts parameter)")
        elif args[1] == "time" or args[1] == "$time":
            embed.add_field(name="StreamBot help time", value="Time shows you the time until the next livestream from NinjaNube Gaming.\nThis command is NOT case sensitive\nThis command has no parameters")
        else:
            embed.add_field(name="StreamBot help", value="StreamBot commands start with $ to avoid accidental calls from other bot.\nWe don\'t use spaces or parameters in any command other than this one.\nTry \'$help $time\' or \'$help commands\'")
        await client.send_message(message.channel, embed=embed)

    elif message.content.upper().startswith("$GIF"):
        gifNum = len([name for name in os.listdir("./gifs") if os.path.isfile(os.path.join("./gifs", name))])
        gif = randint(1, gifNum)
        embed = discord.Embed(title="GIF", color=0x749dee)
        embed.image().url = "./gifs/" + str(gif) + ".gif"
        #embed.add_field(name="Here\'s a random gif!", value="You got gif " + str(gif) + "/" + str(gifNum))
        embed.set_image(url=str(embed.image.url))
        await client.send_message(message.channel, embed=embed)

    elif message.content.upper().startswith("$LIST"):
        embed = discord.Embed(title="FILTER", color=0x8b8fa1)  # 8b8fa1
        embed.add_field(name="Words you can\'t say", value="\n".join(filter[0:]).lower())
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
                    await client.delete_message(message)  # Detects message from Mee6 bot announcing live and replaces with StreamBot live announcement
                except discord.errors.Forbidden:
                    await client.send_message(message.channel, "***Missing Permissions***")
                embed = discord.Embed(title="Watch it!", color=0x000000)  # 000000
                embed.add_field(name="That word has been blacklisted", value="Use $list for the list of blacklisted words")
                await client.send_message(message.channel, embed=embed)

client.run(str(os.environ.get('BOT_TOKEN')))
