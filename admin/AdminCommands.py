from discord.ext import commands


class AdminCog(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user:
            return

        print("Listener on {}".format("AdminCog"))
