import discord
import asyncio
from discord.ext import commands

import json
import requests
from packaging import version
from bs4 import BeautifulSoup
from zalgo_text import zalgo as z
from pyfiglet import Figlet
import time

# get token from ext file for security
with open('token.txt', 'r') as f:
    token = f.read().strip()

# get id from ext file for security
with open('id.txt', 'r') as f:
    my_id = int(f.read().strip())

prefix = '$'
embed_color = discord.Colour.from_rgb(150, 200, 250)
bot = commands.Bot(command_prefix=prefix, description="", case_insensitive=True, owner_id=my_id)

profile_enabled = True
canijb_enabled = True
docs_enabled = True
tweak_enabled = True
ascii_enabled = True
zalgo_enabled = True
header_enabled = True
framework_enabled = True
say_enabled = False


@bot.event
async def on_ready():
    print('Successfully connected!')
    print('Under user - ' + bot.user.name)
    print('And ID - ' + str(bot.user.id))
    print('------\n')
    await bot.change_presence(activity=discord.Game(name='$help'))


@bot.command(aliases=['tvos'])
async def profile(ctx):

    if(profile_enabled):
        ctx.message.delete()
        await ctx.send(ctx.message.author.mention + " Here you go:", file=discord.File('profile.mobileconfig'))
    else:
        await ctx.send("Command `profile` is disabled")


@bot.command(aliases=['canijailbreak', 'jb'], usage='[ios]')
async def canijb(ctx, ios: str, ios2: str = ""):

    if(canijb_enabled):

        # deletes message containing command
        ctx.message.delete()

        if (ios.lower() == "ios"):
            ios = ios2

        # logs the command issued
        print("------\n" + prefix + "canijb " + ios)

        # fetches json api, loads into list
        r = requests.get("https://canijailbreak.com/jailbreaks.json")
        t = r.text
        data = json.loads(t)
        jailbreaks = data["jailbreaks"]

        jailbroken = False
        done = False

        for x in range(len(jailbreaks)):

            # iterates through the list until it finds data for matching version
            if (version.parse(str(jailbreaks[x]["ios"]["start"])) <= version.parse(ios)) and (version.parse(str(jailbreaks[x]["ios"]["end"])) >= version.parse(ios)):

                # checks if it can be jailbroken
                jailbroken = jailbreaks[x]["jailbroken"]
                if (jailbroken):
                    done = True

                    # grabs name of the tool and the url from the api
                    url = jailbreaks[x]["url"]
                    name = jailbreaks[x]["name"]

                    # helpful message containing tool name and url
                    embed = discord.Embed(title="iOS " + ios + " can be jailbroken!", description="", color=embed_color, url="https://canijailbreak.com/")
                    embed.add_field(name="Use the tool " + name + " which you can get at:", value=url, inline=False)
                    # embed.set_footer(icon_url=ctx.message.author.avatar_url_as(), text="Requested by " + str(ctx.message.author))
                    await ctx.send(embed=embed)
                    print("Successful")
                    break
                else:
                    await ctx.send("iOS " + ios + " can't be jailbroken!")
                    print("Successful")
                    done = True
                    break
            else:
                continue
        if (not jailbroken and not done):
            await ctx.send("Couldn't find data for iOS " + ios)
            print("Failed")

    else:
        await ctx.send("Command `canijb` is disabled")


@bot.command(aliases=['tweakinfo', 'theme'], usage='[tweak]')
async def tweak(ctx, tweak: str, tweak2: str = '', tweak3: str = '', tweak4: str = ''):

    if(tweak_enabled):

        # allows for multi word input
        tweak = tweak + tweak2 + tweak3 + tweak4

        # logs the command issued
        print("------\n" + prefix + "tweak " + tweak)

        # grabs data about tweak from sauriks api
        r = requests.get("https://cydia.saurik.com/api/macciti?query=" + tweak.replace(' ', '').lower().strip())
        t = r.text
        data = json.loads(t)

        # checks if the tweak matches the api's first response
        for x in range(len(data["results"])):
            rtweak = data["results"][x]
            if (rtweak["display"].replace(' ', '').lower().strip() == tweak.replace(' ', '').lower().strip()):

                # gathers basic info
                tweakname = rtweak["display"]
                bundleid = rtweak["name"]
                section = rtweak["section"]
                summary = rtweak["summary"]
                # version = rtweak["version"]
                url = "http://cydia.saurik.com/package/" + bundleid
                icon_url = "http://cydia.saurik.com/icon@2x/" + bundleid + ".png"

                # gets package price
                r = requests.get("http://cydia.saurik.com/api/ibbignerd?query=" + bundleid).text
                pr = json.loads(r)
                if pr is None:
                    price = "Free"
                else:
                    price = pr["msrp"]

                # grabs the repo tweak is hosted on (stolen from https://github.com/hizinfiz/TweakInfoBot/)
                html = requests.get(url).text
                soup = BeautifulSoup(html, "html.parser")
                repo = soup.find('span', {'class': 'source-name'}).contents[0]
                if repo == 'ModMyi.com':
                    repo = 'ModMyi'

                # constructs nice embed
                embed = discord.Embed(title=tweakname, url=url, color=embed_color)
                embed.set_footer(text=tweakname, icon_url=icon_url)
                embed.add_field(name="Section", value=section, inline=True)
                embed.add_field(name="Repo", value=repo, inline=True)
                # embed.add_field(name="Version", value=version, inline=True)
                embed.add_field(name="Price", value=price, inline=True)
                embed.add_field(name="Summary", value=summary, inline=False)
                await ctx.send(embed=embed)
                print("Successful")
                return

        # if command fails
        await ctx.send("Couldn't find info for tweak " + tweak)
        print("Failed")

    else:
        await ctx.send("Command `tweak` is disabled")


@bot.command(aliases=['doc'], usage='[doc]')
async def docs(ctx, doc: str = ''):

    if(docs_enabled):

        # logs command issued
        print("------\n" + prefix + "docs " + doc)
        done = False

        # generates url to relevent doc and retrieves summary
        pages = ["objectivec", "uikit", "webkit", "foundation", "coregraphics", "coredata", "kernel", "coreservices"]
        for x in pages:
            url = "https://developer.apple.com/documentation/" + x + "/" + doc + "?language=objc"
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")

            try:
                summary = soup.find('p').contents[0]
                done = True
                print("Success!")
                break
            except AttributeError:
                continue

        if done:

            # goes to main objc doc page if nothing specified
            if(doc == ''):
                doc = "Objective-C"

            # constructs embed containing url and summary
            embed = discord.Embed(title="Docs for " + doc, url=url, color=embed_color)
            embed.add_field(name="Summary", value=summary, inline=False)
            await ctx.send(embed=embed)
        else:
            print("Failed")
            await ctx.send("Unable to find doc for " + doc)

    else:
        await ctx.send("Command `docs` is disabled")


@bot.command(usage='[object]', aliases=['h', 'headers'])
async def header(ctx, text: str, uinput0: str = '', uinput1: str = ''):  # , ios: str = '11.1.2'):
    if(header_enabled):

        text = text.replace(' ', '').strip()

        # logs command issued
        print("------\n" + prefix + "header " + text)
        ios = "11.1.2"

        # appends .h if it isnt there already
        if not text[-2:] == ".h":
            text = text + ".h"

        framework = ""

        if not uinput0 == '':
            try:
                int(uinput0.replace('.', ''))
                ios = str(uinput0)
            except ValueError:
                framework = str(uinput0)

            if not uinput1 == '':
                try:
                    int(uinput1.replace('.', ''))
                    ios = str(uinput1)
                except ValueError:
                    framework = str(uinput1)

        if not framework == "" and not framework[-10:] == ".framework":
            framework = framework + ".framework"

        pages = ["SpringBoard", "UIKit.framework", "WebKit.framework", "Foundation.framework", "CoreData.framework", "CoreServices.framework"]
        for x in pages:

            if not framework == "":

                url = "http://developer.limneos.net/index.php?ios=" + ios + "&framework=" + framework + "&header=" + text

            else:
                url = "http://developer.limneos.net/index.php?ios=" + ios + "&framework=" + x + "&header=" + text

            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            if str(soup).strip() == "Access error.":
                await ctx.send("Header " + text + " not found for iOS " + ios)
                print("Failed")
                return

            title = soup.title.contents[0]

            try:
                if(soup.findAll('div')[7].findAll('br')[1].contents[0].strip() == "Error resolving file."):
                    continue

                else:
                    embed = discord.Embed(title=title, url=url, color=embed_color)
                    await ctx.send(embed=embed)
                    print("Successful!")
                    return

            except IndexError:
                if soup.findAll('div')[6].findAll('br')[0].findAll('br')[0].contents[0].strip() == "Error resolving file.":
                    continue
                else:
                    embed = discord.Embed(title=title, url=url, color=embed_color)
                    await ctx.send(embed=embed)
                    print("Successful!")
                    return


        await ctx.send("Couldn't find header for " + text)
        print("Failed")

    else:
        await ctx.send("Command `header` is disabled")


@bot.command(aliases=['f'])
async def framework(ctx, text: str):
    if(framework_enabled):

        text = text.replace(' ', '').strip()

        # logs command issued
        print("------\n" + prefix + "framework " + text)
        ios = "11.1.2"

        if not text == "SpringBoard" and not text[:-10] == ".framework":
            text_frm = text + ".framework"
        else:
            text_frm = text

        url = "http://developer.limneos.net/index.php?ios=" + ios + "&framework=" + text_frm
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")

        title = soup.title.contents[0]

        try:
            if(soup.findAll('div')[7].findAll('pre')[0].contents[0].strip() == "Given Framework doesn't exist in my database, sorry."):

                await ctx.send("Couldn't find framework " + text)
                print("Failed")
            else:
                embed = discord.Embed(title=title, url=url, color=embed_color)
                await ctx.send(embed=embed)
                print("Successful!")
                return

        except IndexError:
            embed = discord.Embed(title=title, url=url, color=embed_color)
            await ctx.send(embed=embed)
            print("Successful!")
            return

    else:
        await ctx.send("Command `framework` is disabled")


@bot.command(aliases=['saythis', 's'])
async def say(ctx, *, words):
    if(say_enabled):
        await ctx.send(words)
    else:
        await ctx.send("Command `say` is disabled")


@bot.command(usage='[text]', aliases=['z'])
async def zalgo(ctx, *, words):
    if(zalgo_enabled):
        zalgod = z.zalgo().zalgofy(words)
        await ctx.send(zalgod)
    else:
        await ctx.send("Command `zalgo` is disabled")


@bot.command(usage='[text]', aliases=['a'])
async def ascii(ctx, *, words):
    if(ascii_enabled):
        f = Figlet()
        asciid = f.renderText(words)
        await ctx.send("```" + asciid + "```")
    else:
        await ctx.send("Command `ascii` is disabled")


@bot.command(usage='[cmd]', aliases=['e'])
async def enable(ctx, cmd):

    # only lets bot owner run it
    if ctx.author.id == bot.owner_id:

        if(cmd == "jb" or cmd == "canijb"):
            global canijb_enabled
            canijb_enabled = True
        elif(cmd == "profile" or cmd == "tvos"):
            global profile_enabled
            profile_enabled = True
        elif(cmd == "doc" or cmd == "docs"):
            global docs_enabled
            docs_enabled = True
        elif(cmd == "tweak" or cmd == "info"):
            global tweak_enabled
            tweak_enabled = True
        elif(cmd == "ascii"):
            global ascii_enabled
            ascii_enabled = True
        elif(cmd == "header"):
            global header_enabled
            header_enabled = True
        elif(cmd == "framework"):
            global framework_enabled
            framework_enabled = True
        elif(cmd == "zalgo"):
            global zalgo_enabled
            zalgo_enabled = True
        elif(cmd == "say"):
            global say_enabled
            say_enabled = True
        else:
            await ctx.send("Command `" + cmd + "` not found")
            return
        await ctx.send("Enabled command `" + cmd + "`")

    else:
        await ctx.send("You don't have permission to do that")


@bot.command(usage='[cmd]', aliases=['d'])
async def disable(ctx, cmd):

    # only lets bot owner run it
    if ctx.author.id == bot.owner_id:

        if(cmd == "jb" or cmd == "canijb"):
            global canijb_enabled
            canijb_enabled = False
        elif(cmd == "profile" or cmd == "tvos"):
            global profile_enabled
            profile_enabled = False
        elif(cmd == "doc" or cmd == "docs"):
            global docs_enabled
            docs_enabled = False
        elif(cmd == "tweak" or cmd == "info"):
            global tweak_enabled
            tweak_enabled = False
        elif(cmd == "ascii"):
            global ascii_enabled
            ascii_enabled = False
        elif(cmd == "header"):
            global header_enabled
            header_enabled = False
        elif(cmd == "framework"):
            global framework_enabled
            framework_enabled = True
        elif(cmd == "zalgo"):
            global zalgo_enabled
            zalgo_enabled = False
        elif(cmd == "say"):
            global say_enabled
            say_enabled = False
        else:
            await ctx.send("Command `" + cmd + "` not found")
            return
        await ctx.send("Disabled command `" + cmd + "`")

    else:
        await ctx.send("You don't have permission to do that")


@bot.command(aliases=['game'])
async def play(ctx, *, game):
    await bot.change_presence(activity=discord.Game(name=game))


@bot.command()
async def ping(ctx):
    t1 = time.perf_counter()
    await ctx.trigger_typing()
    t2 = time.perf_counter()
    embed = discord.Embed(color=embed_color)
    embed.add_field(name="Pong! Response time: ", value="{}ms".format(round((t2 - t1) * 1000)), inline=False)
    await ctx.send(embed=embed)


bot.remove_command('help')


@bot.group()
async def help(ctx):
    if ctx.invoked_subcommand is None:

        # embed containing help
        embed = discord.Embed(title="Jailbreak Bot Help", color=embed_color)
        embed.add_field(name="$canijb [ios]  or  $jb [ios]", value="Check if the given iOS is jailbreak-able", inline=False)
        embed.add_field(name="$profile  or  $tvos", value="Sends the tvOS 11 beta profile in the current channel, allowing you to 1-click install it", inline=True)
        embed.add_field(name="$tweak [tweak]  or  $theme [theme]", value="Provides information about and a download link for a specific tweak", inline=True)
        embed.add_field(name="$docs [object]  or  $doc [data type]  etc.", value="Provides a link to requested Apple Obj-C doc, as well as a short summary", inline=True)
        embed.add_field(name="$header [header] <ios> <framework>  or  $h [header] <framework> <ios>", value="Provides a link to requested header file", inline=True)
        embed.add_field(name="$framework [framework]  or  $f [framework]", value="Provides a link to requested framework", inline=True)
        embed.set_footer(text="Type $help [command] to get detailed info about a certain command", icon_url=bot.user.avatar_url_as())
        await ctx.send(embed=embed)


@help.command(aliases=['jb', 'canijailbreak'])
async def canijb(ctx):
    embed = discord.Embed(title="Jailbreak Bot Help", color=embed_color)
    embed.add_field(name="$canijb [ios]  or  $jb [ios]", value="Check if the given iOS is jailbreak-able. Works for every ios except 5, not sure . Sends name of the jailbreak tool and link to get it", inline=False)
    embed.add_field(name="Examples", value="$canijb 11.0\n$canijb ios 6.1.3\n$jb 7.1.2\n$jb ios 5.1", inline=False)
    await ctx.send(embed=embed)

@help.command(aliases=['tvos'])
async def profile(ctx):
    embed = discord.Embed(title="Jailbreak Bot Help", color=embed_color)
    embed.add_field(name="$profile  or  $tvos", value="Sends the tvOS 11 beta profile in the current channel, allowing you to 1-click install it", inline=True)
    embed.add_field(name="Examples", value="$profile\n$tvos", inline=False)
    await ctx.send(embed=embed)


@help.command(aliases=['theme'])
async def tweak(ctx):
    embed = discord.Embed(title="Jailbreak Bot Help", color=embed_color)
    embed.add_field(name="$tweak [tweak]  or  $theme [theme]", value="Provides information about and a download link for a specific tweak. Currently only works for defualt repos", inline=True)
    embed.add_field(name="Examples", value="$tweak icleaner\n$tweak classicfolders 2\n$theme indigo", inline=False)
    await ctx.send(embed=embed)


@help.command(aliases=['doc'])
async def docs(ctx):
    embed = discord.Embed(title="Jailbreak Bot Help", color=embed_color)
    embed.add_field(name="$docs [object]  or  $doc [data type]  etc.", value="Provides a link to requested Apple Obj-C doc, as well as a short summary. Only frameworks currently supported are: Objective-C, UIKit, WebKit, Foundation, CoreGraphics, CoreData, Kernel, CoreServices", inline=True)
    embed.add_field(name="Examples", value="$docs NSObject\n$doc UIViewController\n$docs CGFloat", inline=False)
    await ctx.send(embed=embed)


@help.command(aliases=['h'])
async def header(ctx):
    embed = discord.Embed(title="Jailbreak Bot Help", color=embed_color)
    embed.add_field(name="$header [header] <ios> <framework>  or  $h [header] <framework> <ios>", value="Provides a link to requested header file. Case Sensitive. Generates a link to developer.limneos.net. Only frameworks currently supported are: SpringBoard, UIKit, WebKit, Foundation, CoreData, CoreServices. However it will check any frameworks provided explicitly", inline=True)
    embed.add_field(name="Examples", value="$header SBAlertView\n$h SBPowerDownAlertView 10.2\n$h CXStartCallAction.h CallKit 10.1.1", inline=False)
    await ctx.send(embed=embed)

@help.command(aliases=['f'])
async def framework(ctx):
    embed = discord.Embed(title="Jailbreak Bot Help", color=embed_color)
    embed.add_field(name="$framework [framework]  or  $f [framework]", value="Provides a link to requested framework on developer.limneos.net. Case Sensitive.", inline=True)
    embed.add_field(name="Examples", value="$framework SpringBoard\n$f UIKit\n$f Foundation", inline=False)
    await ctx.send(embed=embed)


@canijb.error
async def canijb_on_error(ctx, error):
    await ctx.send("Usage:")
    await ctx.send("``" + prefix + "canijb [ios]``")


@tweak.error
async def tweak_on_error(ctx, error):
    await ctx.send("Usage:")
    await ctx.send("``" + prefix + "tweak [tweak]``")


@docs.error
async def docs_on_error(ctx, error):
    await ctx.send("Usage:")
    await ctx.send("``" + prefix + "docs [object]``")


@header.error
async def header_on_error(ctx, error):
    await ctx.send("Usage:")
    await ctx.send("``" + prefix + "header [header]``")


@zalgo.error
async def zalgo_on_error(ctx, error):
    await ctx.send("Usage:")
    await ctx.send("``" + prefix + "zalgo [text]``")


@ascii.error
async def ascii_on_error(ctx, error):
    await ctx.send("Usage:")
    await ctx.send("``" + prefix + "ascii [text]``")


bot.run(token)
