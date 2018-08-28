import discord
from discord.ext import commands


class tweak():

    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        await ctx.send("Usage:")
        await ctx.send("``$profile``")
        print("$profile errored:")
        print(error)

    @commands.command(aliases=['tvos'])
    async def profile(self, ctx):
            await ctx.send(ctx.message.author.mention + " Here you go:", file=discord.File('profile.mobileconfig'))


def setup(bot):
    bot.add_cog(tweak(bot))
