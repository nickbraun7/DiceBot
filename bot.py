#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, string

import discord, asyncio
from discord.ext import commands

import load, rp

DiscordToken = load.token()
OwnerID = 124686030631731203

#list of all possible role playing games
rp_games = [ 
    "DnD",
    "Shadow Run",
    "Tephra",
    ]

class guild_info():
    game = ""

guilds = {}

client = commands.Bot(command_prefix='~')
client.remove_command("help") #remove help to add custom help command

@client.event
async def on_ready():
    for guild in client.guilds:
        guilds[guild.id] = guild_info()

    await client.change_presence(activity=discord.Game("Haven't Rolled a Twenty Yet | ~help"))

    print("Dice Bot Operational")

@client.event
async def on_guild_join(guild):
    guilds[guild.id] = guild_info()

@client.event
async def on_guild_remove(guild):
    guilds.pop(guild.id)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(":stop_sign: **Command Not Found**")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":stop_sign: **Invalied Argument**")
    elif isinstance(error, commands.NotOwner):
        await ctx.send(":stop_sign: **You think you have the power!**")

    raise error

"""
Discord Command help screen
"""
@client.command()
async def help(ctx):
    embed = discord.Embed()

    embed.add_field(
        name="**~list**",
        value="list all the current role playing games supported",
        inline=False,
        )

    embed.add_field(
        name="**~set _game_**",
        value="set the current role playing of the server",
        inline=False,
        )

    embed.add_field(
        name="**~roll _#d#+/-#_**",
        value="takes in the argument (number of dice)d(value of dice)(+ or -)(modifier)",
        inline=False
        )

    embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed, delete_after=60)

"""
Discord Command to list all supported role
playing games.
"""
@client.command()
async def list(ctx):
    embed = discord.Embed()

    embed.add_field(
        name="**Supported Role Playing Games: **",
        value="\n".join(rp_games),
        inline=False
        )

    embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed, delete_after=60)

"""
Discord Command which sets the guild's current
game to the one specificed by a guild user.
"""
@client.command()
async def set(ctx, *args):
    guild = ctx.guild.id
    guild_info = guilds[guild]
    
    arg = " ".join(args)

    game = ""
    for rp_game in rp_games:
        if arg.lower() == rp_game.lower():
            game = rp_game

    if game:
        guild_info.game = game
        await ctx.send(":white_check_mark: **Game Set: **" + game)
    else:
        await ctx.send(":stop_sign: **Unknown Game: **" + game)

"""
Discord Command which takes the user's arguements,
checks to see if the string is valid, then calls
and prints the rolled value result.
"""
@client.command()
async def roll(ctx, arg):
    guild = ctx.guild.id
    guild_game = guilds[guild].game

    #regex string to detect dice rolls
    dice = re.search("(\d+)?d(\d+)([\+\-]\d+)?", arg, re.I)

    if guild_game:
        if dice:
            rp_roll = rp.roll(dice.group(1,2,3)) 
            await print_res(ctx, rp_roll.switch(guild_game))
        else:
            await ctx.send(":stop_sign: **Invalid Argument**")
    else:
        await ctx.send(":stop_sign: **Game Not Set**")

"""
Unpack the given res from the rp.roll class
function call and print the result to the user.
"""
async def print_res(ctx, res):
    total, mod, ls, crit = res

    embed = discord.Embed()

    embed.add_field(
        name = "**Total: **" + str(total) + crit,
        value = ":game_die: " + " + ".join(ls) + " " + mod,
        inline = False,
        )

    embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

client.run(DiscordToken)
