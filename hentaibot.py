import json
import os
import requests
import random
import nekos_fun
import discord
from discord import app_commands
from typing import Optional, Literal
from dotenv import load_dotenv


class Bot(discord.Client):
    def __init__(self):
        super().__init__()
        self.tree = app_commands.CommandTree(self)
        self.tree.on_error = self.on_app_command_error

    async def setup_hook(self):
        await self.tree.sync()


intents = discord.Intents(messages=True, members=True, typing=True, guilds=True)
bot = Bot(intents=intents)
game = discord.Game("Naughty")

load_dotenv()
token = os.getenv('token')


@bot.event
async def on_ready():
    print(bot.user.name)
    await bot.change_presence(status=discord.Status.idle, activity=game)


@bot.tree.command(description="Shows the help menu", nsfw=True)
async def help(ctx: discord.Interaction):
    await ctx.response.defer()
    ret = "```\n"
    ret += "gelbooru [tags]\n"
    ret += "Get image/video from Gelbooru.\n"
    ret += "yandere [tags]\n"
    ret += "Get image from Yandere.\n"
    ret += "konachan [tags]\n"
    ret += "Get image from Konachan.\n"
    ret += "danbooru [tags]\n"
    ret += "Get image from danbooru.\n"
    ret += "nekolewd\n"
    ret += "Get lewded nekos from NekoLove.\n"
    ret += "nekosfun\n"
    ret += "Get images/gifs from NekosLife.\n"
    ret += "```"
    await ctx.followup.send(ret)


@bot.tree.command(description="Get hentai from Gelbooru", nsfw=True)
@app_commands.describe(tag="Add a tag")
async def gelbooru(ctx: discord.Interaction, tag: Optional[str] = None) -> None:
    await ctx.response.defer()
    formated_tag = tag.replace(" ", "_")
    if tag == None:
        api = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:explicit+-loli+-shota+-cub"

    else:
        api = (
            "https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=rating:explicit+-loli+-shota+-cub"
            + formated_tag
        )
    response = requests.get(api)
    ret = json.loads(response.text)
    post = random.choice(ret["post"])
    source = post["source"]
    owner = post["owner"]
    score = post["score"]
    image: str = post["file_url"]
    created_at = post["created_at"]
    if image.endswith(".mp4"):
        await ctx.followup.send(image)
    else:
        embed = discord.Embed(title="Created by {}".format(owner))
        embed.add_field(
            name="Source", value="[Click here]({})".format(source), inline=True
        )
        embed.add_field(name="Score", value=score, inline=True)
        embed.set_image(url=image)
        embed.set_footer(text="Fetched from Gelbooru\nCreated at {}".format(created_at))
        await ctx.followup.send(embed=embed)


@bot.tree.command(description="Get hentai from Yandere", nsfw=True)
@app_commands.describe(tag="Add a tag")
async def yandere(ctx: discord.Interaction, tag: Optional[str] = None) -> None:
    await ctx.response.defer()
    if tag == None:
        ret = random.choice(
            requests.get(
                "https://yande.re/post.json?limit=100&shown:true&tags=rating:explicit+-loli+-shota+-cub"
            ).json()
        )
    else:
        tag = tag.replace(" ", "_")
        ret = random.choice(
            requests.get(
                "https://yande.re/post.json?limit=100&shown:true&tags=rating:explicit+-loli+-shota+-cub"
                + tag
            ).json()
        )
    created_at = ret["created_at"]
    file = ret["file_url"]
    author = ret["author"]
    source = ret["source"]
    score = ret["score"]
    embed = discord.Embed(title="Created by {}".format(author))
    embed.add_field(name="Source", value="[Click here]({})".format(source), inline=True)
    embed.add_field(name="Score", value=score, inline=True)
    embed.set_image(url=file)
    embed.set_footer(text="Fetched from Yande.re\nCreated at {}".format(created_at))
    await ctx.followup.send(embed=embed)


@bot.tree.command(description="Get hentai from Konachan", nsfw=True)
@app_commands.describe(tag="Add a tag")
async def konachan(ctx: discord.Interaction, tag: Optional[str] = None) -> None:
    await ctx.response.defer()
    if tag == None:
        ret = random.choice(
            requests.get(
                "https://konachan.com/post.json?s=post&q=index&limit=100&tags=rating:explicit+-loli+-shota+-cub"
            ).json()
        )

    else:
        tag = tag.replace(" ", "_")
        ret = random.choice(
            requests.get(
                f"https://konachan.com/post.json?s=post&q=index&limit=100&tags=rating:explicit+-loli+-shota+-cub"
                + tag
            ).json()
        )

    created_at = ret["created_at"]
    file = ret["file_url"]
    author = ret["author"]
    source = ret["source"]
    score = ret["score"]
    embed = discord.Embed(title="Created by {}".format(author))
    embed.add_field(name="Source", value="[Click here]({})".format(source), inline=True)
    embed.add_field(name="Score", value=score, inline=True)
    embed.set_image(url=file)
    embed.set_footer(text="Fetched from Konachan\nCreated at {}".format(created_at))
    await ctx.followup.send(embed=embed)


@bot.tree.command(description="Get hentai from Danbooru", nsfw=True)
@app_commands.describe(tag="Add a tag")
async def danbooru(ctx: discord.Interaction, tag: Optional[str] = None) -> None:
    await ctx.response.defer()
    if tag == None:
        ret = random.choice(
            requests.get(
                "https://danbooru.donmai.us/posts.json?limit=100&tags=rating:explicit-loli-shota-cub",
                headers="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
            ).json()
        )

    else:
        tag = tag.replace(" ", "_")
        ret = random.choice(
            requests.get(
                "https://danbooru.donmai.us/posts.json?limit=100&tags=rating:explicit-loli-shota-cub"
                + tag,
                headers="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
            ).json()
        )

    created_at = ret["created_at"]
    file = ret["file_url"]
    author = ret["tag_string_artist"]
    source = ret["source"]
    score = ret["score"]
    embed = discord.Embed(title="Created by {}".format(author))
    embed.add_field(name="Source", value="[Click here]({})".format(source), inline=True)
    embed.add_field(name="Score", value=score, inline=True)
    embed.set_image(url=file)
    embed.set_footer(text="Fetched from Danbooru\nCreated at {}".format(created_at))
    await ctx.followup.send(embed=embed)


@bot.tree.command(description="Get lewded nekos from NekoLove", nsfw=True)
async def nekolewd(ctx: discord.Interaction):
    await ctx.response.defer()
    ret = requests.get("https://neko-love.xyz/api/v1/nekolewd").json()
    response = ret["code"]
    image = ret["url"]

    if response != 200:
        embed = discord.Embed(
            description="Error with API!\nPlease contact the neko-love.xyz team. If the fault is not on their side, please reach up to me"
        )
        await ctx.followup.send(embed=embed)
    else:
        embed = discord.Embed()
        embed.set_image(url=image)
        embed.set_footer(text="Fetched from NekoLove")
        await ctx.followup.send(embed=embed)


@bot.tree.command(description="Get an image/gif from NekosLife", nsfw=True)
@app_commands.describe(tag="Which tag?")
async def nekosfun(
    ctx: discord.Interaction,
    tag: Optional[
        Literal[
            "ass", "bj", "boobs", "cum", "hentai", "spank", "gasm", "lesbian", "pussy"
        ]
    ],
):
    if tag == None:
        tags = [
            "ass",
            "bj",
            "boobs",
            "cum",
            "hentai",
            "spank",
            "gasm",
            "lesbian",
            "pussy",
        ]
        image = nekos_fun.nekofun(random.choice(tags))

    else:
        image = nekos_fun.nekofun(tag)

    if image != 200:
        await ctx.followup.send(image)
    else:
        embed = discord.Embed()
        embed.set_image(url=image)
        embed.set_footer(text="Fetched from Nekos.Fun")
        await ctx.followup.send(embed=embed)


@bot.event
async def on_app_command_error(
    ctx: discord.Interaction, error: app_commands.AppCommandError
):
    if isinstance(error, KeyError):
        embed = discord.Embed(
            title="Hentai Failed",
            description="Hentai couldn't be sent in this channel",
            color=0xFF0000,
        ).add_field(name="Reason", value="Tag not found")
        await ctx.followup.send(embed=embed)


bot.run(token)
