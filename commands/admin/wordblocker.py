import logging
import config.loadconfig as cfg


class wordblocker():

    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        await ctx.send("Usage:")
        await ctx.send("``$wordblocker``")
        print("$wordblocker errored:")
        logging.error(error)

    async def on_message(self, message):
        for word in cfg.banned_words:
            if word in message.content:
                await message.delete()
                await message.channel.send("Hey " + message.author.mention + " watch your language!")


def setup(bot):
    bot.add_cog(wordblocker(bot))
