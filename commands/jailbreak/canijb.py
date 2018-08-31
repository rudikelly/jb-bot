import discord
from discord.ext import commands

from packaging import version
import json
import aiohttp


class canijb():

    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        await ctx.send("Usage:")
        await ctx.send("``$canijb [ios]``")
        print("$canijb errored:")
        print(error)

    @commands.command(aliases=['canijailbreak', 'jb'], usage='[ios]')
    async def canijb(self, ctx, ios: str, ios2: str = ""):
        print(self)
        await ctx.trigger_typing()

        if (ios.lower() == "ios"):
            ios = ios2

        # fetches json api, loads into list
        async with aiohttp.ClientSession() as session:
            async with session.get("http://canijailbreak.com/jailbreaks.json") as r:
                t = await r.text()
                data = json.loads(t)
                jailbreaks = data["jailbreaks"]

                jailbroken = False
                done = False

                for x in range(len(jailbreaks)):

                    # iterates through the list until it finds data for matching version
                    if (version.parse(str(jailbreaks[x]["ios"]["start"])) <= version.parse(ios)) and (version.parse(str(jailbreaks[x]["ios"]["end"])) >= version.parse(ios)):

                        # checks if it can be jailbroken
                        jailbroken = jailbreaks[x]["jailbroken"]
                        if (jailbroken):
                            done = True

                            # grabs name of the tool and the url from the api
                            url = jailbreaks[x]["url"]
                            name = jailbreaks[x]["name"]

                            # helpful message containing tool name and url
                            embed = discord.Embed(title="iOS " + ios + " can be jailbroken!", description="", color=discord.Colour(0x96c8fa), url="https://canijailbreak.com/")
                            embed.add_field(name="Use the tool " + name + " which you can get at:", value=url, inline=False)
                            # embed.set_footer(icon_url=ctx.message.author.avatar_url_as(), text="Requested by " + str(ctx.message.author))
                            await ctx.send(embed=embed)
                            break
                        else:
                            await ctx.send("iOS " + ios + " can't be jailbroken!")
                            done = True
                            break
                    else:
                        continue
                if (not jailbroken and not done):
                    await ctx.send("Couldn't find data for iOS " + ios)


def setup(bot):
    bot.add_cog(canijb(bot))
