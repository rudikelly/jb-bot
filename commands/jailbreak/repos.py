import discord
from discord.ext import commands
import json
import config.loadconfig as cfg


class repos():

    def __init__(self, bot):
        self.bot = bot

    # async def __error(self, ctx, error):
    #     await ctx.send("Usage:")
    #     await ctx.send("``$repos``")
    #     print("$repos errored:")
    #     print(error)

    @commands.command()
    async def repos(self, ctx):
        builtin_repo_list = ""
        for repo in cfg.repo_list:
            builtin_repo_list += repo + "\n"
        server_repo_list = ""
        with open("config/servers.json", 'r+') as f:
            servers = json.load(f)["servers"]
            for repo in servers[str(ctx.message.guild.id)]["repo_list"]:
                server_repo_list += repo + "\n"
        if server_repo_list is "":
            server_repo_list = "None"
        await ctx.send("Built-in repos: ```" + builtin_repo_list + "``` Server repos: ```" + server_repo_list + "```")

    @commands.command()
    async def repo():
        pass


def setup(bot):
    bot.add_cog(repos(bot))
