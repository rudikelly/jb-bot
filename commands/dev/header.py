import discord
from discord.ext import commands

import aiohttp
from bs4 import BeautifulSoup


class header():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage='[object]', aliases=['h', 'headers'])
    async def header(self, ctx, text: str, uinput0: str = '', uinput1: str = ''):

        await ctx.trigger_typing()

        text = text.replace(' ', '').strip()

        ios = "11.1.2"

        # appends .h if it isnt there already
        if not text[-2:] == ".h":
            text = text + ".h"

        framework = ""

        if not uinput0 == '':
            try:
                int(uinput0.replace('.', ''))
                ios = str(uinput0)
            except ValueError:
                framework = str(uinput0)

            if not uinput1 == '':
                try:
                    int(uinput1.replace('.', ''))
                    ios = str(uinput1)
                except ValueError:
                    framework = str(uinput1)

        if not framework == "" and not framework[-10:] == ".framework":
            framework = framework + ".framework"

        pages = ["SpringBoard", "UIKit.framework", "WebKit.framework", "Foundation.framework", "CoreData.framework", "CoreServices.framework"]
        for x in pages:

            if not framework == "":

                url = "http://developer.limneos.net/index.php?ios=" + ios + "&framework=" + framework + "&header=" + text

            else:
                url = "http://developer.limneos.net/index.php?ios=" + ios + "&framework=" + x + "&header=" + text

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    html = await r.text()
                    soup = BeautifulSoup(html, "html.parser")
                    if str(soup).strip() == "Access error.":
                        await ctx.send("Header " + text + " not found for iOS " + ios)
                        return

                    title = soup.title.contents[0]

                    try:
                        if(soup.findAll('div')[7].findAll('br')[1].contents[0].strip() == "Error resolving file."):
                            continue

                        else:
                            embed = discord.Embed(title=title, url=url, color=discord.Colour(0x96c8fa))
                            await ctx.send(embed=embed)
                            return

                    except IndexError:
                        if soup.findAll('div')[6].findAll('br')[0].findAll('br')[0].contents[0].strip() == "Error resolving file.":
                            continue
                        else:
                            embed = discord.Embed(title=title, url=url, color=discord.Colour(0x96c8fa))
                            await ctx.send(embed=embed)
                            return

                await ctx.send("Couldn't find header for " + text)


def setup(bot):
    bot.add_cog(header(bot))
