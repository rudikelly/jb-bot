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

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, user: discord.Member):
        await ctx.guild.kick(user)
        await ctx.send("Kicked " + user)

    @kick.error
    async def kick_error_handler(self, ctx, error):
        if isinstance(error, discord.Forbidden):
            await ctx.send("I don't have permission to kick users!")
        else:
            await ctx.send("Usage:")
            await ctx.send("`$kick @user`")


def setup(bot):
    bot.add_cog(kick(bot))
