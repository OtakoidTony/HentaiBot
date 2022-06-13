import json
import os
import math
import requests
import random
import nextcord
from nextcord.ext.commands import AutoShardedBot
from nextcord.ext.application_checks import is_nsfw
from nextcord.ext.application_checks.errors import ApplicationNSFWChannelRequired

intents=nextcord.Intents(messages = True, members = True, typing = True, guilds = True)
bot = AutoShardedBot(intents=intents)
game = nextcord.Game("Naughty")
bot.remove_command('help')

token = os.environ['TOKEN']


def toHHMMSS(this):
    myNum = int(this)
    hours = math.floor(myNum / 3600000)
    minutes = math.floor((myNum - (hours * 3600000)) / 60000)
    seconds = math.floor((myNum - (hours * 3600000) - (minutes * 60000)) / 1000)

    if (hours < 10):
        hours = "0" + str(hours)
    else:
        hours = str(hours)
    if (minutes < 10):
        minutes = "0" + str(minutes)
    else:
        minutes = str(minutes)
    if (seconds < 10):
        seconds = "0" + str(seconds)
    else:
        seconds = str(seconds)
    return hours + ':' + minutes + ':' + seconds


@bot.event
async def on_ready():
    print(bot.user.name)
    await bot.change_presence(status=nextcord.Status.idle, activity=game)


@bot.slash_command()
async def help(ctx:nextcord.Interaction):
    await ctx.response.defer()
    ret = "```\n"
    ret += "gelbooru [tags]\n"
    ret += "Get image from Gelbooru.\n"
    ret += "yandere [tags]\n"
    ret += "Get image from Yandere.\n"
    ret += "hanime [title]\n"
    ret += "Retrieve adult animation information from HTV (tag required).\n"
    ret += "```"
    await ctx.followup.send(ret)

@bot.slash_command()
@is_nsfw()
async def gelbooru(ctx:nextcord.Interaction, tag = nextcord.SlashOption(required=False)):
    await ctx.response.defer()
    if tag == None:
        api="https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:explicit+-loli+-shota+-cub"
        response = requests.get(api)
        ret = json.loads(response.text)
        image = random.choice(ret['post'])["file_url"]
    else:
        api="https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:explicit+-loli+-shota+-cub" + tag
        response = requests.get(api)
        ret = json.loads(response.text)
        image = random.choice(ret['post'])["file_url"]
    embed = nextcord.Embed(title="Gelbooru API").set_image(url=image)
    await ctx.followup.send(embed=embed)

@bot.slash_command()
@is_nsfw()
async def yandere(ctx: nextcord.Interaction, tag=nextcord.SlashOption(required=False)):
    await ctx.response.defer()
    if tag == None:
        ret = random.choice(requests.get(
            "https://yande.re/post.json?limit=100&tags=rating:explicit+-loli+-shota+-cub").json())
    else:
        ret = random.choice(requests.get(
            "https://yande.re/post.json?limit=100&tags=rating:explicit+-loli+-shota+-cub" + tag).json())
    embed = nextcord.Embed(title="Yandere API").set_image(url=ret["file_url"])
    embed.set_footer(text=ret["created_at"])
    await ctx.followup.send(embed=embed)

@bot.slash_command()
@is_nsfw()
async def konachan(ctx:nextcord.Interaction, tag=nextcord.SlashOption(required=False)):
    await ctx.response.defer()
    if tag == None:
        konachan_api = random.choice(requests.get("https://konachan.com/post.json?s=post&q=index&limit=100&tags=rating:explicit+-loli+-shota+-cub").json())

    else:
        konachan_api = random.choice(requests.get(f"https://konachan.com/post.json?s=post&q=index&limit=100&tags=rating:explicit+-loli+-shota+-cub+{tag}").json())

    embed = nextcord.Embed(color=0xFFC0CB)
    embed.set_image(url=konachan_api['file_url'])
    embed.set_footer(text="Fetched from Konachan")
    await ctx.followup.send(embed=embed)

@bot.slash_command()
@is_nsfw()
async def hanime(ctx: nextcord.Interaction, tag=nextcord.SlashOption(required=True)):
    await ctx.response.defer()
    res = requests.get("https://members.hanime.tv/api/v5/hentai-videos/" + tag.replace(' ', '-'), headers={'User-Agent': "Mozilla/5.0", 'X-Directive': "api"}).json()["hentai_video"]
    embed = nextcord.Embed(title="Yandere API", description=res["brand"]).set_image(url=res["poster_url"])
    embed.set_thumbnail(url = res["cover_url"])
    embed.add_field(name="Views", value=res["views"], inline=True)
    embed.add_field(name="Interests", value=res["interests"], inline=True)
    embed.add_field(name="Duration", value=toHHMMSS(res["duration_in_ms"]), inline=True)
    embed.add_field(name="Likes", value=res["likes"], inline=True)
    embed.add_field(name="Dislikes", value=res["dislikes"], inline=True)
    embed.add_field(name="Downloads", value=res["downloads"], inline=True)
    embed.set_footer(text=res["released_at"])
    await ctx.followup.send(embed=embed)

@bot.event
async def on_application_command_error(ctx:nextcord.Interaction, error):
    if isinstance(error, ApplicationNSFWChannelRequired):
        await ctx.response.defer()
        embed = nextcord.Embed(title='Hentai Failed', description="Hentai couldn't be sent in this channel", color=0xff0000).add_field(name="Reason", value="Channel is not NSFW enabled")
        await ctx.followup.send(embed=embed)

bot.run(token)
