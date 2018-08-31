import discord
from discord.ext import commands


class kick():

    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        await ctx.send("Usage:")
        await ctx.send("`$kick @user`")
        print("$kick errored:")
        print(error)

    @commands.is_owner()
    @commands.command()
    async def kick(self, ctx, user: discord.Member):
        try:
            await ctx.guild.kick(user)
            await ctx.send("Kicked " + user)
        except discord.errors.Forbidden:
            await ctx.send("I don't have permission to do that :(")


def setup(bot):
    bot.add_cog(kick(bot))
