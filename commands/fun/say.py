from discord.ext import commands


class say():

    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        await ctx.send("Usage:")
        await ctx.send("``$say [text]``")
        print("$say errored:")
        print(error)

    @commands.command(aliases=['saythis', 's'])
    async def say(self, ctx, *, words):
        await ctx.send(words)


def setup(bot):
    bot.add_cog(say(bot))
