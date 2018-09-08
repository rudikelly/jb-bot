from discord.ext import commands
import discord


class purge():

    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        await ctx.send("Usage:")
        await ctx.send("``$purge``")
        print("$purge errored:")
        print(error)

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def purge(self, ctx, msgs: int):
        await ctx.message.delete()

        if msgs < 10000:
            async for message in ctx.message.channel.history(limit=msgs):
                await message.delete()
        else:
            await ctx.send('Too many messages to delete. Enter a number < 10000')

    @purge.error
    async def purge_error_handler(self, ctx, error):
        if isinstance(error, discord.Forbidden):
            await ctx.send("I don't have permission to do that!")
        else:
            await ctx.send("Usage:")
            await ctx.send("`$purge [number of messages]`")


def setup(bot):
    bot.add_cog(purge(bot))
