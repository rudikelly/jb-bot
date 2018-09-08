import discord
from discord.ext import commands


class tweak():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['tvos'])
    async def profile(self, ctx):
            await ctx.send(ctx.message.author.mention + " Here you go:", file=discord.File('profile.mobileconfig'))

    @profile.error
    async def profile_error_handler(self, ctx, error):
        error = getattr(error, 'original', error)
        if isinstance(error, discord.Forbidden):
            await ctx.send("I don't have permission to send files here!")


def setup(bot):
    bot.add_cog(tweak(bot))
