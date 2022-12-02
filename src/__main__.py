#!/usr/bin/python
# -*- coding: utf-8 -*-

# Native libraries
import os
import time
import asyncio

# Discord
import discord
from discord.ext import commands

# Etc.
import wolframalpha

# Custom packages
import utils.usersAudioManager as usersAudioManager
import utils.listAudioManager as listAudioManager
import utils.trashVariables as trashVariables

# Fixes warnings of unsucessfull quit at client.close()
import platform
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Uncomment to run locally
from dotenv import load_dotenv
load_dotenv(encoding='latin-1')


# Client class
class MyClient(commands.Bot):
    class Questionnaire(discord.ui.Modal):
        def __init__(
            self, on_submit_func, title='Basic Title',
            items=[{'label': 'Name', 'placeholder': 'Your name here'}]
        ):
            super().__init__(
                title=title,
            )

            self.callback_submit_func = on_submit_func

            self.items = {}
            for item in items:
                self.items[item['variableName']] = discord.ui.TextInput(
                    label=item['label'].capitalize(),
                    placeholder=item['placeholder'],
                    required=item['required'] if 'required' in item.keys()
                    else False,
                )

                self.add_item(self.items[item['variableName']])

        async def on_submit(
            self, interaction: discord.Interaction
        ):
            items = self.items.items()
            variables_values = {key: value.value for (key, value) in items}
            await self.callback_submit_func(
                author=interaction.user,
                sendWith=interaction.response.send_message,
                variables=variables_values
            )

        async def on_error(
            self, error: Exception, interaction: discord.Interaction
        ) -> None:
            import traceback
            await interaction.response.send_message(
                'Oops! Something went wrong.', ephemeral=True
            )
            traceback.print_tb(error.__traceback__)

    # Enviroment variables and auxiliary variables
    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        description = ("This bot does a lot of useless stuff."
                       "And it plays some online games.")

        super().__init__(
            command_prefix=commands.when_mentioned_or('$'),
            description=description,
            case_insensitive=True,
            intents=intents,
            help_command=None,
        )

        self.dbs = {}

        self.aux_vars = {}

        # Owner id. This person will have admin rights.
        self.aux_vars['currentOwner'] = os.environ.get('currentOwner')
        # Defines admin server. The one which slash admin commands will appear
        self.aux_vars['admin_svr_id'] = int(os.environ.get('admin_svr_id'))
        # Currency converter object.
        self.aux_vars['converter'] = None
        # Game that the bot will be playing.
        self.aux_vars['gameName'] = os.environ.get('gameName')
        # Bot name displayed.
        self.aux_vars['botName'] = os.environ.get('botName')
        # Client for wolfram alpha.
        self.aux_vars['wolfram'] = wolframalpha.Client(
            os.environ.get('wolframKey')
        )

        self.aux_vars['language_list'] = {
            'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic',
            'ar': 'arabic', 'hy': 'armenian', 'az': 'azerbaijani',
            'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali',
            'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan',
            'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese',
            'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)',
            'co': 'corsican', 'hr': 'croatian', 'cs': 'czech',
            'da': 'danish', 'nl': 'dutch', 'en': 'english',
            'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino',
            'fi': 'finnish', 'fr': 'french', 'fy': 'frisian',
            'gl': 'galician', 'ka': 'georgian', 'de': 'german',
            'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole',
            'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew',
            'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian',
            'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian',
            'ga': 'irish', 'it': 'italian', 'ja': 'japanese',
            'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh',
            'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)',
            'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian',
            'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian',
            'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam',
            'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian',
            'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian',
            'ps': 'pashto', 'fa': 'persian', 'pl': 'polish',
            'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian',
            'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic',
            'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi',
            'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian',
            'so': 'somali', 'es': 'spanish', 'su': 'sundanese',
            'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil',
            'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian',
            'ur': 'urdu', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh',
            'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu',
            'fil': 'Filipino', 'he': 'Hebrew',
        }

        dbUsr = os.environ.get('dbUsr')
        dbPss = os.environ.get('dbPss')
        dbName = os.environ.get('dbName')
        self.dbs['db_users'] = usersAudioManager.connect(dbUsr, dbPss, dbName)
        self.dbs['db_audios'] = listAudioManager.connect(dbUsr, dbPss, dbName)
        self.dbs['db_trash_var'] = trashVariables.connect(dbUsr, dbPss, dbName)

        self.aux_vars['audioInfos'] = listAudioManager.getAllInfo(
            self.dbs['db_audios']
        )

    async def setup_hook(self):
        """Loads every cog necessary"""
        await self.log(f'Initializing MainCog.')
        await self.load_extension("cogs.mainCog")
        await self.log(f'Initializing AdminCog.')
        await self.load_extension("cogs.adminCog")

    async def on_ready(self):
        horario = {time.strftime('%d/%m/%Y - %H:%M:%S')}
        stringS = ("\n_________________New session "
                   f"({horario})_________________\n")
        stringS += f"\tUser Name: {str(self.user.name)}\n"
        stringS += f"\tUser ID:{str(self.user.id)}\n"
        stringS += ("_________________________________"
                    "_________________________________")
        await self.log(stringS)

        try:
            await self.log('\tSyncing tree [GLOBAL].')
            await self.tree.sync()
        except discord.HTTPException as e:
            await self.log(f'\tCouldn\'t sync tree [GLOBAL]. {e}')
        except discord.CommandSyncFailure as e:
            await self.log(f'\tCouldn\'t sync tree [GLOBAL]. {e}')
        except discord.Forbidden as e:
            await self.log(f'Invalid permissions for tree [GLOBAL]. {e}')

        # Tries to sync tree commands for all guilds on startup
        for guild in self.guilds:
            try:
                await self.log(f'\tSyncing tree {guild.name} [{guild.id}].')
                await self.tree.sync(guild=guild)
            except discord.HTTPException:
                await self.log(
                    f'\tCouldn\'t sync tree {guild.name} [{guild.id}]'
                )
            except discord.Forbidden:
                await self.log(
                    f'Invalid permissions for tree {guild.name} [{guild.id}]'
                )

        await self.change_presence(
            activity=discord.Activity(
                name=self.aux_vars['gameName'], url="https://play.barbie.com",
                type=discord.ActivityType.streaming, start=1,
                state='Epic Gamer Moment', details='Being Toxic',
                assets={
                    'large_image': 'ow_6', 'large_text': 'Scooby Dooby Doo',
                    'small_image': 'ow_6', 'small_text': 'Scooby Dooby Doo',
                }
            )
        )
        await self.log("\tGame title set.")

        if (self.user.name != self.aux_vars['botName']):
            await self.user.edit(username=self.aux_vars['botName'])
            await self.log(f"\tBot name updated [{self.aux_vars['botName']}].")

        await self.log('\tDone!')

    async def log(self, message, printMessage=True):
        with open('log.txt', "a", encoding="utf-8") as file:
            file.write(f"[LOG]({time.strftime('%d/%m/%Y - %H:%M:%S')}): ")
            file.write(f"{message}\n")

        if (printMessage):
            try:
                print(
                    (f'[LOG]'
                     f'({time.strftime("%d/%m/%Y - %H:%M:%S")}): '
                     f'[{message}].')
                )
            except Exception as e:
                print(
                    (f'[EXCEPTION ON PRINT]'
                     f'({time.strftime("%d/%m/%Y - %H:%M:%S")}): '
                     f'[{e}].')
                )

    async def log_command_call(self, interaction, **kwargs):
        if isinstance(interaction, discord.Interaction):
            author = interaction.user
        elif isinstance(interaction, commands.Context):
            author = interaction.author

        admin = await self.validate_admin(interaction)
        admin_str = "[ADMIN]" * admin
        await self.log(
            (f"'/{interaction.command.qualified_name}'"
             f" from {admin_str}{author} ({author.id}). [{kwargs}]")
        )

        return author

    async def disconnectProperly(self, voiceClient):
        await voiceClient.disconnect()
        voiceClient.cleanup()

    def audioDisconnect(self, voiceClient):
        # Function to async disconnect from voiceClient
        coro = self.disconnectProperly(voiceClient)
        fut = asyncio.run_coroutine_threadsafe(coro, self.loop)
        fut.result()

    def checkForAudio(self, audioname, check_db, audioFolder=""):
        # Checks if audio is downloaded in bot folder
        if (not os.path.isfile(f'Audio/{audioFolder}' + audioname)):
            audio = usersAudioManager.getAudioFromDb(check_db, audioname)
            if (audio == -1):  # File not downloaded and doesn't exists in db
                return False
            else:  # Found file inside db
                usersAudioManager.convertStringToAudio(
                    audio, f'Audio/{audioFolder}', audioname
                )
                return True

        return True  # File exists

    async def validate_admin(self, interaction):
        """Checks if user can use admin commands"""
        if isinstance(interaction, discord.Interaction):
            author = interaction.user
        elif isinstance(interaction, commands.Context):
            author = interaction.author
        else:
            await self.log(
                (f'\tAsked validation of [{interaction}]'
                 f' of type [{type(interaction)}]. Unknown type denied.')
            )
            return 0

        if (str(author.id) == str(self.aux_vars['currentOwner'])):
            return 1
        return 0

    def get_channel(self, interaction):
        author = interaction.user
        if (isinstance(author, discord.User)):
            for server in self.guilds:
                for channel in server.voice_channels:
                    for member in channel.members:
                        if (member == author):
                            return channel
        elif (isinstance(author, discord.Member)):
            if (author.voice is None):
                return None
            return author.voice.channel

        return None

    # Event on_voice_state_update
    async def on_voice_state_update(self, member, before, after):
        authorFile = f'{str(member.id)}.mp3'

        if (after.channel is not None and before.channel is None):
            await self.log(
                f'{member.name} ({member.id}) entered {str(after.channel)}.'
            )

            dont_have = not self.checkForAudio(
                audioname=authorFile, check_db=self.dbs['db_users'],
                audioFolder='Users/'
            )

            if (dont_have):
                return
            await self.log(f'\tIt triggered a sound.')

            try:
                voiceClient = await after.channel.connect()
            except Exception as e:
                await self.log(f"\tRaised exception. [{e}]")
                return

            voiceClient.play(
                discord.FFmpegPCMAudio(f'Audio/Users/{authorFile}'),
                after=lambda _: self.audioDisconnect(voiceClient),
            )

            await self.log(f'\tOpening "{authorFile}".')


def main():
    client = MyClient()
    client.run(os.environ.get('token'))


if __name__ == '__main__':
    main()
