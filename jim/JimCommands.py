from discord.ext import commands
import discord


class JimCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jim = 'lord and saviour'

    def _get_jim_object(self, members):
        return discord.utils.get(members, name=self.jim)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user:
            return

        if msg.author.name == self.jim:
            await msg.add_reaction('🤡')

            if '🧇' in msg.system_content:
                await msg.add_reaction('♿')
                await msg.author.send('Niemand moet u wafels hebben, zwegt')
                return
            if 'kaars' in msg.system_content:
                await msg.add_reaction('♿')
                await msg.author.send('Niemand moet u kaarsen hebben, zwegt')
                return

    @commands.command(name="zwegt")
    async def mute_jim(self, ctx):
        jim = self._get_jim_object(ctx.guild.members)
        if not jim or not jim.voice:
            await ctx.send("Jim is ons te slim af, hij is offline ☹")
            return

        if jim.voice.mute:
            await ctx.send('Gelukkig zwegt em al 🤡')
            return

        await jim.edit(mute=True)
        await jim.send("Gemute, en verdiend gvd 🤡")
        await ctx.send('Zwegt')

    @commands.command(name="sprekt")
    async def unmute_jim(self, ctx):
        jim = self._get_jim_object(ctx.guild.members)
        if not jim or not jim.voice:
            await ctx.send("Jim is ni online, jammer he, hehe")
            return

        if ctx.author.name == self.jim:
            await ctx.author.send("Nice try, but no")
            return

        if not jim.voice.mute:
            await ctx.send("IEMAND besloot om hem te unmuten... Why tho")
            return

        await jim.edit(mute=False)
        await jim.send("Gelukkig dat den {} u unmute, tis goe voor ene keer...".format(ctx.author.mention))
