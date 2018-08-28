import discord
from discord.ext import commands


class __command__():

    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        await ctx.send("Usage:")
        await ctx.send("``$__command__``")
        print("$__command__ errored:")
        print(error)

    @commands.command()
    async def __command__():
        pass


def setup(bot):
    bot.add_cog(__command__(bot))
