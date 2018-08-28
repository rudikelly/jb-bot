import discord
from discord.ext import commands

import time


class ping():

    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        await ctx.send("Usage:")
        await ctx.send("``$ping``")
        print("$ping errored:")
        print(error)

    @commands.command()
    async def ping(self, ctx):
        t1 = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        embed = discord.Embed(color=discord.Colour(0x96c8fa))
        embed.add_field(name="Pong! Response time: ", value="{}ms".format(round((t2 - t1) * 1000)), inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ping(bot))
