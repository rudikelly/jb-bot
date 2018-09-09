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

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, user: discord.Member):
        await ctx.guild.ban(user)
        await ctx.send("Banned " + user)

    @ban.error
    async def ban_error_handler(self, ctx, error):
        if isinstance(error, discord.Forbidden):
            await ctx.send("I don't have permission to ban users!")
        else:
            await ctx.send("Usage:")
            await ctx.send("`$ban @user`")


def setup(bot):
    bot.add_cog(ban(bot))
