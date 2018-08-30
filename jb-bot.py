import discord
import asyncio
from discord.ext import commands
import config.loadconfig as cfg
import os
import logging


# Sets up logging
logging.basicConfig(level=logging.INFO)

# Initializes bot with basic info
bot = commands.Bot(command_prefix=commands.when_mentioned_or(cfg.prefixes), description="", case_insensitive=True, owner_id=cfg.my_id)
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
                logging.info("Successfully loaded " + extension)
                break
            except(ModuleNotFoundError):
                logging.warning("Failed to load " + extension)
                break


# Announces successful connection and basic data
@bot.event
async def on_ready():
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
        print("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("Successfully unloaded extension {}".format(extension))

# Runs bot
bot.run(cfg.token)
