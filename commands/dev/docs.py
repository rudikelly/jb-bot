import discord
from discord.ext import commands

import aiohttp
from bs4 import BeautifulSoup


class docs():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['doc'])
    async def docs(self, ctx, doc: str = '', framework: str = ''):

        await ctx.trigger_typing()

        done = False

        if framework != '':
            url = "https://developer.apple.com/documentation/" + framework + "/" + doc + "?language=objc"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    html = await r.text()
                    soup = BeautifulSoup(html, "html.parser")

                    try:
                        summary = soup.find('p').contents[0]
                        done = True
                    except AttributeError:
                        done = False

        else:

            # generates url to relevent doc and retrieves summary
            pages = ["objectivec", "uikit", "webkit", "foundation", "coregraphics", "coredata", "kernel", "coreservices"]
            for x in pages:
                url = "https://developer.apple.com/documentation/" + x + "/" + doc + "?language=objc"

                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as r:
                        html = await r.text()
                        soup = BeautifulSoup(html, "html.parser")

                        try:
                            summary = soup.find('p').contents[0]
                            done = True
                            break
                        except AttributeError:
                            continue

            if done:

                # goes to main objc doc page if nothing specified
                if(doc == ''):
                    doc = "Objective-C"

                # constructs embed containing url and summary
                embed = discord.Embed(title="Docs for " + doc, url=url, color=discord.Colour(0x96c8fa))
                embed.add_field(name="Summary", value=summary, inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Unable to find doc for " + doc)


def setup(bot):
    bot.add_cog(docs(bot))
