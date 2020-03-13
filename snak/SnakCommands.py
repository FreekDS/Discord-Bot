import discord
from discord.ext import commands
from snak.SnakBase import SnakBase, DIRECTIONS
import asyncio
import time


class SnakCog(commands.Cog, SnakBase):
    def __init__(self, bot):
        super(SnakCog, self).__init__(width=19, height=19)
        self.bot = bot
        self._playing = False
        self._game_msg = None
        self._playerObject = None
        self._headEmoji = None
        self._last_update = None
        self._start = None
        self._antispam = list()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user or reaction.message.id != self._game_msg.id:
            return

        if user != self._playerObject or not self._playing:
            await reaction.message.remove_reaction(reaction, user)
            return

        self._last_update = time.time()

        # TODO move second check to SNAK library
        if reaction.emoji == '⏪' and not self._is_horizontal(self.direction):
            self.update_direction(DIRECTIONS["LEFT"])
        elif reaction.emoji == '⏩' and not self._is_horizontal(self.direction):
            self.update_direction(DIRECTIONS["RIGHT"])
        elif reaction.emoji == '⏫' and not self._is_vertical(self.direction):
            self.update_direction(DIRECTIONS["UP"])
        elif reaction.emoji == '⏬' and not self._is_vertical(self.direction):
            self.update_direction(DIRECTIONS["DOWN"])

        await reaction.message.remove_reaction(reaction, user)

    @commands.command(name='snak')
    async def play(self, ctx, arg=None, head=None):
        if arg is None:
            await ctx.send("Use arguments you dumbass")
            return

        if arg.lower() == 'play':
            if self._playing is True:
                self._antispam.append(
                    await ctx.send("{} is already playing, wait for your turn".format(self._playerObject.name)))
                self._playing = False
                return
            self._antispam.append(ctx.message)
            self._headEmoji = None
            if head:
                self._headEmoji = head
            self._playerObject = ctx.author
            embed = discord.Embed(description="Booting Snak...")
            self._game_msg = await ctx.send(embed=embed)
            await self._game_msg.add_reaction('⏪')
            await self._game_msg.add_reaction('⏩')
            await self._game_msg.add_reaction('⏫')
            await self._game_msg.add_reaction('⏬')
            self.bot.loop.create_task(self._run_game())
            self._playing = True
            self._last_update = time.time()
        elif arg.lower() == 'stop':
            if self._playing:
                self._playing = False
        else:
            self._antispam.append(
                await ctx.send("Unknown argument: '{}'\nuse either 'play' or 'stop' as argument".format(arg)))

    def __str__(self):
        res = '  '
        for i in range(self.width): res += '──'
        res += '\n'
        for y in range(self.height):
            for x in range(self.width):
                if x == 0:
                    res += '│ '
                if (x, y) == self._head:
                    if not self._headEmoji:
                        res += '🟢'
                    else:
                        res += self._headEmoji
                elif (x, y) in self.player:
                    if (x, y) in self._eat_locations:
                        res += '🟩'
                    else:
                        res += '🟢'
                elif (x, y) == self.fruit:
                    res += '🍎'
                else:
                    res += '∘∘∘'
                if x == self.width - 1:
                    res += '\t│ '
            res += '\n'
        res += '  '
        for i in range(self.width): res += '──'
        res += '\n'
        return res

    def reset(self):
        super().reset()
        self._game_msg = None
        self._playing = False
        self._last_update = None
        self.game_over = False
        self._playerObject = None
        self._headEmoji = None

    async def _run_game(self):
        await self.bot.wait_until_ready()
        self.update()
        while not self.bot.is_closed() and self._playing:
            embed = discord.Embed(description=str(self), title="SNAK THE GEEM")
            await self._game_msg.edit(embed=embed)
            self.update()
            if self.game_over:
                break
            await asyncio.sleep(1.1)

            if self._last_update:
                if time.time() - self._last_update > 120:
                    break

        embed = discord.Embed(
            title="Snak the geem",
            description="{} played snak and scored {} points! use '!snak play' to play".format(
                self._playerObject.mention,
                self.score
            )
        )

        await self._game_msg.channel.send(embed=embed)

        # Cleanup the messages
        await self._game_msg.delete()
        for msg in self._antispam:
            await msg.delete()
            self._antispam.remove(msg)

        self.reset()
