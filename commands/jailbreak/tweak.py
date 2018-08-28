import discord
from discord.ext import commands

from bs4 import BeautifulSoup
import json
import aiohttp


class tweak():

    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        await ctx.send("Usage:")
        await ctx.send("``$tweak [tweak]``")
        print("$tweak errored:")
        print(error)

    @commands.command(aliases=['tweakinfo', 'theme'], usage='[tweak]')
    async def tweak(self, ctx, tweak: str, tweak2: str = '', tweak3: str = '', tweak4: str = ''):

        await ctx.trigger_typing()

        # allows for multi word input
        tweak = tweak + tweak2 + tweak3 + tweak4

        # logs the command issued
        print("------\n" + ctx.message.content)

        # grabs data about tweak from sauriks api
        async with aiohttp.ClientSession() as session:
            async with session.get("https://cydia.saurik.com/api/macciti?query=" + tweak.replace(' ', '').lower().strip()) as r:
                t = await r.text()
                data = json.loads(t)

                # checks if the tweak matches the api's first response
                for x in range(len(data["results"])):
                    rtweak = data["results"][x]
                    if (rtweak["display"].replace(' ', '').lower().strip() == tweak.replace(' ', '').lower().strip()):

                        # gathers basic info
                        tweakname = rtweak["display"]
                        bundleid = rtweak["name"]
                        section = rtweak["section"]
                        summary = rtweak["summary"]
                        # version = rtweak["version"]
                        url = "http://cydia.saurik.com/package/" + bundleid
                        icon_url = "http://cydia.saurik.com/icon@2x/" + bundleid + ".png"

                        # gets package price
                        async with session.get("http://cydia.saurik.com/api/ibbignerd?query=" + bundleid) as r:
                            gr = await r.text()
                            pr = json.loads(gr)
                            if pr is None:
                                price = "Free"
                            else:
                                price = pr["msrp"]

                        # grabs the repo tweak is hosted on (stolen from https://github.com/hizinfiz/TweakInfoBot/)
                        async with session.get(url) as r:
                            html = await r.text()
                            soup = BeautifulSoup(html, "html.parser")
                            repo = soup.find('span', {'class': 'source-name'}).contents[0]
                            if repo == 'ModMyi.com':
                                            repo = 'ModMyi'

                        # constructs nice embed
                        embed = discord.Embed(title=tweakname, url=url, color=discord.Colour(0x96c8fa))
                        embed.set_footer(text=tweakname, icon_url=icon_url)
                        embed.add_field(name="Section", value=section, inline=True)
                        embed.add_field(name="Repo", value=repo, inline=True)
                        # embed.add_field(name="Version", value=version, inline=True)
                        embed.add_field(name="Price", value=price, inline=True)
                        embed.add_field(name="Summary", value=summary, inline=False)
                        await ctx.send(embed=embed)
                        print("Successful")
                        return

                # if command fails
                await ctx.send("Couldn't find info for tweak " + tweak)
                print("Failed")


def setup(bot):
    bot.add_cog(tweak(bot))
