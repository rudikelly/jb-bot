import discord
from discord.ext import commands


class ban():

    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        await ctx.send("Usage:")
        await ctx.send("`$ban @user`")
        print("$ban errored:")
        print(error)

    @commands.is_owner()
    @commands.command()
    async def ban(self, ctx, user: discord.Member):
        try:
            await ctx.guild.ban(user)
            await ctx.send("Banned " + user)
        except discord.errors.Forbidden:
            await ctx.send("I don't have permission to do that :(")


def setup(bot):
    bot.add_cog(ban(bot))
