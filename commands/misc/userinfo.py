import discord
from discord.ext import commands


class userinfo():

    def __init__(self, bot):
        self.bot = bot

    # async def __error(self, ctx, error):
    #     await ctx.send("Usage:")
    #     await ctx.send("``$userinfo @user``")
    #     print("$userinfo errored:")
    #     print(error)

    @commands.command()
    async def userinfo(self, ctx, user: discord.Member = None):

        # If user isnt passed, gets info for the message author
        if user is None:
            user = ctx.message.author

        if user.id == self.bot.user.id:
            return await ctx.send("Hey that's me!")

        if user.bot:
            return await ctx.send("That user is a bot!")

        # Grabs all user roles
        roles = ""
        role_count = 0
        for role in user.roles[1:]:
            roles += role.mention + "\n"
            role_count += 1
        if roles == "":
            roles = "None"

        # Constructs embed containing info
        embed = discord.Embed(color=discord.Colour(0x96c8fa))
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Name", value=user.name, inline=True)
        embed.add_field(name="Nick", value=user.nick, inline=True)
        embed.add_field(name="Roles (" + str(role_count) + ")", value=roles, inline=False)
        embed.set_author(name=user.name + "#" + user.discriminator, icon_url=user.avatar_url)
        embed.set_footer(text="ID:" + str(user.id))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(userinfo(bot))
