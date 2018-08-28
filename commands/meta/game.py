import discord
from discord.ext import commands


class game():

    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        await ctx.send("Usage:")
        await ctx.send("``$game``")
        print("$game errored:")
        print(error)

    @commands.command(aliases=['play'])
    async def game(self, ctx, *, game):
        await self.bot.change_presence(activity=discord.Game(name=game))
        await ctx.send("Set game to `" + game + "`")


def setup(bot):
    bot.add_cog(game(bot))
