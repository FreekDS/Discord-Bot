from dotenv import load_dotenv
import os
import configparser
from discord.ext import commands

cfg = configparser.ConfigParser()
cfg.read('res/config.ini', encoding='utf-8')

bot = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
    print('We have logged in as {0.user} on {1} guild(s)'.format(bot, len(bot.guilds)))


def register_cogs():
    from admin.AdminCommands import AdminCog
    from jim.JimCommands import JimCog
    from concreet.ConcreetCommands import ConcreetCog
    from snak.SnakCommands import SnakCog
    bot.add_cog(ConcreetCog(bot, cfg))
    bot.add_cog(JimCog(bot))
    bot.add_cog(AdminCog(bot, cfg))
    bot.add_cog(SnakCog(bot))


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv("TEST_TOKEN")
    register_cogs()
    bot.run(token)