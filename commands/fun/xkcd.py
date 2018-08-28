import discord
from discord.ext import commands

import aiohttp
import json
import random


class xkcd():

    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        await ctx.send("Usage:")
        await ctx.send("``$xkcd [number]``")
        print("$xkcd errored:")
        print(error)

    @commands.command()
    async def xkcd(self, ctx, arg: str = ''):

        async with aiohttp.ClientSession() as session:
            async with session.get("https://xkcd.com/info.0.json") as r:
                latest = json.loads(await r.text())
                total = latest["num"]

            try:
                num = int(arg)
            except(ValueError):
                if arg.lower() == "random" or arg == '':
                    num = random.randint(1, total)
                elif arg.lower() == "latest":
                    num = total
                else:
                    await ctx.send("`xkcd`: Unknown option `" + arg + "`")
                    return

            async with session.get("https://xkcd.com/" + str(num) + "/info.0.json") as r:
                comic = json.loads(await r.text())
                title = comic["safe_title"]
                link = comic["img"]
            embed = discord.Embed(title="xkcd " + str(num) + ": " + title, url="https://xkcd.com/" + str(num), color=discord.Colour(0x96c8fa))
            embed.set_image(url=link)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(xkcd(bot))
