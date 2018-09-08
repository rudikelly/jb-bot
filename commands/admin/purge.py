from discord.ext import commands


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


def setup(bot):
    bot.add_cog(purge(bot))
