from discord.ext import commands
from zalgo_text import zalgo as z


class zalgo():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['zalgothis', 'z'])
    async def zalgo(self, ctx, *, words):
        zalgod = ""
        for x in words:
            zalgod = zalgod + (z.zalgo().zalgofy(x))
        await ctx.send(zalgod)


def setup(bot):
    bot.add_cog(zalgo(bot))
