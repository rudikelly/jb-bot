import discord
from discord.ext import commands
import json
import aiohttp
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
            builtin_repo_list += repo + " \n"
        server_repo_list = ""
        with open("config/servers.json", 'r+') as f:
            servers = json.load(f)["servers"]
            for repo in servers[str(ctx.message.guild.id)]["repo_list"]:
                server_repo_list += repo + "\n"
        if server_repo_list is "":
            server_repo_list = "None"
        embed = discord.Embed(title="Jailbreak Bot Repos", color=discord.Colour(0x96c8fa))
        embed.add_field(name="Built-in Repos:", value=builtin_repo_list, inline=True)
        embed.add_field(name="Server Repos:", value=server_repo_list, inline=True)
        await ctx.send(embed=embed)

    @commands.group()
    async def repo(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Usage: `repo add [repo]`  or  `repo remove [repo]`")

    @repo.command()
    async def add(self, ctx, repo_to_add):
        with open("config/servers.json", 'r+') as f:
            servers = json.load(f)
            for repo in servers["servers"][str(ctx.message.guild.id)]["repo_list"]:
                if repo_to_add == repo:
                    return await ctx.send("That repo has already been added")
            for repo in cfg.repo_list:
                if repo_to_add == repo:
                    return await ctx.send("That repo is a default repo")
            async with aiohttp.ClientSession() as session:
                async with session.get("https://cydia.s0n1c.org/cydia/" + "?url=" + repo_to_add) as resp:
                    if resp.status == 200 and json.loads(await resp.text())["status"]:
                        servers["servers"][str(ctx.message.guild.id)]["repo_list"].append(repo_to_add)
                        f.seek(0)
                        json.dump(servers, f, indent=4)
                        return await ctx.send("Repo succesfully added")
                    else:
                        print("repo not found")

    @repo.command()
    async def remove(self, ctx, repo_to_remove):
        with open("config/servers.json", 'r') as f:
            servers = json.load(f)
        with open("config/servers.json", 'w') as f:
            for repo in servers["servers"][str(ctx.message.guild.id)]["repo_list"]:
                if repo_to_remove == repo:
                    servers["servers"][str(ctx.message.guild.id)]["repo_list"].remove(repo)
            for repo in cfg.repo_list:
                if repo_to_remove == repo:
                    return await ctx.send("That repo is a default repo and can't be removed")
            print(servers)
            f.seek(0)
            json.dump(servers, f, indent=4)
            return await ctx.send("Repo successfully removed")


def setup(bot):
    bot.add_cog(repos(bot))
