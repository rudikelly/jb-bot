import discord
import asyncio
from discord.ext import commands

import json

# get token and id from ext file for security
with open('config/config.json', 'r') as f:
    config = json.load(f)
    token = config["token"]
    my_id = int(config["owner_id"])


def get_prefix(bot, message):
    prefixes = ['$', '!?']
    return commands.when_mentioned_or(*prefixes)(bot, message)


embed_color = discord.Colour(0x96c8fa)
bot = commands.Bot(command_prefix=get_prefix, description="", case_insensitive=True, owner_id=my_id)

extensions = ["commands.jailbreak.canijb",
              "commands.jailbreak.canijb",
              "commands.jailbreak.profile",
              "commands.dev.docs",
              "commands.dev.header",
              "commands.dev.framework",
              "commands.fun.say",
              "commands.fun.xkcd",
              "commands.fun.zalgo",
              "commands.fun.ascii",
              "commands.meta.ping",
              "commands.meta.game"]

for x in extensions:
    bot.load_extension(x)

profile_enabled = True
canijb_enabled = True
docs_enabled = True
tweak_enabled = True
ascii_enabled = True
zalgo_enabled = True
header_enabled = True
framework_enabled = True
say_enabled = False
xkcd_enabled = True


@bot.event
async def on_ready():
    print('Successfully connected!')
    print('As user - ' + bot.user.name)
    print('And ID - ' + str(bot.user.id))
    print('Owners id - ' + str(bot.owner_id))
    print('------\n')
    await bot.change_presence(activity=discord.Game(name='$help'))


@bot.command(usage='[cmd]', aliases=['e'])
async def enable(ctx, cmd):

    # only lets bot owner run it
    if ctx.author.id == bot.owner_id:

        if(cmd == "jb" or cmd == "canijb"):
            global canijb_enabled
            canijb_enabled = True
        elif(cmd == "profile" or cmd == "tvos"):
            global profile_enabled
            profile_enabled = True
        elif(cmd == "doc" or cmd == "docs"):
            global docs_enabled
            docs_enabled = True
        elif(cmd == "tweak" or cmd == "info"):
            global tweak_enabled
            tweak_enabled = True
        elif(cmd == "ascii"):
            global ascii_enabled
            ascii_enabled = True
        elif(cmd == "header"):
            global header_enabled
            header_enabled = True
        elif(cmd == "framework"):
            global framework_enabled
            framework_enabled = True
        elif(cmd == "zalgo"):
            global zalgo_enabled
            zalgo_enabled = True
        elif(cmd == "say"):
            global say_enabled
            say_enabled = True
        else:
            await ctx.send("Command `" + cmd + "` not found")
            return
        await ctx.send("Enabled command `" + cmd + "`")

    else:
        await ctx.send("You don't have permission to do that")


@bot.command(usage='[cmd]', aliases=['d'])
async def disable(ctx, cmd):

    # only lets bot owner run it
    if ctx.author.id == bot.owner_id:

        if(cmd == "jb" or cmd == "canijb"):
            global canijb_enabled
            canijb_enabled = False
        elif(cmd == "profile" or cmd == "tvos"):
            global profile_enabled
            profile_enabled = False
        elif(cmd == "doc" or cmd == "docs"):
            global docs_enabled
            docs_enabled = False
        elif(cmd == "tweak" or cmd == "info"):
            global tweak_enabled
            tweak_enabled = False
        elif(cmd == "ascii"):
            global ascii_enabled
            ascii_enabled = False
        elif(cmd == "header"):
            global header_enabled
            header_enabled = False
        elif(cmd == "framework"):
            global framework_enabled
            framework_enabled = True
        elif(cmd == "zalgo"):
            global zalgo_enabled
            zalgo_enabled = False
        elif(cmd == "say"):
            global say_enabled
            say_enabled = False
        else:
            await ctx.send("Command `" + cmd + "` not found")
            return
        await ctx.send("Disabled command `" + cmd + "`")

    else:
        await ctx.send("You don't have permission to do that")


bot.remove_command('help')


@bot.group()
async def help(ctx):
    if ctx.invoked_subcommand is None:

        page = 1

        # embed containing help
        embed = discord.Embed(title="Jailbreak Bot Help | Page " + str(page), color=embed_color)
        embed.add_field(name="$canijb [ios]  or  $jb [ios]", value="Check if the given iOS is jailbreak-able", inline=False)
        embed.add_field(name="$profile  or  $tvos", value="Sends the tvOS 11 beta profile in the current channel, allowing you to 1-click install it", inline=True)
        embed.add_field(name="$tweak [tweak]  or  $theme [theme]", value="Provides information about and a download link for a specific tweak", inline=True)
        embed.add_field(name="$docs [object]  or  $doc [data type]  etc.", value="Provides a link to requested Apple Obj-C doc, as well as a short summary", inline=True)
        embed.add_field(name="$header [header] <ios> <framework>  or  $h [header] <framework> <ios>", value="Provides a link to requested header file", inline=True)
        embed.add_field(name="$framework [framework]  or  $f [framework]", value="Provides a link to requested framework", inline=True)
        embed.add_field(name="$xkcd random  or  $xkcd latest  or  $xkcd [number]", value="Sends the requested xkcd comic in the current channel. Defaults to random", inline=True)
        embed.set_footer(text="Type $help [command] to get detailed info about a certain command", icon_url=bot.user.avatar_url_as())
        msg = await ctx.send(embed=embed)

        await msg.add_reaction(u"\u2B05")
        await msg.add_reaction(u"\u27A1")


@help.command(aliases=['jb', 'canijailbreak'], name="canijb")
async def canijb_help(ctx):
    embed = discord.Embed(title="Jailbreak Bot Help", color=embed_color)
    embed.add_field(name="$canijb [ios]  or  $jb [ios]", value="Check if the given iOS is jailbreak-able. Works for every ios except 5, not sure . Sends name of the jailbreak tool and link to get it", inline=False)
    embed.add_field(name="Examples", value="$canijb 11.0\n$canijb ios 6.1.3\n$jb 7.1.2\n$jb ios 5.1", inline=False)
    await ctx.send(embed=embed)


@help.command(aliases=['tvos'], name="profile")
async def profile_help(ctx):
    embed = discord.Embed(title="Jailbreak Bot Help", color=embed_color)
    embed.add_field(name="$profile  or  $tvos", value="Sends the tvOS 11 beta profile in the current channel, allowing you to 1-click install it", inline=True)
    embed.add_field(name="Examples", value="$profile\n$tvos", inline=False)
    await ctx.send(embed=embed)


@help.command(aliases=['theme'], name="tweak")
async def tweak_help(ctx):
    embed = discord.Embed(title="Jailbreak Bot Help", color=embed_color)
    embed.add_field(name="$tweak [tweak]  or  $theme [theme]", value="Provides information about and a download link for a specific tweak. Currently only works for defualt repos", inline=True)
    embed.add_field(name="Examples", value="$tweak icleaner\n$tweak classicfolders 2\n$theme indigo", inline=False)
    await ctx.send(embed=embed)


@help.command(aliases=['doc'], name="docs")
async def docs_help(ctx):
    embed = discord.Embed(title="Jailbreak Bot Help", color=embed_color)
    embed.add_field(name="$docs [object]  or  $doc [data type]  etc.", value="Provides a link to requested Apple Obj-C doc, as well as a short summary. Only frameworks currently supported are: Objective-C, UIKit, WebKit, Foundation, CoreGraphics, CoreData, Kernel, CoreServices", inline=True)
    embed.add_field(name="Examples", value="$docs NSObject\n$doc UIViewController\n$docs CGFloat", inline=False)
    await ctx.send(embed=embed)


@help.command(aliases=['h'], name="header")
async def header_help(ctx):
    embed = discord.Embed(title="Jailbreak Bot Help", color=embed_color)
    embed.add_field(name="$header [header] <ios> <framework>  or  $h [header] <framework> <ios>", value="Provides a link to requested header file. Case Sensitive. Generates a link to developer.limneos.net. Only frameworks currently supported are: SpringBoard, UIKit, WebKit, Foundation, CoreData, CoreServices. However it will check any frameworks provided explicitly", inline=True)
    embed.add_field(name="Examples", value="$header SBAlertView\n$h SBPowerDownAlertView 10.2\n$h CXStartCallAction.h CallKit 10.1.1", inline=False)
    await ctx.send(embed=embed)


@help.command(aliases=['f'], name="framework")
async def framework_help(ctx):
    embed = discord.Embed(title="Jailbreak Bot Help", color=embed_color)
    embed.add_field(name="$framework [framework]  or  $f [framework]", value="Provides a link to requested framework on developer.limneos.net. Case Sensitive.", inline=True)
    embed.add_field(name="Examples", value="$framework SpringBoard\n$f UIKit\n$f Foundation", inline=False)
    await ctx.send(embed=embed)


@help.command(name="xkcd")
async def xkcd_help(ctx):
    embed = discord.Embed(title="Jailbreak Bot Help", color=embed_color)
    embed.add_field(name="$xkcd random  or  $xkcd latest  or  $xkcd [number]", value="Sends the requested xkcd comic in the current channel. Defaults to random", inline=True)
    embed.add_field(name="Examples", value="$xkcd latest\n$xkcd 678\n$xkcd", inline=False)
    await ctx.send(embed=embed)


bot.run(token)
