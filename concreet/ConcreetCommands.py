from discord.ext import commands
from utils import *
import discord
import random


class ConcreetCog(commands.Cog):
    def __init__(self, bot, cfg):
        super().__init__()
        self.bot = bot
        self.cfg = cfg

    def _get_concrete_boys(self):
        return list_to_str(cfg_to_list(self.cfg['Concrete boys']['persons']))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.name in self._get_concrete_boys():
            if not before.channel and after.channel:
                names = [n for n in cfg_to_list(self.cfg['Concrete boys']['images']) if n != '']
                images = [create_image(name) for name in names]
                pick = random.choice(images)
                if type(pick) is discord.File:
                    await member.send(file=pick)
                else:
                    await member.send(embed=pick)

    @commands.command(name="concreet")
    async def concrete(self, ctx):
        names = [n for n in cfg_to_list(self.cfg['Concrete boys']['images']) if n != '']
        images = [create_image(n) for n in names]
        pick = random.choice(images)
        if type(pick) is discord.File:
            await ctx.send(file=pick)
        else:
            await ctx.send(embed=pick)