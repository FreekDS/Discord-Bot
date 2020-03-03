import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
guild_name = os.getenv('GUILD_NAME')

client = discord.Client()
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == guild_name:
            break
    else:
        guild = None
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return

    if msg.author.name != 'Wofke':
        return

    await msg.add_reaction('🤡')

    if '🧇' in msg.system_content:
        await msg.add_reaction('♿')
        await msg.author.send('Niemand moet u wafels hebben, zwegt')


bot.run(token)
