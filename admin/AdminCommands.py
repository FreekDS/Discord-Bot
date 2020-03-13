from utils import *


class AdminCog(commands.Cog):
    def __init__(self, bot, cfg):
        super().__init__()
        self.bot = bot
        self.cfg = cfg

    def _get_admins(self, as_list=False):
        the_list = cfg_to_list(self.cfg['General']['admins'])
        if as_list:
            return the_list
        return list_to_str(the_list)

    @staticmethod
    async def show_help(channel):
        help = "This bot has the following DM commands```" \
               "!help: shows this message\n" \
               "!admin add <username>: add <username> to the list of admins\n" \
               "!admin del <username>: remove admin of the list\n" \
               "!admin show: shows the admins\n" \
               "!concreet person add <username>: add username to the list of concreet people\n" \
               "!concreet person del <username>: remove username from concreet people if it exists\n" \
               "!concreet person show: shows the users that get concreet messages\n" \
               "!concreet image add <url>: add image to the list of images. Url must end with .png, .gif, .jpg, " \
               ".jpeg  or .bmp" \
               "```"
        await channel.send(help)

    def _get_concrete_boys(self, as_list=False):
        the_list = cfg_to_list(self.cfg['Concrete boys']['persons'])
        if as_list:
            return the_list
        return list_to_str(the_list)

    def _get_images(self):
        return list_to_str(cfg_to_list(self.cfg['Concrete boys']['images']))

    async def _proc_concrete_cmds(self, channel, author, command):
        if command.startswith('person'):
            command = strip_cmd('person', command)
            if command.startswith('add'):
                new_person = strip_cmd('add', command)
                if new_person in self._get_concrete_boys(True):
                    await channel.send('This person was already in the list.')
                    return
                self.cfg['Concrete boys']['persons'] = add_to_cfglist(self.cfg['Concrete boys']['persons'], new_person)
                update_cfg(self.cfg)
                names = self._get_concrete_boys()
                await channel.send("This is the new list of concrete persons ```\n{}```".format(names))
            elif command.startswith('del'):
                to_remove = strip_cmd('del', command)
                if len(to_remove) == 0:
                    await channel.send('Please specify a username to delete')
                    return
                if to_remove not in self._get_concrete_boys(True):
                    await channel.send("{} is no concrete boy".format(to_remove))
                    return
                if to_remove == 'Wofke':
                    await channel.send("Error 500: ___creatorNotDeleteError____  line 69 in fucku.py")
                    await channel.send("Wa peist gij wel ni, clown 🤡")
                    return
                self.cfg['Concrete boys']['persons'] = remove_from_cfglist(self.cfg['Concrete boys']['persons'],
                                                                           to_remove)
                update_cfg(self.cfg)
                names = self._get_concrete_boys()
                await channel.send("This is the new list of concrete persons: ```\n{}```".format(names))
            elif command.startswith('show'):
                names = self._get_concrete_boys()
                await channel.send("These persons get concrete messages: ```\n{}```".format(names))
            else:
                await channel.send('Unknown option "{}"'.format(command))
        elif command.startswith('image'):
            command = strip_cmd('image', command)
            if command.startswith('add'):
                url = strip_cmd('add', command)
                if url in self._get_images():
                    await channel.send("Image already exists")
                    return
                if not is_url(url):
                    await channel.send("Please provide a url to an image {}".format(url))
                    return
                self.cfg['Concrete boys']['images'] = add_to_cfglist(self.cfg['Concrete boys']['images'], url)
                update_cfg(self.cfg)
                embed = create_image(url)
                embed.title = 'Image added:'
                await channel.send(embed=embed)
            else:
                await channel.send("Unknown option '{}', use !help to view the DM commands".format(command))
        else:
            await channel.send('Unknown command "{}"'.format(command))

    async def _proc_admin_cmds(self, channel, admin, command):
        if command.startswith('show'):
            names = self._get_admins()
            await channel.send("This are the current admins: ```\n{}```".format(names))
        elif command.startswith('add'):
            new_admin = strip_cmd('add', command)
            if new_admin in self._get_admins(True):
                await channel.send('This person was already in the list.')
                return
            self.cfg['General']['admins'] = add_to_cfglist(self.cfg['General']['admins'], new_admin)
            update_cfg(self.cfg)
            names = self._get_admins()
            await channel.send("This is the new list of admins: ```\n{}```".format(names))
        elif command.startswith('del'):
            to_remove = strip_cmd('del', command)
            if len(to_remove) == 0:
                await channel.send('Please specify a username to delete')
                return
            if to_remove not in self._get_admins(True):
                await channel.send("{} is no admin".format(to_remove))
                return
            if to_remove == admin.name:
                await channel.send("You cannot delete yourself as admin")
                return
            if to_remove == 'Wofke':
                await channel.send("Error 500: ___creatorNotDeleteError____  line 69 in fucku.py")
                await channel.send("Wa peist gij wel ni, clown 🤡")
                return
            self.cfg['General']['admins'] = remove_from_cfglist(self.cfg['General']['admins'], to_remove)
            update_cfg(self.cfg)
            names = self._get_admins()
            await channel.send("This is the new list of admins: ```\n{}```".format(names))
        else:
            await channel.send('Unknown option, {}'.format(command.split(' ')[0]))

    async def _proc_dm(self, msg, author):
        if author.name not in self._get_admins(True) or msg.system_content[0] != '!':
            await msg.channel.send('🤡🤡♿♿♿♿♿♿♿♿♿♿♿🤡🤡')
            return

        if msg.system_content.strip() == '!help':
            await AdminCog.show_help(msg.channel)

        if msg.system_content.startswith('!admin'):
            command = strip_cmd('!admin', msg.system_content)
            try:
                await self._proc_admin_cmds(msg.channel, author, command)
            except Exception as e:
                await msg.channel.send('Unknown error.... 🤡')
        elif msg.system_content.startswith('!concreet'):
            command = strip_cmd('!concreet', msg.system_content)
            try:
                await self._proc_concrete_cmds(msg.channel, author, command)
            except Exception as e:
                await msg.channel.send('Unknown error.... 🤡')
        return None

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user:
            return

        if type(msg.channel) is discord.DMChannel:
            await self._proc_dm(msg, msg.author)
            return
