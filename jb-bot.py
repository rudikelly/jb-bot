import discord
import asyncio
from discord.ext import commands
import config.loadconfig as cfg
import os
import sys
import logging as log
import json


# Sets up logging
log.basicConfig(level=log.INFO)

# Initializes bot with basic info
bot = commands.Bot(command_prefix=commands.when_mentioned_or(*cfg.prefixes), description="", case_insensitive=True, owner_id=cfg.my_id)
bot.remove_command('help')

# Gets list of file in 'commands' dir, stores in 'extensions'
categories = os.listdir("commands")
extensions = []
for category in categories:
    files = os.listdir("commands/" + category)
    for file in files:
        extensions.append("commands." + category + "." + file[:-3])

# Loads all extensions except those explicitly ignored
for extension in extensions:
    for ignore in cfg.ignored:
        if "commands." + extension.lower() != ignore:
            try:
                bot.load_extension(extension)
                log.info("Successfully loaded " + extension)
                break
            except ModuleNotFoundError:
                log.warning("Failed to load " + extension)
                break


# Announces successful connection and basic data
@bot.event
async def on_ready():

    # adds missing servers to servers.json
    try:
        with open("config/servers.json", 'r+') as f:
            servers = json.load(f)
            for guild in bot.guilds:
                if str(guild.id) in servers["servers"].keys():
                    log.info("Server " + guild.name + " already configured")
                else:
                    servers["servers"][guild.id] = {}
                    log.info("Configures server " + guild.name)
            f.seek(0)
            json.dump(servers, f, indent=4)
    except FileNotFoundError:
        log.fatal("Servers.json file not found. Exiting")
        sys.exit()

    os.system('clear')
    print('Successfully connected!')
    print('As user - ' + bot.user.name)
    print('And ID - ' + str(bot.user.id))
    print('Owners id - ' + str(bot.owner_id))
    print('------\n')
    await bot.change_presence(activity=discord.Game(name=cfg.game))


# Command to load extra extensions
@commands.is_owner()
@bot.command(aliases=['e', 'enable'])
async def load(ctx, extension: str):
    extension = extension.lower().strip()
    try:
        bot.load_extension("commands." + extension)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("Successfully loaded extension {}".format(extension))


# Command to unload extensions
@commands.is_owner()
@bot.command(aliases=['d', 'disable'])
async def unload(ctx, extension: str):
    extension = extension.lower().strip()
    try:
        bot.unload_extension("commands." + extension)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("Successfully unloaded extension {}".format(extension))

# Runs bot
bot.run(cfg.token)
