import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import random
import asyncio
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

bot = commands.Bot(command_prefix='!')


def is_me(m):
    return m.author == bot.user

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


def make_bingo(options):
    img = Image.new('RGB', (1000, 1000), color='white')
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("Roboto-Regular.ttf", 20)
    for l in range(1, 5):
        d.line(((l*200, 0), (l*200), 1000), fill='black', width=10)
        d.line(((0, l*200),  (1000, l*200)), fill='black', width=10)
    for i in range(0, 5):
        for j in range(0,5):
            if (j == 2) and (i == 2):
                tempList = "Free Space"
                tempList = tempList.split()
                temp = ""
            else:
                temp = (options.pop(random.randint(0, len(options)-1))).content
                temp.replace("'", "")
                tempList = temp.split()
                temp = ""
            for k in range(0, len(tempList)):
                if (k % 2 == 0):
                    temp += tempList[k] + "\n"
                else:
                    temp += tempList[k] + " "
            d.text(((i*200)+5, (j*200)+5), text=temp, fill='black', font=font)
    return img

@bot.command()
async def bingoBoard(ctx):
    await ctx.message.delete()
    channel = ctx.channel
    messages = await channel.history(limit=200).flatten()
    img = make_bingo(messages)
    img.save("bingo.png")
    await channel.send(file=discord.File("bingo.png"))
    await asyncio.sleep(120)
    await ctx.channel.purge(limit=1, check=is_me)

@bot.command()
async def UTCovid(ctx):
    await ctx.message.delete()
    channel = ctx.channel
    UT = requests.get('https://www.utoledo.edu/coronavirus/')
    UTsoup = BeautifulSoup(UT.text, 'html.parser')
    UTable = UTsoup.find('table')
    UTable = UTable.getText()
    UTable = UTable.split()
    UTable = UTable[15:]
    total = 0
    for i in range(0, len(UTable), 6):
        total += int(UTable[i])
    await channel.send("UToledo currently has " + str(total) + " covid-19 cases.")

@bot.command()
async def OpenNow(ctx):
    await ctx.message.delete()
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("C:/Users/rfd20/PycharmProjects/bingoMaker/venv/Lib/site-packages/selenium/webdriver/chrome", chrome_options=options)
    driver.get('https://dineoncampus.com/utoledo')
    channel = ctx.channel
    await asyncio.sleep(10)
    food = driver.page_source
    soup = BeautifulSoup(food.text, 'html.parser')
    open = soup.find_all('div', {'class' : 'row whats-open-tile_hours_8qXHw'})
    #open = open.get_text()
    await channel.send(open)

bot.run('TOKEN GO HERE')
