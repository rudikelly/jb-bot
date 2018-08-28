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
bot.remove_command('help')

extensions = ["jailbreak.canijb",
              "jailbreak.canijb",
              "jailbreak.profile",
              "dev.docs",
              "dev.header",
              "dev.framework",
              "fun.say",
              "fun.xkcd",
              "fun.zalgo",
              "fun.ascii",
              "meta.ping",
              "meta.game",
              "meta.help"]

for x in extensions:
    bot.load_extension("commands." + x)


@bot.event
async def on_ready():
    print('Successfully connected!')
    print('As user - ' + bot.user.name)
    print('And ID - ' + str(bot.user.id))
    print('Owners id - ' + str(bot.owner_id))
    print('------\n')
    await bot.change_presence(activity=discord.Game(name='$help'))






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
