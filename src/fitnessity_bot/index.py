"""
Alex Corpuz
8/18/2020

Notes: Some functions seem redundant. Goal is to minimize and reuse.
        Add function to reset hotstreak/scoreboard manually.
        Add function to allow ADMINS to set scores?
        Fix truncate in when updating data.
"""


import discord
import random
from collections import defaultdict


COMMAND_LIST = {"start": "Provides Link To Start Workout", "attendance": "Takes Attendance",
                "scoreboard": "Displays Current Scoreboard", "hotstreak": "Displays Current Hotstreaks",
                "help": "Shows Useful Commands", "report": "Shows Both Hotstreak and Scoreboard."}

CHEER = ["You're the man.", ":fire:", "Keep it up bud-man.", "Try a little harder next time.", "Killin' it.",
         "You definitely earned a beer.", "You rolled a nat 20 and tore that workout in half.", ":muscle:",
         ":clap:", ":punch:", ":star:", ":star2:"]


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
client = discord.Client()


@client.event
async def on_message(message):
    channels = ["workout"]
    if str(message.channel) in channels:
        await on_command(message)


async def on_command(message):
    str_command = message.content.lower()
    if str_command == "!fit":
        await message.channel.send("I am a Health/Fitness bot. Try '!fit help' to see what I can "
                                   "do so far. \nCheck us out at: https://Fitnessity.org")
    elif str_command == "!fit help":
        await help_command(message)
    elif str_command == "!fit start":
        await start_command(message)
    elif str_command == "!fit attendance":
        await attendance(message)
    elif str_command == "!fit scoreboard":
        await display_scores(read_scores(), message)
    elif str_command == "!fit hotstreak":
        await display_hot_streak(read_hot_streak(), message)
    elif str_command == "!fit report":
        await report(message)


async def attendance(message):
    voice_channel = client.get_channel(745179301107990581 and 735618391141777480)
    present_people = voice_channel.members
    names_list = [name.name for name in present_people if name.bot is False]
    for name in names_list:
        await message.channel.send(f"+1 for {name}.    {random.choice(CHEER)}")
    update_scores(names_list, read_scores())
    update_hot_streak(names_list, read_hot_streak())


def read_scores():
    scores_dict = defaultdict(int)
    with open("scoreboard.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        n, s = line.split()
        scores_dict[n] = int(s)
    return scores_dict


def update_scores(current_list, scores_dict):
    with open("scoreboard.txt", "w") as f:
        for people in current_list:
            if people not in scores_dict:
                scores_dict[people] = 1
            else:
                scores_dict[people] += 1
        f.truncate(0)  # Fix this in case of error. Don't want to lose data.
        for n, s in scores_dict.items():
            f.write(f"{n} {s}\n")


async def display_scores(scores_dict, message):
    scores_dict = sorted([(n, s) for (n, s) in scores_dict.items()], key=lambda x: x[1], reverse=True)
    scores_embed = discord.Embed(title="__Scoreboard__", inline=False)
    if len(scores_embed) == 0:
        scores_embed.add_field(value="Currently No One Has Worked Out.. :cry:", inline=False)
    else:
        for n, s in scores_dict:
            scores_embed.add_field(name=f"**{n}**: {s}\n", value=f"{(':trophy:' * s)}\n", inline=False)
    await message.channel.send(embed=scores_embed)


def read_hot_streak():
    hot_streak_dict = defaultdict(int)
    with open("hotstreak.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        n, s = line.split()
        hot_streak_dict[n] = int(s)
    return hot_streak_dict


def update_hot_streak(current_list, hot_streak_dict):
    with open("hotstreak.txt", "w") as f:
        for people in current_list:
            if people not in hot_streak_dict:
                hot_streak_dict[people] = 1
            else:
                hot_streak_dict[people] += 1
        for key in list(hot_streak_dict.keys()):
            if key not in current_list:
                del hot_streak_dict[key]
        f.truncate(0)  # Fix this in case of error. Don't want to lose data.
        for n, s in hot_streak_dict.items():
            f.write(f"{n} {s}\n")


async def display_hot_streak(hot_steak_dict, message):
    hot_steak_dict = sorted([(n, s) for (n, s) in hot_steak_dict.items()], key=lambda x: x[1], reverse=True)
    hot_streak_embed = discord.Embed(title="__Current Hot Streaks__", inline=False)
    if len(hot_steak_dict) == 0:
        hot_streak_embed.add_field(value="No Hot Streaks, Only Cold Streaks.. :cry:", inline=False)
    else:
        for n, s in hot_steak_dict:
            hot_streak_embed.add_field(name=f"{n} {s}\n", value=f"{(':fire:' * s)}\n", inline=False)
    await message.channel.send(embed=hot_streak_embed)


async def start_command(message):
    embed_website = discord.Embed(title="Fitnessity", description="**Click link above to start your workout!**",
                                  url="https://fitnessity.org")
    embed_website.set_thumbnail(url="https://www.fitnessity.org/logo.png")
    await message.channel.send(embed=embed_website)


async def help_command(message):
    embed_help = discord.Embed(title="Fitnessity Bot Commands", inline=True)
    for command, value in COMMAND_LIST.items():
        embed_help.add_field(name=f"!fit {command}", value=value, inline=False)
    await message.channel.send(embed=embed_help)


async def report(message):
    await display_scores(read_scores(), message)
    await display_hot_streak(read_hot_streak(), message)

def main():
    client.run(token)


