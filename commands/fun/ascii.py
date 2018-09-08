from discord.ext import commands
from pyfiglet import Figlet


class ascii():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['asciithis'])
    async def ascii(self, ctx, *, words):
        f = Figlet()
        asciid = f.renderText(words)
        await ctx.send("```" + asciid + "```")


def setup(bot):
    bot.add_cog(ascii(bot))
