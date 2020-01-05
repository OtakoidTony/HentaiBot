import urllib.request
import os
import sqlite3
from discord.ext import commands
import codecs
import requests
from bs4 import BeautifulSoup
import random


class YandereApi:
    def __init__(self, tags):
        url = ("https://yande.re/post.json?limit=100&page=" + str(random.randrange(1, 5)) + "&tags=" + tags)
        res = requests.get(url)
        res = res.json()
        data = random.choice(res)

        self.id = data['id']
        self.tags = data['tags']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']
        self.approver_id = data['approver_id']
        self.author = data['author']
        self.change = data['change']
        self.source = data['source']
        self.file = data['file_url']
        self.preview = data['preview_url']
        self.sample = data['sample_url']
        self.jpeg = data['jpeg_url']


class Gelbooru:
    def __init__(self, tags):
        # https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tag=loli
        tags = tags.replace(' ', '+')
        url = ("https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&tags=" + tags+"&api_key=anonymous&user_id=9455")
        res = requests.get(url)
        res = res.json()
        data = random.choice(res)

        self.source = data['source']
        self.directory = data['directory']
        self.hash = data['hash']
        self.height = data['height']
        self.id = data['id']
        self.image = data['image']
        self.change = data['change']
        self.owner = data['owner']
        self.parent_id = data['parent_id']
        self.rating = data['rating']
        self.sample = data['sample']
        self.sample_height = data['sample_height']
        self.sample_width = data['sample_width']
        self.score = data['score']
        self.tags = data['tags']
        self.width = data['width']
        self.file_url = data['file_url']
        self.created_at = data['created_at']

        self.image_size = str(data['width']) + ' × ' + str(data['height'])
        self.sample_size = str(data['sample_width']) + ' × ' + str(data['sample_height'])


class Danbooru:
    def __init__(self, tags):
        url = ("https://danbooru.donmai.us/posts.json?page=" + str(random.randrange(1, 5)) + "&limit=100&tags=" + tags)
        res = requests.get(url)
        res = res.json()
        data = random.choice(res)

        tags = data['tag_string']
        tags = tags.replace("/\\/\\/\\ ", "")

        self.id = data['id']
        self.created_at = data['created_at']
        self.source = data['source']

        self.image_width = data['image_width']
        self.image_height = data['image_height']
        self.image_size = str(data['image_width']) + ' × ' + str(data['image_height'])

        # self.file_ext = data['file_ext']
        self.updated_at = data['updated_at']

        self.tags = tags
        self.pixiv_id = data['pixiv_id']
        self.artist = data['tag_string_artist']
        self.character = data['tag_string_character']
        self.copyright = data['tag_string_copyright']

        # ================[ Image Files ]================
        self.file = data['file_url']
        self.large = data['large_file_url']
        self.preview = data['preview_file_url']


class Hitomi:
    def __init__(self, number):
        input_url = 'https://hitomi.la/galleries/' + number + ".html"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        res = requests.get(input_url, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        link = soup.find('a')
        input_url = link.get('href')

        res = requests.get(input_url, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')

        gallery_info_ul = soup.find_all('ul', attrs={'class': "tags"})
        print(gallery_info_ul)
        character_ul = gallery_info_ul[0]
        print(character_ul)
        character_li = character_ul.find_all('li')
        tags_ul = gallery_info_ul[1]
        tags_li = tags_ul.find_all('li')
        artist_ul = soup.find("ul", attrs={'class': "comma-list"})
        artist_li = artist_ul.find_all('li')
        cover_div = soup.find('div', attrs={'class': "cover"})
        cover_img = cover_div.find('img')
        cover = "https:" + cover_img.get('src')

        type = soup.find('title').text.split('- Read Online - hentai ')[1].split(' | Hitomi.la')[0]

        if type == 'manga':
            title_div = soup.find('div', attrs={'class': "gallery manga-gallery"})
            title = title_div.find('a', attrs={'href': "/reader/" + number + ".html"}).text
        if type == 'doujinshi':
            title_div = soup.find('div', attrs={'class': "gallery dj-gallery"})
            title = title_div.find('a', attrs={'href': "/reader/" + number + ".html"}).text
        if type == 'artistcg':
            title_div = soup.find('div', attrs={'class': "gallery acg-gallery"})
            title = title_div.find('a', attrs={'href': "/reader/" + number + ".html"}).text
        artist = []
        for i in artist_li:
            artist.append(i.text)
        tags = []
        for i in tags_li:
            tags.append(i.text)
        character = []
        for i in character_li:
            character.append(i.text)

        self.number = number
        self.tags = tags
        self.title = title
        self.character = character
        self.cover = cover
        self.artist = artist
        self.type = type


class Htv:
    def __init__(self, title):
        title = title.replace(' ', '-')
        input_url = 'https://hanime.tv/videos/hentai/' + title
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        res = requests.get(input_url, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        cover_div = soup.find('div', attrs={'class': "hvpi-cover-container"})
        cover_img = cover_div.find('img')
        cover = cover_img.get('src')
        title = soup.find('h1', attrs={'class': 'tv-title'}).text
        brand = soup.find('a', attrs={'class': "hvpimbc-text"}).text
        desc = soup.find('div', attrs={'class': 'mt-3 mb-0 hvpist-description'}).text
        desc = desc.replace('\n', '')
        soup = soup.find('div', attrs={'class': "hvpi-summary"})
        tags_a = soup.find_all('a')
        tags = []
        for i in tags_a:
            tags.append(i.text)

        self.title = title
        self.desc = desc
        self.tags = tags
        self.brand = brand
        self.cover = cover

client = discord.Client()
conn = sqlite3.connect('bounties.db')

game = discord.Game("야한거")

@client.event
async def on_ready():
    print('HentaiBot Online')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(status=discord.Status.idle, activity=game)

@client.event
async def on_message(message):
    channel = message.channel
    msg = message.content

    if channel.is_nsfw() and message.author.id != client.user.id:
        # ========[ Yande.re API ]==============================
        if msg[:7].lower() == "yandre:":
            a = YandereApi(message.content[7:])
            embed = discord.Embed().set_image(url=a.file)
            await channel.send("", embed=embed)

        # ========[ Danbooru API ]==============================
        if msg[:9].lower() == "danbooru:":
            a = Danbooru(message.content[9:])
            if (a=="loli" or a=="shota"):
                temp = """
                Danbooru 에서의 Loli 및 Shota 검색은 유료서비스 입니다.\n
                Loli 혹은 Shota를 검색하려면 Gelbooru 를 이용해주시기 바랍니다.
                """
                await channel.send(temp)
            embed = discord.Embed().set_image(url=a.file)
            await channel.send("", embed=embed)

        # ========[ Gelbooru API ]==============================
        if msg[:9].lower() == "gelbooru:":
            a = Gelbooru(message.content[9:])
            embed = discord.Embed().set_image(url=a.file_url)
            await channel.send("", embed=embed)

client.run('your token')