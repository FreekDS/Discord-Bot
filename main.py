import discord
import os
import random
import configparser
from discord.ext import commands
from dotenv import load_dotenv
from utils import strip_cmd, \
    cfg_to_list, \
    list_to_str, \
    update_cfg, \
    add_to_cfglist, \
    remove_from_cfglist, \
    create_image, is_url

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
guild_name = os.getenv('GUILD_NAME')

cfg = configparser.ConfigParser()
cfg.read('res/config.ini', encoding='utf-8')

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


async def show_help(channel):
    help = "This bot has the following DM commands```" \
           "!help: shows this message\n" \
           "!admin add <username>: add <username to the list of admins>\n" \
           "!admin del <username>: remove admin of the list\n" \
           "!admin show: shows the admins\n" \
           "!concreet person add <username>: add username to the list of concreet people\n" \
           "!concreet person del <username>: remove username from concreet people if it exists\n" \
           "!concreet person show: shows the users that get concreet messages\n" \
           "```"

    await channel.send(help)


def get_admins():
    return list_to_str(cfg_to_list(cfg['General']['admins']))


def get_concrete_boys(partial=False):
    if partial:
        return list_to_str(cfg_to_list(cfg['Concrete boys']['partial_persons']))
    return list_to_str(cfg_to_list(cfg['Concrete boys']['persons']))


def get_images():
    return list_to_str(cfg_to_list(cfg['Concrete boys']['images']))


async def handle_admin_cmds(channel, admin, command):
    if command.startswith('show'):
        names = get_admins()
        await channel.send("This are the current admins: ```\n{}```".format(names))
    elif command.startswith('add'):
        new_admin = strip_cmd('add', command)
        if new_admin in get_admins():
            await channel.send('This person was already in the list.')
            return
        cfg['General']['admins'] = add_to_cfglist(cfg['General']['admins'], new_admin)
        update_cfg(cfg)
        names = get_admins()
        await channel.send("This is the new list of admins: ```\n{}```".format(names))
    elif command.startswith('del'):
        to_remove = strip_cmd('del', command)
        if len(to_remove) == 0:
            await channel.send('Please specify a username to delete')
            return
        if to_remove not in get_admins():
            await channel.send("{} is no admin".format(to_remove))
            return
        if to_remove == admin.name:
            await channel.send("You cannot delete yourself as admin")
            return
        if to_remove == 'Wofke':
            await channel.send("Error 500: ___creatorNotDeleteError____  line 69 in fucku.py")
            await channel.send("Wa peist gij wel ni, clown 🤡")
            return
        cfg['General']['admins'] = remove_from_cfglist(cfg['General']['admins'], to_remove)
        update_cfg(cfg)
        names = get_admins()
        await channel.send("This is the new list of admins: ```\n{}```".format(names))
    else:
        await channel.send('Unknown option, {}'.format(command.split(' ')[0]))


async def handle_concrete_cmds(channel, author, command):
    if command.startswith('person'):
        command = strip_cmd('person', command)
        if command.startswith('add'):
            new_person = strip_cmd('add', command)
            if new_person in get_concrete_boys():
                await channel.send('This person was already in the list.')
                return
            cfg['Concrete boys']['persons'] = add_to_cfglist(cfg['Concrete boys']['persons'], new_person)
            update_cfg(cfg)
            names = get_concrete_boys()
            await channel.send("This is the new list of concrete persons ```\n{}```".format(names))
        elif command.startswith('del'):
            to_remove = strip_cmd('del', command)
            if len(to_remove) == 0:
                await channel.send('Please specify a username to delete')
                return
            if to_remove not in get_concrete_boys():
                await channel.send("{} is no concrete boy".format(to_remove))
                return
            if to_remove == 'Wofke':
                await channel.send("Error 500: ___creatorNotDeleteError____  line 69 in fucku.py")
                await channel.send("Wa peist gij wel ni, clown 🤡")
                return
            cfg['Concrete boys']['persons'] = remove_from_cfglist(cfg['Concrete boys']['persons'], to_remove)
            update_cfg(cfg)
            names = get_concrete_boys()
            await channel.send("This is the new list of concrete persons: ```\n{}```".format(names))
        elif command.startswith('show'):
            names = get_concrete_boys()
            await channel.send("These persons get concrete messages: ```\n{}```".format(names))
        else:
            await channel.send('Unknown command "{}"'.format(command))
    elif command.startswith('image'):
        command = strip_cmd('image', command)
        if command.startswith('add'):
            url = strip_cmd('add', command)
            if url in get_images():
                await channel.send("Image already exists")
                return
            if not is_url(url):
                await channel.send("Please provide a url to an image {}".format(url))
                return
            cfg['Concrete boys']['images'] = add_to_cfglist(cfg['Concrete boys']['images'], url)
            update_cfg(cfg)
            embed = create_image(url)
            embed.title = 'Image added:'
            await channel.send(embed=embed)
        else:
            pass
    else:
        await channel.send('Unknown command "{}"'.format(command))


async def dm_handler(msg, author):
    if author.name not in get_admins() or msg.system_content[0] != '!':
        await msg.channel.send('🤡🤡♿♿♿♿♿♿♿♿♿♿♿🤡🤡')
        return

    if msg.system_content.strip() == '!help':
        await show_help(msg.channel)

    if msg.system_content.startswith('!admin'):
        command = strip_cmd('!admin', msg.system_content)
        try:
            await handle_admin_cmds(msg.channel, author, command)
        except Exception as e:
            await msg.channel.send('Unknown error.... 🤡')
    elif msg.system_content.startswith('!concreet'):
        command = strip_cmd('!concreet', msg.system_content)
        try:
            await handle_concrete_cmds(msg.channel, author, command)
        except Exception as e:
            await msg.channel.send('Unknown error.... 🤡')


@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return

    if type(msg.channel) is discord.DMChannel:
        await dm_handler(msg, msg.author)
        return

    if msg.author.name != 'lord and saviour' and 'PERIDOT' not in msg.author.name:
        await bot.process_commands(msg)
        return

    await msg.add_reaction('🤡')

    if '🧇' in msg.system_content:
        await msg.add_reaction('♿')
        await msg.author.send('Niemand moet u wafels hebben, zwegt')

    # This line is required to keep responding to commands
    await bot.process_commands(msg)


@bot.event
async def on_voice_state_update(member, before, after):
    if member.name in get_concrete_boys() or member.name in get_concrete_boys(True):
        if not before.channel and after.channel:
            names = [n for n in cfg_to_list(cfg['Concrete boys']['images']) if n != '']
            images = [create_image(name) for name in names]
            await member.send(file=random.choice(images))


@bot.command(name='concreet')
async def concrete(ctx):

    names = [n for n in cfg_to_list(cfg['Concrete boys']['images']) if n != '']
    images = [create_image(n) for n in names]

    pick = random.choice(images)

    if type(pick) is discord.File:
        await ctx.send(file=pick)
    else:
        await ctx.send(embed=pick)


@bot.command(name='zwegt')
async def mute_jim(ctx):
    jim = discord.utils.get(ctx.guild.members, name='lord and saviour')
    if not jim or not jim.voice:
        await ctx.send('Jim is ons te slim af, hij is offline :(')
        return

    if jim.voice.mute:
        await ctx.send('Gelukkig zwegt em al 🤡')
        return

    await jim.edit(mute=True)
    await jim.send("Gemute, en verdiend gvd 🤡")
    await ctx.send('Zwegt')


bot.run(token)
