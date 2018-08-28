import discord
import asyncio
from discord.ext import commands

import json
import sys

try:
    with open('config/config.json', 'r') as f:
        config = json.load(f)
        extensions = config["startup_extensions"]
        prefixes = config["prefixes"]
        default_game = config["default_game"]
        my_id = int(config["owner_id"])
except():
    print("Couldn't open config file. Exiting")
    sys.exit()

try:
    with open('config/keys.json', 'r') as f:
        keys = json.load(f)
        token = keys["token"]
except():
    print("Couldn't open keys file. Exiting")
    sys.exit()


def get_prefix(bot, message):
    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(command_prefix=get_prefix, description="", case_insensitive=True, owner_id=my_id)
bot.remove_command('help')

for x in extensions:
    bot.load_extension("commands." + x)


@bot.event
async def on_ready():
    print('Successfully connected!')
    print('As user - ' + bot.user.name)
    print('And ID - ' + str(bot.user.id))
    print('Owners id - ' + str(bot.owner_id))
    print('------\n')
    await bot.change_presence(activity=discord.Game(name=default_game))


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

bot.run(token)
