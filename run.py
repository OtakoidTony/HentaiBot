import discord
import os
import math
import requests
import random

client = discord.Client()
game = discord.Game("야한거")

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


@client.event
async def on_ready():
    print(client.user.name)
    await client.change_presence(status=discord.Status.idle, activity=game)

prefix = "hentai."

@client.event
async def on_message(message):
    if message.author.bot:
        return None
    if message.content[:len(prefix)] == "hentai.":
        command = message.content[len(prefix):]
        if command.startswith("help"):
            ret = "```\n"
            ret += prefix + "gelbooru [tags]\n"
            ret += "  Gelbooru로부터 이미지를 불러옵니다.\n"
            ret += prefix + "yandere [tags]\n"
            ret += "  Yandere로부터 이미지를 불러옵니다.\n"
            ret += prefix + "hanime [title]\n"
            ret += "  HTV로부터 성인 애니메이션 정보를 불러옵니다.\n"
            ret += "```"
            await message.channel.send(ret)
        if command.startswith("gelbooru"):
            tag = command[9:]
            ret = random.choice(requests.get("https://gelbooru.com//index.php?page=dapi&s=post&q=index&json=1&tags=" + tag).json())
            embed = discord.Embed(title="Gelbooru API").set_image(url=ret["file_url"])
            embed.set_footer(text=ret["created_at"])
            await message.channel.send(embed=embed)
        if command.startswith("yandere"):
            tag = command[8:]
            ret = random.choice(requests.get("https://yande.re/post.json?tags=" + tag).json())
            embed = discord.Embed(title="Yandere API").set_image(url=ret["file_url"])
            embed.set_footer(text=ret["created_at"])
            await message.channel.send(embed=embed)
        if command.startswith("hanime"):
            tag = command[7:]
            res = requests.get("https://members.hanime.tv/api/v5/hentai-videos/" + tag.replace(' ', '-'), headers={'User-Agent': "Mozilla/5.0", 'X-Directive': "api"}).json()["hentai_video"]
            embed = discord.Embed(title="Yandere API", description=res["brand"]).set_image(url=res["poster_url"])
            embed.set_thumbnail(url = res["cover_url"])
            embed.add_field(name="시청수", value=res["views"], inline=True)
            embed.add_field(name="흥미있음", value=res["interests"], inline=True)
            embed.add_field(name="시간", value=toHHMMSS(res["duration_in_ms"]), inline=True)
            embed.add_field(name="좋아요", value=res["likes"], inline=True)
            embed.add_field(name="싫어요", value=res["dislikes"], inline=True)
            embed.add_field(name="다운로드수", value=res["downloads"], inline=True)
            embed.set_footer(text=res["released_at"])
            await message.channel.send(embed=embed)
client.run(token)
