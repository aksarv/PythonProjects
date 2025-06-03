from discord.ext import commands
from requests import get
from bs4 import BeautifulSoup

# Replace token with actual token - not shown here
TOKEN = 'TOKEN'

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'{bot.user} has started!')
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!subscribercount '):
        await message.channel.send(f'Finding the subscriber count of **{message.content[17:]}**...')
        url = f'https://api.socialcounts.org/youtube-live-subscriber-count/search/{message.content[17:]}'
        req = get(url).content
        soup = BeautifulSoup(req, 'html.parser')
        channel_id = str(soup)[17:41]
        url2 = f'https://api.socialcounts.org/youtube-live-subscriber-count/{channel_id}'
        req2 = str(get(url2).content)
        await message.channel.send('**'+message.content[17:]+'** has **' + '{:,}'.format(int(req2[req2.index('"est_sub":')+10:req2.index(',"API_sub"')])) +'** subscribers.')
    await bot.process_commands(message)
bot.run(TOKEN)
