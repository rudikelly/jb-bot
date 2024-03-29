import discord
from discord.ext import commands

import aiohttp
from bs4 import BeautifulSoup


class framework():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['f'])
    async def framework(self, ctx, text: str):

        await ctx.trigger_typing()

        text = text.replace(' ', '').strip()

        # logs command issued
        ios = "11.1.2"

        if not text == "SpringBoard" and not text[:-10] == ".framework":
            text_frm = text + ".framework"
        else:
            text_frm = text

        url = "http://developer.limneos.net/index.php?ios=" + ios + "&framework=" + text_frm

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                html = await r.text()
                soup = BeautifulSoup(html, "html.parser")

                title = soup.title.contents[0]

                try:
                    if(soup.findAll('div')[7].findAll('pre')[0].contents[0].strip() == "Given Framework doesn't exist in my database, sorry."):

                        await ctx.send("Couldn't find framework " + text)
                    else:
                        embed = discord.Embed(title=title, url=url, color=discord.Colour(0x96c8fa))
                        await ctx.send(embed=embed)
                        return

                except IndexError:
                    embed = discord.Embed(title=title, url=url, color=discord.Colour(0x96c8fa))
                    await ctx.send(embed=embed)
                    return


def setup(bot):
    bot.add_cog(framework(bot))
