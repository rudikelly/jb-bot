from discord.ext import commands


class say():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['saythis', 's'])
    async def say(self, ctx, *, words):
        await ctx.send(words)


def setup(bot):
    bot.add_cog(say(bot))
