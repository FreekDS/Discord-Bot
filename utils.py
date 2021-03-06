import re
from discord import File, Embed
from discord.ext import commands
import discord
from functools import wraps

URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)'
    r'*(.png|.bmp|.gif|.jp(e)?g)$'

    , re.IGNORECASE)


def strip_cmd(to_strip, cmd):
    return cmd.replace(to_strip, '').strip()


def cfg_to_list(cfg, sep=','):
    return [item.strip() for item in cfg.split(sep)]


def list_to_str(l, sep='\n'):
    res = str()
    for i in l:
        res = res + str(i) + sep
    return res[:-len(sep)]


def add_to_cfglist(entry, new_val, sep='\n'):
    return entry + sep + new_val + ','


def _build_cfg_str(the_list, line='\n', sep=','):
    res = '\n'
    for i in the_list:
        if i is None or str(i) == '':
            continue
        res += str(i) + sep + line
    return res[:-1]


def remove_from_cfglist(entry, to_remove):
    lst = cfg_to_list(entry)
    lst.remove(to_remove)
    return _build_cfg_str(lst)


def update_cfg(cfg):
    with open('res/config.ini', 'w', encoding='utf-8') as file:
        cfg.write(file)


def is_url(string):
    return re.match(URL_REGEX, string) is not None


async def not_dm(*args, **kwargs):
    msg = [x for x in args if isinstance(x, discord.Message)]
    if len(msg) != 0:
        return msg[0].channel is discord.DMChannel

    msg = [x for x in [*kwargs.values()] if isinstance(x, discord.Message)]
    if len(msg) != 0:
        return msg[0].channel is discord.DMChannel

    ctx = [x for x in args if isinstance(x, commands.Context)]
    if len(ctx) != 0:
        f = ctx[0].channel is not discord.DMChannel
        return not isinstance(ctx[0].channel, discord.DMChannel)

    ctx = [x for x in [*kwargs.values()] if isinstance(x, commands.Context)]
    if len(ctx) != 0:
        return ctx[0].channel is discord.DMChannel


def create_image(n):
    if is_url(n):
        embed = Embed()
        embed.set_image(url=n.strip())
        return embed
    else:
        return File(n.strip())
