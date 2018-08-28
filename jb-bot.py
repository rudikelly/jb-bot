import discord
import asyncio
from discord.ext import commands
import config.loadconfig as cfg


# Initializes bot with basic info
bot = commands.Bot(command_prefix=commands.when_mentioned_or(*cfg.prefixes), description="", case_insensitive=True, owner_id=cfg.my_id)
bot.remove_command('help')


# Initializes commands
for x in cfg.extensions:
    bot.load_extension("commands." + x)


# Announces successful connection and basic data
@bot.event
async def on_ready():
    print('Successfully connected!')
    print('As user - ' + bot.user.name)
    print('And ID - ' + str(bot.user.id))
    print('Owners id - ' + str(bot.owner_id))
    print('------\n')
    await bot.change_presence(activity=discord.Game(name=cfg.game))


# Load extra extensions
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


# Unload extensions
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
