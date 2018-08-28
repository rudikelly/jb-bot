import discord
from discord.ext import commands


class help():

    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx, error):
        await ctx.send("Usage:")
        await ctx.send("``$help``")
        print("$help errored:")
        print(error)

    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:

            page = 1

            # embed containing help
            embed = discord.Embed(title="Jailbreak Bot Help | Page " + str(page), color=discord.Colour(0x96c8fa))
            embed.add_field(name="$canijb [ios]  or  $jb [ios]", value="Check if the given iOS is jailbreak-able", inline=False)
            embed.add_field(name="$profile  or  $tvos", value="Sends the tvOS 11 beta profile in the current channel, allowing you to 1-click install it", inline=True)
            embed.add_field(name="$tweak [tweak]  or  $theme [theme]", value="Provides information about and a download link for a specific tweak", inline=True)
            embed.add_field(name="$docs [object]  or  $doc [data type]  etc.", value="Provides a link to requested Apple Obj-C doc, as well as a short summary", inline=True)
            embed.add_field(name="$header [header] <ios> <framework>  or  $h [header] <framework> <ios>", value="Provides a link to requested header file", inline=True)
            embed.add_field(name="$framework [framework]  or  $f [framework]", value="Provides a link to requested framework", inline=True)
            embed.add_field(name="$xkcd random  or  $xkcd latest  or  $xkcd [number]", value="Sends the requested xkcd comic in the current channel. Defaults to random", inline=True)
            embed.set_footer(text="Type $help [command] to get detailed info about a certain command", icon_url=self.bot.user.avatar_url_as())
            msg = await ctx.send(embed=embed)

            await msg.add_reaction(u"\u2B05")
            await msg.add_reaction(u"\u27A1")

    @help.command(aliases=['jb', 'canijailbreak'], name="canijb")
    async def canijb_help(self, ctx):
        embed = discord.Embed(title="Jailbreak Bot Help", color=discord.Colour(0x96c8fa))
        embed.add_field(name="$canijb [ios]  or  $jb [ios]", value="Check if the given iOS is jailbreak-able. Works for every ios except 5, not sure . Sends name of the jailbreak tool and link to get it", inline=False)
        embed.add_field(name="Examples", value="$canijb 11.0\n$canijb ios 6.1.3\n$jb 7.1.2\n$jb ios 5.1", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['tvos'], name="profile")
    async def profile_help(self, ctx):
        embed = discord.Embed(title="Jailbreak Bot Help", color=discord.Colour(0x96c8fa))
        embed.add_field(name="$profile  or  $tvos", value="Sends the tvOS 11 beta profile in the current channel, allowing you to 1-click install it", inline=True)
        embed.add_field(name="Examples", value="$profile\n$tvos", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['theme'], name="tweak")
    async def tweak_help(self, ctx):
        embed = discord.Embed(title="Jailbreak Bot Help", color=discord.Colour(0x96c8fa))
        embed.add_field(name="$tweak [tweak]  or  $theme [theme]", value="Provides information about and a download link for a specific tweak. Currently only works for defualt repos", inline=True)
        embed.add_field(name="Examples", value="$tweak icleaner\n$tweak classicfolders 2\n$theme indigo", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['doc'], name="docs")
    async def docs_help(self, ctx):
        embed = discord.Embed(title="Jailbreak Bot Help", color=discord.Colour(0x96c8fa))
        embed.add_field(name="$docs [object]  or  $doc [data type]  etc.", value="Provides a link to requested Apple Obj-C doc, as well as a short summary. Only frameworks currently supported are: Objective-C, UIKit, WebKit, Foundation, CoreGraphics, CoreData, Kernel, CoreServices", inline=True)
        embed.add_field(name="Examples", value="$docs NSObject\n$doc UIViewController\n$docs CGFloat", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['h'], name="header")
    async def header_help(self, ctx):
        embed = discord.Embed(title="Jailbreak Bot Help", color=discord.Colour(0x96c8fa))
        embed.add_field(name="$header [header] <ios> <framework>  or  $h [header] <framework> <ios>", value="Provides a link to requested header file. Case Sensitive. Generates a link to developer.limneos.net. Only frameworks currently supported are: SpringBoard, UIKit, WebKit, Foundation, CoreData, CoreServices. However it will check any frameworks provided explicitly", inline=True)
        embed.add_field(name="Examples", value="$header SBAlertView\n$h SBPowerDownAlertView 10.2\n$h CXStartCallAction.h CallKit 10.1.1", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=['f'], name="framework")
    async def framework_help(self, ctx):
        embed = discord.Embed(title="Jailbreak Bot Help", color=discord.Colour(0x96c8fa))
        embed.add_field(name="$framework [framework]  or  $f [framework]", value="Provides a link to requested framework on developer.limneos.net. Case Sensitive.", inline=True)
        embed.add_field(name="Examples", value="$framework SpringBoard\n$f UIKit\n$f Foundation", inline=False)
        await ctx.send(embed=embed)

    @help.command(name="xkcd")
    async def xkcd_help(self, ctx):
        embed = discord.Embed(title="Jailbreak Bot Help", color=discord.Colour(0x96c8fa))
        embed.add_field(name="$xkcd random  or  $xkcd latest  or  $xkcd [number]", value="Sends the requested xkcd comic in the current channel. Defaults to random", inline=True)
        embed.add_field(name="Examples", value="$xkcd latest\n$xkcd 678\n$xkcd", inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(help(bot))
