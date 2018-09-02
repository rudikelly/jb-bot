import discord
from discord.ext import commands

from bs4 import BeautifulSoup
import json
import aiohttp
import config.loadconfig as cfg
import logging as log

repo_list = []
for repo in cfg.repo_list:
    repo_list.append(repo)
try:
    with open("config/servers.json", 'r') as f:
        server_repo_list = json.load(f)["servers"]

except FileNotFoundError:
    log.error("server.json not found")


class tweak():

    def __init__(self, bot):
        self.bot = bot

    # async def __error(self, ctx, error):
    #     await ctx.send("Usage:")
    #     await ctx.send("``$tweak [tweak]``")
    #     print("$tweak errored:")
    #     print(error)

    @commands.command(aliases=['tweakinfo', 'theme'], usage='[tweak]')
    async def tweak(self, ctx, *, query: str):

        tweak = query.replace(' ', '').lower().strip()

        # grabs data about tweak from sauriks api
        async with aiohttp.ClientSession() as session:
            async with session.get("https://cydia.saurik.com/api/macciti?query=" + tweak) as r:
                t = await r.text()
                data = json.loads(t)

                # checks if the tweak matches the api's first response
                for x in range(len(data["results"])):
                    rtweak = data["results"][x]
                    if (rtweak["display"].replace(' ', '').lower().strip() == tweak):

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
                        return

            for repo in server_repo_list[str(ctx.message.guild.id)]["repo_list"]:
                repo_list.append(repo)

            exact_match = False

            # if tweak isnt found on a default repo, search non-default ones
            for repo in repo_list:
                # searches as though the query is a tweak name
                async with session.get("https://cydia.s0n1c.org/cydia/" + "?q=" + tweak + "&url=" + repo) as resp:
                    if resp.status == 200:
                        data = json.loads(await resp.text())
                    else:
                        await ctx.send("Error contacting cydia :(")
                        log.error("Got non-200 status code from API")
                if data["status"]:
                    for x in range(len(data["results"])):
                        result = data["results"][str(list(data["results"].keys())[x])]
                        if result["name"].strip().lower() == tweak:
                            tweak_data = result
                            exact_match = True
                            break
                    if not exact_match:
                        tweak_data = data["results"][str(list(data["results"].keys())[x])]
                    async with session.get("https://cydia.s0n1c.org/cydia/" + "?url=" + repo) as resp:
                        repo_info = json.loads(await resp.text())["info"]
                        repo_icon_url = repo_info["icon"]
                        repo_name = repo_info["Label"]

                    # constructs nice embed
                    embed = discord.Embed(title=tweak_data["name"], url=tweak_data["depict"], color=discord.Colour(0x96c8fa))
                    embed.set_footer(text=tweak_data["name"] + " - " + repo_name, icon_url=repo_icon_url)
                    embed.add_field(name="Section", value=tweak_data["section"], inline=True)
                    embed.add_field(name="Repo", value=repo, inline=True)
                    if not tweak_data["author"] is "":
                        embed.add_field(name="Author", value=tweak_data["author"], inline=True)
                    embed.add_field(name="Summary", value=tweak_data["desc"], inline=False)
                    if not exact_match:
                        await ctx.send("Couldn't find an exact match :(. This might be it")
                    await ctx.send(embed=embed)
                    return

            else:
                await ctx.send("Couldn't find info for tweak " + query)


def setup(bot):
    bot.add_cog(tweak(bot))
