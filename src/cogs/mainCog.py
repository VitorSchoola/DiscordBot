# Native imports
import os
import shutil
import re
import random
import requests
import datetime
import math
from typing import Optional
import asyncio

# Discord
import discord
from discord.ext import commands

# Image imports
import PIL.Image
from PIL import ImageFont
from PIL import ImageDraw

# Audio Imports
from pydub import AudioSegment
from gtts import gTTS

# Etc.
from thefuzz import fuzz

from googletrans import Translator

from emoji import is_emoji

# Custom libs
import utils.getCurrency as getCurrency
import utils.getWiki as getWiki
import utils.Img2Ascii as Img2Ascii
import utils.trashVariables as trashVariables
import utils.listAudioManager as listAudioManager
import utils.usersAudioManager as usersAudioManager


class MainCog(commands.Cog, name='Commands', command_attrs=dict(hidden=False)):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def handle_link(
        self, link: str,
        max_mb: int = 1, list_extensions=[],
        img=True, default_name_file=None,
    ):
        # Check if a link was sent
        if ((link is None) or (link == '')):
            return (-2, 'No file found at link', None)

        # Get file name from link if none was provided
        r = requests.get(link)
        if default_name_file:
            nomeArq = default_name_file
        else:
            try:
                if ('content-disposition' in r.headers.keys()):
                    d = r.headers['content-disposition']
                    nomeArq = re.findall("filename=(.+)", d)[0]
                else:
                    nomeArq = link.split("/")[-1]
            except:
                return (-1, f'Couldnt resolve filetype', None)

        # Checks if file is less than max_mb MB
        length = int(r.headers.get('Content-Length', 0))
        if length > max_mb * 1024 * 1024:
            return (-3, f'File is larger than {max_mb}', None)

        # Saves to auxiliary folder
        if img:
            nomeArq = f'Img/Img_aux/{nomeArq}'
        else:
            nomeArq = f'Audio/Audio_aux/{nomeArq}'

        # Downloads file
        try:
            # Write request to a file
            with open(nomeArq, 'wb') as f:
                f.write(r.content)
        except Exception as e:
            return (-4, f'I couldn\'t save the file. [{e}]', None)

        if (nomeArq.split('.')[-1] not in list_extensions):
            os.remove(nomeArq)
            return (-5, 'Invalid file extension.', None)

        return (0, 'OK', nomeArq)

    # Image aux functions
    def wrap_text(self, text, width, font, maxLines=4):
        text_lines = []
        text_line = []
        lines = text.splitlines()

        words = []
        for line in lines:
            wordsL = line.split()
            for word in wordsL:
                words.append(word)
            words.append('\n')

        for word in words:
            text_line.append(word)
            _, _, w, _ = font.getbbox(' '.join(text_line))
            if w > width or word == '\n':
                text_line.pop()
                text_lines.append(' '.join(text_line))
                text_line = [word]

        if len(text_line) > 0:
            text_lines.append(' '.join(text_line))

        if (len(text_lines) > maxLines):
            text_lines = text_lines[0:maxLines]

        return text_lines

    def createImage(self, imagePath, message1, fontSize1):
        # Creates Animal Crossing meme
        img = PIL.Image.open(imagePath)
        draw = ImageDraw.Draw(img)
        width, height = img.size

        msg1 = message1

        myFont1 = ImageFont.truetype("Img/Img_in/ACFont.otf", fontSize1)
        myFont2 = ImageFont.truetype("Img/Img_in/emojis.otf", fontSize1)
        myFont3 = ImageFont.truetype("Img/Img_in/arial.ttf", fontSize1)

        lines = self.wrap_text(msg1, 1069, myFont1)

        nice_words = [
            'muit', 'grand', 'gigant', 'fantást',
            'fantast', 'admir', 'fenom', 'extra',
            'divin', 'estupe', 'deslum',
            'magnífic', 'magnific', 'fabulo',
        ]

        y_text = 708
        for line in lines:
            (_, _, wl, hl) = myFont1.getbbox(line)
            curW = 425
            for word in line.split():
                number = random.randrange(0, 100, 1)
                if any(x in word.lower() for x in nice_words):
                    number = 0
                for letter in word:
                    if (is_emoji(letter)):
                        draw.text(
                            (curW, y_text), letter,
                            font=myFont2, fill=(140, 112, 0)
                        )
                        curW += myFont2.getbbox(letter)[2]
                    elif (letter == '.'):
                        draw.text(
                            (curW, y_text), letter,
                            font=myFont3, fill=(135, 119, 93)
                        )
                        curW += myFont3.getbbox(letter)[2]
                    else:
                        if (
                            letter not in [',', '!', '.', ';', '?']
                            and number <= 13
                        ):
                            draw.text(
                                (curW, y_text), letter,
                                font=myFont1, fill=(1, 184, 200)
                            )
                        else:
                            draw.text(
                                (curW, y_text), letter,
                                font=myFont1, fill=(135, 119, 93)
                            )
                        curW += myFont1.getbbox(letter)[2]
                curW += myFont1.getbbox(' ')[2]
            y_text += hl

        img.save('Img/Img_aux/Meme-out.jpg')
        return 'Img/Img_aux/Meme-out.jpg'

    def createImage2(self, imagePath, message1, fontSize1):
        # Creates Dota+ meme
        img = PIL.Image.open(imagePath)
        draw = ImageDraw.Draw(img)
        width, height = img.size

        msg1 = message1

        myFont1 = ImageFont.truetype("Img/Img_in/Doto.otf", fontSize1)
        myFont2 = ImageFont.truetype("Img/Img_in/emojis.otf", fontSize1)
        myFont3 = ImageFont.truetype("Img/Img_in/arial.ttf", fontSize1)

        lines = self.wrap_text(msg1, 426, myFont1, 9)

        y_text = 220
        for line in lines:
            _, _, wl, hl = myFont1.getbbox(line)
            curW = 35
            for word in line.split():
                for letter in word:
                    if (is_emoji(letter)):
                        draw.text(
                            (curW, y_text), letter,
                            font=myFont2, fill=(140, 112, 0)
                        )
                        curW += myFont2.getbbox(letter)[2]
                    elif (letter == '.'):
                        draw.text(
                            (curW, y_text), letter,
                            font=myFont3, fill=(135, 119, 93)
                        )
                        curW += myFont3.getbbox(letter)[2]
                    else:
                        draw.text(
                            (curW, y_text), letter,
                            font=myFont1, fill=(135 + 50, 119 + 50, 93 + 50)
                        )
                        curW += myFont1.getbbox(letter)[2]
                curW += myFont1.getbbox(' ')[2]
            y_text += hl

        img.save('Img/Img_aux/Meme-out.jpg')
        return 'Img/Img_aux/Meme-out.jpg'

    # Audio aux functions
    def changePitchSeg(self, sound, speed=1.0):
        alt_sound = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * speed)
        })

        return alt_sound.set_frame_rate(sound.frame_rate)

    def changePitch(self, inFile, outFile, pitchchange):
        if (inFile[-4:] == '.mp3'):
            sound = AudioSegment.from_mp3(inFile)
        else:
            sound = AudioSegment.from_ogg(inFile)

        new_sample_rate = int(sound.frame_rate * (2.0 ** float(pitchchange)))
        hipitch_sound = sound._spawn(
            sound.raw_data, overrides={'frame_rate': new_sample_rate}
        )
        hipitch_sound = hipitch_sound.set_frame_rate(44100)

        if (hipitch_sound.duration_seconds > 10):
            self.log('\tCropped due to audio being too long.')
        hipitch_sound[:10000].export(outFile, format="mp3")

    def applyWacky(self, inFile, outFile):
        audio = AudioSegment.from_mp3(inFile)

        newAudio = AudioSegment.from_mp3("Audio/Audio_in/Effects/silence.mp3")
        newAudio = newAudio[:10]

        for j in range(0, int(audio.duration_seconds * 2000), 10):
            newAudio += self.changePitchSeg(
                audio[j:j + 10], 1.15 + 0.25 * math.sin(j / (20 * math.pi))
            )

        newAudio.export(outFile, format="mp3")

    def applyReverse(self, inFile, outFile):
        sound = AudioSegment.from_mp3(inFile)
        sound = sound.reverse()
        sound.export(outFile, format="mp3")

    def authAudio(self, originalFile, fileName, limit, max_secs=5):
        # Authenticator for audio files.
        # Makes audio hame a max of limit db and not more than max_secs seconds

        try:  # Invalid name or invalid audio
            song = AudioSegment.from_file(originalFile)
        except Exception as e:  # Low to no documentation
            e
            return -1

        # Invalid duration
        if (song.duration_seconds > max_secs):
            return -2

        songDif = song.dBFS + limit
        song = song - songDif
        song.export(str(fileName), format="mp3")
        print('Done')
        return 0

    async def process_audio(
        self, interaction: discord.Interaction,
        path_file: str,
        pitch_change: float, wacky: bool, reverse: bool,
    ) -> int:
        # Pitch change
        if (pitch_change != 0):
            pitch_change = float(pitch_change) * 0.1
            if (pitch_change < -1) or (pitch_change > 1):
                await interaction.followup.send(
                    ("Invalid pitch number. \n"
                     "```Use numbers between -10 and 10 for <pitch_change>```")
                )
                await self.client.log("\tInvalid pitch number.")
                return -1

            self.changePitch(
                path_file,
                path_file,
                pitch_change,
            )

        # Wacky effect
        if wacky:
            self.applyWacky(
                path_file,
                path_file,
            )

        # Reverse effect
        if reverse:
            self.applyReverse(
                path_file,
                path_file,
            )

        return 0

    async def playAudio(self, channel, file):
        """- Plays audio from path <file> into the <channel>;"""
        if (channel is not None):
            source = discord.FFmpegOpusAudio(file)
            source.read() # This will take some seconds

            try:
                voiceClient = await channel.connect(timeout=5)
            except Exception as e:
                await self.client.log(
                    f"\tUnexpected error connecting to channel: [{e}]."
                )
                return

            await self.client.log(f'\tPlaying "{file}" inside channel.')
            voiceClient.play(source)
            await self.client.audioDisconnect(voiceClient)
            return voiceClient
        else:
            await self.client.log(f"\tNo channel provided to connect.")
            return

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        """A cog Error Handler for our commands."""

        # We don't need to track if the command was not found
        # The person could be typing currency amount ($10)
        if (isinstance(error, discord.ext.commands.errors.CommandNotFound)):
            return

        if (isinstance(error, commands.errors.BadArgument)
                or isinstance(error, commands.errors.MissingRequiredArgument)
                or isinstance(error, commands.errors.DisabledCommand)
                or isinstance(error, commands.errors.NoPrivateMessage)):
            err_msg = (
                f'```{error}```'
                f'**Usage**:```${ctx.command.name} {ctx.command.help}```'
            )
            log_msg = (
                f'{ctx.author} ({ctx.author.id}) on command '
                f'{ctx.command.name}: {error}'
            )

        if isinstance(error, commands.errors.BadArgument):
            await ctx.message.reply(
                f'Sorry! I got the following error: {err_msg}'
            )
            await self.client.log(
                f'[ERROR] I got the following error for user {log_msg}'
            )

        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.reply(
                f'Sorry! There was a missing argument: {err_msg}'
            )
            await self.client.log(
                f'[ERROR] There was a missing argument for user {log_msg}'
            )

        elif isinstance(error, commands.errors.DisabledCommand):
            await ctx.message.reply(
                f'Sorry! This command is disabled.'
            )
            await self.client.log(
                f'[ERROR] Disabled command by {log_msg}'
            )

        elif isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.author.send(
                f'Sorry! {ctx.command} can not be used in Private Messages.'
            )
            await self.client.log(
                f'[ERROR] Command not usable in PMs by {log_msg}'
            )

        else:
            await self.client.log(
                (f'\tIgnoring exception on command {ctx.command}. '
                 f'The type of the error is {type(error)}. '
                 f'Error message: {error}')
            )

    def parse_s(self, group_obj, com):
        aux_s = ''

        if isinstance(com, discord.app_commands.Group):
            aux_s += '\t🔹'
        elif isinstance(com, discord.app_commands.Command):
            aux_s += '\t▫️'

        if (group_obj != com):
            aux_s += f" /{group_obj.name} {com.name} "
        else:
            aux_s += f" /{group_obj.name} "
        if isinstance(com, discord.app_commands.Command):
            for parameter in com.parameters:
                if parameter.required:
                    aux_s += f'<{parameter.display_name}> '
                else:
                    aux_s += f'[{parameter.display_name}] '
        aux_s += f"- {com.description}\n"
        return aux_s

    async def how_to_use_group(
        self, interaction: discord.Interaction,
        group_obj,
    ):
        author = interaction.user

        await self.client.log(
            f'\tShowing help of /{group_obj.name} for {author} ({author.id}).',
        )

        cog_commands = group_obj.commands

        shown_commands = [
            command for command in cog_commands
            if (command.guild_only is False)
        ]

        embeds = []

        title = f"How to use /{group_obj.name} 🤌"
        s = ''
        if (shown_commands != []):
            for com in shown_commands:
                s += self.parse_s(group_obj, com)

        if s != '':
            embeds.append(
                discord.Embed(
                    type='rich', title=title,
                    colour=0xFF9978, description=s,
                )
            )

        if (str(author.id) == str(self.client.aux_vars['currentOwner'])):
            hidden_commands = [
                command for command in cog_commands
                if (command.guild_only is True)
            ]
            title = f"\n*How to use hidden /{group_obj.name}* 🤌"
            s = ''
            if (hidden_commands != []):
                for com in hidden_commands:
                    s += self.parse_s(group_obj, com)

            if s != '':
                embeds.append(
                    discord.Embed(
                        type='rich', title=title,
                        colour=0xFF9978, description=s,
                    )
                )

        if len(embeds) != 0:
            await interaction.followup.send(
                embeds=embeds, ephemeral=True
            )
        else:
            await interaction.followup.send(
                'Nothing found', ephemeral=True
            )

    # STANDALONE COMMANDS #

    @discord.app_commands.command(
        name='help',
        description='Shows help documentation of commands',
    )
    @discord.app_commands.describe(
        command_name='Filter command or group',
        hidden='Show the results only for you',
    )
    async def help_func(
        self, interaction: discord.Interaction,
        command_name: Optional[str] = '',
        hidden: Optional[bool] = True,
    ):
        await self.client.log_command_call(
            interaction, command_name=command_name,
        )
        await interaction.response.defer(ephemeral=hidden, thinking=True)

        # Access validations
        validated_admin = await self.client.validate_admin(interaction)

        embeds = []

        all_commands = self.get_app_commands()
        shown_commands = [
            command for command in all_commands
            if (command_name.lower() in command.name.lower())
        ]

        # If there is only one result, and it's a group
        # Show group help
        if (
            len(shown_commands) == 1
            and isinstance(shown_commands[0], discord.app_commands.Group)
        ):
            await self.client.log(
                f"\tOne result found and Group instance."
            )
            await self.how_to_use_group(
                interaction, shown_commands[0],
            )
            return

        if len(shown_commands) > 0:
            s = 'To show help documentation of a group of commands[🔹]:\n'
            s += 'Type /help <Group>. (Example "/help audio")\n\n'
            s += 'In commands [▫]:\n'
            s += 'Variables with <> are required.\n'
            s += 'Variables with [] are optional.\n'
            for command in shown_commands:
                s += self.parse_s(command, command)

            botName = self.client.aux_vars['botName']
            title = (f"⁉️ Hello! I'm {botName}™."
                     f" You can use the following commands: ⁉️")
            if command_name != '':
                title += f" [🔎 {command_name}]"
            embed = discord.Embed(
                type='rich', title=title,
                colour=0x9978FF, description=s,
            )
            embeds.append(embed)

        # Admin commands
        if (validated_admin):
            admin_cog = self.client.get_cog('AdminCog')
            if admin_cog:
                admin_commands = admin_cog.get_app_commands()
                admin_commands = [
                    com for com in admin_commands
                    if (command_name.lower() in com.name.lower())
                ]

                # Show group help
                if (
                    len(admin_commands) == 1
                    and isinstance(
                        admin_commands[0], discord.app_commands.Group
                    )
                    and embeds == []
                ):
                    await self.client.log(
                        f"\tOne result found and Group instance."
                    )
                    await self.how_to_use_group(
                        interaction, admin_commands[0],
                    )
                    return

                if len(admin_commands) > 0:
                    server_id = self.client.aux_vars['admin_svr_id']
                    guild = self.client.get_guild(server_id)
                    s = ''
                    s += f"❕Use commands at [{guild.name}]❕\n\n"
                    for command in admin_commands:
                        if (command_name.lower() in command.name.lower()):
                            s += self.parse_s(command, command)
                    title = '😎 Admin commands: 😎'
                    if command_name != '':
                        title += f" [🔎 {command_name}]"
                    embed = discord.Embed(
                        type='rich', title=title,
                        colour=0xAA89FF, description=s,
                    )
                    embeds.append(embed)
                else:
                    embeds.append(embed=discord.Embed(
                                  type='rich', title='No admin cog',
                                  colour=0xAA89FF, description=''))

        if len(embeds) != 0:
            await interaction.followup.send(
                embeds=embeds, ephemeral=hidden,
            )
        else:
            await interaction.followup.send(
                'No command found', ephemeral=True,
            )
            await self.client.log(
                f"\tNo command found"
            )

    @discord.app_commands.command(
        name='ping',
        description=('Shows how much time the bot takes to get '
                     'an answer from the server in milliseconds'),
    )
    @discord.app_commands.describe(
        message='Message to check if bot is receiving your text correctly',
        hidden='Show the results only for you',
    )
    async def ping_func(
        self, interaction: discord.Interaction, message: str = '',
        hidden: Optional[bool] = True,
    ):
        author = await self.client.log_command_call(
            interaction, message=message
        )
        await interaction.response.defer(ephemeral=hidden, thinking=True)

        ping = self.client.latency

        await interaction.followup.send(
            content=(f'Hey, <@!{str(author.id)}>\n'
                     f'Pong! [{str(ping*1000)}ms]\n'
                     f'You wrote: {str(message)}'),
            ephemeral=hidden,
        )
        await self.client.log("\tPong!.")

    @discord.app_commands.command(
        name='imagefy',
        description='Transforms the image into ascii art',
    )
    @discord.app_commands.describe(
        attach='Image attachment',
        link='Link to image',
        hidden='Show the results only for you',
    )
    async def ascii_imagefy_func(
        self, interaction: discord.Interaction,
        attach: Optional[discord.Attachment] = None,
        link: Optional[str] = None,
        hidden: Optional[bool] = True,
    ):
        await self.client.log_command_call(interaction)
        await interaction.response.defer(ephemeral=hidden, thinking=True)

        if attach:
            selected_url = attach.url
            default_name_file = attach.filename
            file_type = attach.content_type
        elif link:
            selected_url = link
            default_name_file = None
            file_type = None
        else:
            await interaction.followup.send(
                content='No image received.',
                ephemeral=True,
            )
            await self.client.log('\tNo image received.')
            return

        # Download of file
        list_extensions = ['png', 'jpg', 'gif', 'jpeg', 'tiff']
        try:
            (errorCode, errorMess, nomeArq) = self.handle_link(
                selected_url, max_mb=5, default_name_file=default_name_file, list_extensions=list_extensions,
            )
        except Exception as e:
            await interaction.followup.send(
                content=f'Couldn\'t handle file. 😔 [{e}]',
                ephemeral=True,
            )
        if (errorCode != 0):  # Returned error
            await interaction.followup.send(
                content=errorMess,
                ephemeral=True,
            )
            await self.client.log(f'{errorMess}')
            return

        # Obtem as linhas ASCII art da imagem
        lines = Img2Ascii.ImgToAscii(nomeArq)

        await interaction.followup.send(
            f"||{lines[0]}||"
        )

        await self.client.log("\tDone.")

        if os.path.exists(nomeArq):
            os.remove(nomeArq)

    @discord.app_commands.command(
        name='roll',
        description='Gets a random integer between <a> and [b].',
    )
    @discord.app_commands.describe(
        a='First number',
        b='Second number',
        hidden='Show the results only for you',
    )
    async def roll_func(
        self, interaction: discord.Interaction,
        a: int, b: Optional[int] = 0,
        hidden: Optional[bool] = False,
    ):
        """<a> [b] - Gets a random integer between <a> and [b];
         if b is not given, it's set as 0;"""
        author = await self.client.log_command_call(interaction, a=a, b=b)
        await interaction.response.defer(ephemeral=hidden, thinking=True)

        smaller = min(a, b)
        bigger = max(a, b)

        random.seed()
        try:
            aleatorio = random.randint(smaller, bigger)
        except Exception as e:
            await interaction.followup.send("Invalid numbers to roll.")
            await self.client.log(f"\tRoll raised exception. [{e}]")
            return

        await interaction.followup.send(
            f"{author} rolled {aleatorio}. 🎲 (Range was {smaller}~{bigger})",
            ephemeral=hidden,
        )
        await self.client.log(f"\tRolled {aleatorio}. ({smaller}~{bigger})")

    @discord.app_commands.command(
        name='loro',
        description='AI LORO!',
    )
    @discord.app_commands.describe(
    )
    async def loro_func(
        self, interaction: discord.Interaction,
    ):
        """- O prato é caro, loro;"""
        await self.client.log_command_call(interaction)
        await interaction.response.defer(ephemeral=False, thinking=True)

        embed = discord.Embed(
            type='rich',
            title="AI LORO",
            colour=0xCF3928,
            description='',
        )

        embed.set_image(url='https://i.imgur.com/GNQjcxE.png')

        await interaction.followup.send(
            embed=embed, ephemeral=False,
        )
        await self.client.log(f"\tDone.")

    @discord.app_commands.command(
        name='wolfram',
        description='Asks wolfram a question',
    )
    @discord.app_commands.describe(
        question='What do you want to ask?',
        hidden='Show the results only for you',
    )
    async def wolfram_func(
        self, interaction: discord.Interaction,
        question: str,
        hidden: Optional[bool] = False,
    ):
        """<question> - Asks wolfram your question;"""
        await self.client.log_command_call(interaction, question=question)
        await interaction.response.defer(ephemeral=hidden, thinking=True)

        try:
            res = self.client.aux_vars['wolfram'].query(question)
            answer = next(res.results).text
            await interaction.followup.send(answer)
            await self.client.log(f"'\tQuery [{question}] returned [{answer}]")
        except Exception as e:
            await interaction.followup.send(
                "I wasn't able to complete your request.",
            )
            await self.client.log(
                f"\tI wasn't able to complete the request. [{e}]"
            )

    # IMAGE STANDALONE COMMANDS #
    @discord.app_commands.command(
        name='dota',
        description='Creates a Dota+ hot tip! [Gaben]',
    )
    @discord.app_commands.describe(
        message='Hot tip content',
        hidden='Show the results only for you',
    )
    async def dota_func(
        self, interaction: discord.Interaction,
        message: str,
        hidden: Optional[bool] = False,
    ):
        """\"<message>\" - Creates a Dota+ hot tip;"""
        await self.client.log_command_call(interaction, message=message)
        await interaction.response.defer(ephemeral=hidden, thinking=True)

        await self.client.log(f'\tMessage: [{message}]')

        newImage = self.createImage2(
            'Img/Img_in/DOTAPLUS.jpg', message, 25,
        )
        with open(newImage, 'rb') as fp:
            file = discord.File(fp, filename='virus_cavalodetroia.png')
            await interaction.followup.send(
                file=file, ephemeral=hidden,
            )

        await self.client.log(f'\tDota image sent to user.')
        return

    @discord.app_commands.command(
        name='meme',
        description='Creates an Animal Crossing meme 🌱',
    )
    @discord.app_commands.describe(
        message='Text inside chat box',
        hidden='Show the results only for you',
    )
    async def meme_func(
        self, interaction: discord.Interaction,
        message: str,
        hidden: Optional[bool] = False,
    ):
        await self.client.log_command_call(interaction, message=message)
        await interaction.response.defer(ephemeral=hidden, thinking=True)

        await self.client.log(f'\tMessage: [{message}]')

        total_images = len(
            [
                file for file in os.listdir('Img/Img_in/')
                if file.startswith('base')
            ]
        )
        random_idx = random.randrange(1, total_images, 1)
        newImage = self.createImage(
            f'Img/Img_in/base{random_idx}.jpg', message, 52
        )
        with open(newImage, 'rb') as fp:
            file = discord.File(fp, filename='virus_destroi_compiuter.png')
            await interaction.followup.send(
                file=file, ephemeral=hidden,
            )

        await self.client.log(f'\tMeme image sent to user.')
        return 0

    @discord.app_commands.command(
        name='wiki',
        description='Searches the term in wikipedia',
    )
    @discord.app_commands.describe(
        term='Term to search wikipedia',
        simple='Search in simplified wikipedia',
        hidden='Show the results only for you',
    )
    async def wiki_func(
        self, interaction: discord.Interaction,
        term: str,
        simple: Optional[bool] = False,
        hidden: Optional[bool] = False,
    ):
        await self.client.log_command_call(
            interaction, term=term, simple=simple
        )
        await interaction.response.defer(ephemeral=hidden, thinking=True)

        if (term == ""):
            await interaction.followup.send(
                "Empty term.", ephemeral=True
            )
            await self.client.log(f"\tEmpty term.")
            return

        if simple:
            (content, img, page) = getWiki.getWikiSimple(term, 5)
        else:
            (content, img, page) = getWiki.getWiki(term, 5)
        if (content == -1):
            await interaction.followup.send(
                "I didn't find any page. Sorry. 🥲",
            )
            await self.client.log(f"\tNo page found. Query:[{term}].")
            return

        mess = f'**Content:** {str(content)}'
        mess += f"**Link**: [<Click here>]({str(page.url)})"
        embed = discord.Embed(
            type='rich',
            title=(f"🌍 {simple*'[SIMPLE]'}"
                   f" {page.title} 🌎"),
            colour=0xCF3928, description=mess,
        )
        if (img is not None):
            embed.set_image(url=img)

        await interaction.followup.send(
            embed=embed,
        )
        await self.client.log(
            (f"\tInfo shown for {simple*'[SIMPLE]'} {page.title}."
             f" Query was {term}."),
        )

    # DOG GROUP #
    dog_group = discord.app_commands.Group(
        name='dog',
        description=('Shows a doggo of selected breed'
                     ' or a random one if breed is not specified.'),
    )

    @dog_group.command(
        name='list',
        description='See all possible dog breeds.',
    )
    async def dog_list(
        self, interaction: discord.Interaction,
    ):
        await self.client.log_command_call(interaction)
        await interaction.response.defer(ephemeral=True, thinking=True)

        urlBreeds = 'https://dog.ceo/api/breeds/list/all'
        dataBreeds = requests.get(urlBreeds).json()

        # Show all breeds
        s = ''
        for item in dataBreeds['message']:
            s += f'- {item.capitalize()}\n'
        embed = discord.Embed(
            type='rich',
            title='🐶 List of dog breeds: 🐕',
            colour=0xFF0596, description=s,
        )

        await interaction.followup.send(
            embed=embed, ephemeral=True,
        )
        await self.client.log("\tDog list shown.")
        return

    @dog_group.command(
        name='search',
        description=('Shows a doggo of selected breed'
                     ' or a random one if breed is not specified.'),
    )
    @discord.app_commands.describe(
        breed='Breed name',
        hidden='Show the results only for you',
    )
    async def dog_search(
        self, interaction: discord.Interaction,
        breed: Optional[str] = '',
        hidden: Optional[bool] = True,
    ):
        await self.client.log_command_call(interaction, breed=breed)
        await interaction.response.defer(ephemeral=hidden, thinking=True)

        # Removes spaces, because the database
        # doesn't have spaces for dog breeds
        breed = breed.replace(' ', '')

        urlGet = None
        if (breed != '' and len(breed) > 1):
            urlBreeds = 'https://dog.ceo/api/breeds/list/all'
            dataBreeds = requests.get(urlBreeds).json()

            nameDog = ''
            for breedS in dataBreeds['message']:
                if (breed.lower() in breedS.lower()):
                    nameDog = breedS
                    break

            # Found dog
            if (nameDog != ''):
                await self.client.log(
                    f'\tSearching the dog with name {nameDog}'
                )
                urlGet = f'https://dog.ceo/api/breed/{nameDog}/images/random'
                text = f"🐕‍🦺 Here's your {nameDog} dog! 🐩"
        if not urlGet:
            urlGet = "https://dog.ceo/api/breeds/image/random"
            text = "🐕‍🦺 Here's your random dog! 🐩"

        data = requests.get(urlGet).json()

        embed = discord.Embed(
            type='rich', title=text,
            colour=0xFF0596, description='',
        )
        try:
            embed.set_image(url=data['message'])
        except Exception as e:
            await interaction.followup.send(
                content='Sorry, I couldn\'t find a dog... 🐩',
                ephemeral=hidden,
            )
            await self.client.log(f"\tDog broken. [{e}]")
            return

        await interaction.followup.send(embed=embed, ephemeral=hidden)
        await self.client.log("\tDog shown.")
        return

    # CAT GROUP #
    cat_group = discord.app_commands.Group(
        name='cat',
        description=('Shows a cat of selected breed'
                     ' or a random one if breed is not specified.'),
    )

    @cat_group.command(
        name='list',
        description='See all possible cat breeds.',
    )
    async def cat_list(
        self, interaction: discord.Interaction,
    ):
        await self.client.log_command_call(interaction)
        await interaction.response.defer(ephemeral=True, thinking=True)

        urlBreeds = 'https://api.thecatapi.com/v1/breeds'
        dataBreeds = requests.get(urlBreeds).json()

        s = ''
        for item in [breed['name'] for breed in dataBreeds]:
            s += f'- {item}\n'
        embed = discord.Embed(
            type='rich', title='🐈 List of cat breeds: 🐈‍⬛',
            colour=0xFF0596, description=s,
        )

        await interaction.followup.send(
            embed=embed, ephemeral=True,
        )
        await self.client.log("\tCat list shown.")
        return

    @cat_group.command(
        name='search',
        description=('Shows a cat of selected breed'
                     ' or a random one if breed is not specified.'),
    )
    @discord.app_commands.describe(
        breed='Breed name',
        hidden='Show the results only for you',
    )
    async def cat_search(
        self, interaction: discord.Interaction,
        breed: str = '',
        hidden: Optional[bool] = True,
    ):
        await self.client.log_command_call(interaction, breed=breed)
        await interaction.response.defer(ephemeral=hidden, thinking=True)

        breed = breed.lower()

        urlGet = None
        if (breed != "" and len(breed) > 1):
            urlBreeds = 'https://api.thecatapi.com/v1/breeds'
            dataBreeds = requests.get(urlBreeds).json()

            idCat = ''
            nameCat = 'random'
            for breedS in dataBreeds:
                if (breed in breedS['name'].lower().replace(' ', '')):
                    idCat = breedS['id']
                    nameCat = breedS['name']
                    break

            # Didn't find the breed. Searching individual words
            if (idCat == ''):
                for word in breed.split(' '):
                    for breedS in dataBreeds:
                        aux_name = breedS['name'].lower().replace(' ', '')
                        if (word.lower() in aux_name):
                            idCat = breedS['id']
                            nameCat = breedS['name']
                            break

            if (idCat != ''):
                await self.client.log(f'\tSearching the cat with id {idCat}')
                urlGet = ("https://api.thecatapi.com/v1/images/"
                          f"search?breed_ids={idCat}")
                text = f"🐈‍⬛ Here's your {nameCat} cat! 🐈"
        if not (urlGet):
            urlGet = "https://api.thecatapi.com/v1/images/search"
            text = "🐈‍⬛ Here's your random cat! 🐈"

        data = requests.get(urlGet).json()

        embed = discord.Embed(
            type='rich', title=text,
            colour=0xFF0596, description='',
        )
        try:
            embed.set_image(url=data[0]['url'])
        except Exception as e:
            await interaction.followup.send(
                content='Sorry, I couldn\'t find a cat... 🐈‍⬛',
                ephemeral=hidden,
            )
            await self.client.log(f"\tCat broken. [{e}]")
            return

        await interaction.followup.send(embed=embed, ephemeral=hidden)
        await self.client.log("\tCat shown.")
        return

    # STANDALONE AUDIO FUNCIONS #

    @discord.app_commands.command(
        name='chovendo',
        description='Plays a random CHOVENDO audio from the audio list',
    )
    @discord.app_commands.describe(
    )
    async def audio_chovendo_func(
        self, interaction: discord.Interaction,
    ):
        """- Plays a random \"CHOVENDO\" audio from the audio list;"""
        await self.client.log_command_call(interaction)
        await interaction.response.defer(ephemeral=True, thinking=True)
        channel = self.client.get_channel(interaction)

        if (channel is None):
            await interaction.followup.send(
                'You\'re not in a voice channel.', ephemeral=True,
            )
            await self.client.log("\tNot in a voice channel")
            return

        R = random.randint(1, 6)
        audioname = f'Chovendo{R}.wav'

        if (not os.path.isfile(f'Audio/Audio_in/Chovendo/{audioname}')):
            res = trashVariables.getVarFromDb(
                db=self.client.dbs['db_trash_var'],
                name=audioname, variableTag='Name',
            )
            if (res is None):
                await interaction.followup.send(
                    'Unexpected error when obtaining audio.',
                    ephemeral=True,
                )
                await self.client.log(
                    "\tUnexpected error when obtaining audio."
                )
                return
            listAudioManager.convertStringToAudio(
                res['Variable'], 'Audio/Audio_in/Chovendo/', audioname
            )

        await self.playAudio(channel, f'Audio/Audio_in/Chovendo/{audioname}')
        await self.client.log(
            f"\tPlayed [Audio/Audio_in/Chovendo/{audioname}]."
        )
        await interaction.followup.send(
            'Playing audio', ephemeral=True,
        )

    @discord.app_commands.command(
        name='cebolinha',
        description='[PT-BR Command] Quem está morto?',
    )
    @discord.app_commands.describe(
        who='Quem???'
    )
    async def audio_cebolinha_func(
        self, interaction: discord.Interaction,
        who: str,
    ):
        await self.client.log_command_call(interaction, who=who)
        await interaction.response.defer(ephemeral=True, thinking=True)
        channel = self.client.get_channel(interaction)

        try:
            tts = gTTS(text=who, lang='pt', slow=False)
        except Exception as e:
            await interaction.followup.send(
                'Problem connecting to Google\'s TTS API. Try again later.',
                ephemeral=True,
            )
            await self.client.log(
                f'\tProblem connecting to Google\'s TTS API. [{e}]'
            )
            return
        tts.save('Audio/Audio_aux/TTS/CebolaTTS.mp3')

        await self.client.log(f"\tQuem está morto? {who}.")

        song = AudioSegment.from_mp3("Audio/Audio_aux/TTS/CebolaTTS.mp3") - 6
        song2 = AudioSegment.from_mp3("Audio/Audio_in/Effects/cebolinha.mp3")

        Tuts = AudioSegment.from_mp3("Audio/Audio_in/Effects/Tuts.mp3")
        Tuts = Tuts * math.ceil(
            song.duration_seconds / Tuts.duration_seconds
        )
        song = song.overlay(Tuts)

        estaMorto = song2[-1300:]
        audio = song + estaMorto

        audio.export("Audio/Audio_aux/Cebolitos.mp3", format="mp3")

        if (channel is None):
            await interaction.followup.send(
                'You\'re not in a voice channel.', ephemeral=True,
            )
            await self.client.log("\tNot in a voice channel")
            return

        await self.playAudio(channel, 'Audio/Audio_aux/Cebolitos.mp3')
        await interaction.followup.send(
            'Playing audio', ephemeral=True,
        )

    # AUDIO GROUP #
    audio_group = discord.app_commands.Group(
        name='audio',
        description=('Group of audio commands. '
                     'Type "/help audio" for help.'),
    )

    @audio_group.command(
        name='list',
        description='Sends you the list of all playable audios',
    )
    @discord.app_commands.describe(
        hidden='Show the results only for you',
    )
    async def audio_list_func(
        self, interaction: discord.Interaction,
        hidden: Optional[bool] = True,
    ):
        await self.client.log_command_call(interaction)
        await interaction.response.defer(ephemeral=hidden, thinking=True)

        listing = [
            '.'.join(item.split('.')[:-1]).lower()
            for item in list(self.client.aux_vars['audioInfos'].keys())
        ]
        listing.sort()

        s = "List of Audios:\n```"
        for i in range(len(listing)):
            if (listing[i] not in ['users', 'effects']):
                s += f'{listing[i]}\n'
        s += "```"

        await interaction.followup.send(
            s,
            ephemeral=hidden,
        )
        await self.client.log(f"\tDone.")

    @audio_group.command(
        name='info',
        description='Shows information about an audio',
    )
    @discord.app_commands.describe(
        name='Which audio do you want to search?',
        how_many='How many results will be shown. MAXIMUM = 10.',
        hidden='Show the results only for you',
    )
    async def audio_info_func(
        self, interaction: discord.Interaction,
        name: str, how_many: Optional[int] = 3,
        hidden: Optional[bool] = True,
    ):
        async def create_embed(key):
            creator = self.client.aux_vars["audioInfos"][key][0]
            date = self.client.aux_vars["audioInfos"][key][1]

            if (str(creator).isdigit()):
                creator = f'<@!{creator}>'

            s = f'\tFound a match! [{key}]\n'
            s += f'\tCreator: {creator}\n'
            s += f'\tDate: {date}'
            await self.client.log(s)

            embed = discord.Embed(
                type='rich', title=f'Found a match! [{key}]',
                colour=0xFF0596,
                description=f'Creator: {creator}\nDate: {date}'
            )

            return embed

        await self.client.log_command_call(
            interaction, name=name, how_many=how_many
        )
        await interaction.response.defer(ephemeral=hidden, thinking=True)

        ratios = []
        for key in self.client.aux_vars['audioInfos'].keys():
            fratio = fuzz.ratio(name.lower(), key.lower())
            ratios.append((fratio, key))

        ratios.sort(reverse=True)

        embeds = []
        for item in ratios[0:how_many]:
            key = item[1]
            embed = await create_embed(key)
            embeds.append(embed)

        if len(embeds) != 0:
            await interaction.followup.send(
                embeds=embeds, ephemeral=hidden,
            )
        else:
            await interaction.followup.send(
                'No audio found', ephemeral=hidden,
            )

    @audio_group.command(
        name='change',
        description=('Changes the audio that is played when'
                     ' you enter a voice channel'),
    )
    @discord.app_commands.describe(
        attach='Audio attachment',
        link='Link to audio',
    )
    async def audio_change_func(
        self, interaction: discord.Interaction,
        attach: Optional[discord.Attachment] = None,
        link: Optional[str] = None,
    ):
        """[link] - Changes the audio played when you enter a
        voice channel. Uses link if provided,
        or attached file if link is not provided;"""
        author = await self.client.log_command_call(interaction)
        await interaction.response.defer(ephemeral=True, thinking=True)

        if attach:
            selected_url = attach.url
            default_name_file = attach.filename
            file_type = attach.content_type
        elif link:
            selected_url = link
            default_name_file = None
            file_type = None
        else:
            await interaction.followup.send(
                content='No audio received.',
                ephemeral=True,
            )
            await self.client.log('\tNo audio received.')
            return

        # Validation and download of file
        listExtensions = [
            "3gp", "aa", "aac", "aax", "act", "aiff",
            "alac", "amr", "ape", "au", "awb", "dss",
            "dvf", "flac", "gsm", "iklax", "ivs", "m4a",
            "m4b", "m4p", "mmf", "mp3", "mpc", "msv",
            "nmf", "ogg", "oga", "mogg", "opus", "ra",
            "rm", "raw", "rf64", "sln", "tta", "voc",
            "vox", "wav", "wma", "wv", "webm", "8svx", "cda",
        ]
        try:
            (errorCode, errorMess, nomeArq) = self.handle_link(
                selected_url, max_mb=1, list_extensions=listExtensions, default_name_file=default_name_file,
                img=False,
            )
        except Exception as e:
            await interaction.followup.send(
                content=f'Couldn\'t handle file. 😔 [{e}]',
                ephemeral=True,
            )
        if (errorCode != 0):  # Returned error
            await interaction.followup.send(
                content=errorMess, ephemeral=True
            )
            await self.client.log(f'\t{errorMess}')
            return

        # Checks if the audio is valid and puts it's peak volume at -30dB
        await self.client.log('Authenticating audio')
        res = self.authAudio(
            originalFile=nomeArq,
            fileName=f"Audio/Users/{author.id}.mp3",
            limit=30, max_secs=5
        )


        await self.client.log('Authenticated audio')
        if nomeArq != f"Audio/Users/{author.id}.mp3":
            await self.client.log('Removing previous audio from folder')
            os.remove(nomeArq)

        # Confirmação de áudio
        if (res == -1):
            await interaction.followup.send(
                content="Invalid audio. Is it an audio file?",
                ephemeral=True,
            )
            await self.client.log(
                "\tInvalid audio. Is the extension correct?"
            )
            return
        elif (res == -2):
            await interaction.followup.send(
                content="Invalid audio. It's more than 5 seconds long.",
                ephemeral=True,
            )
            await self.client.log(
                "\tInvalid audio. It's more than 5 seconds long."
            )
            return
        else:
            await self.client.log('Converting audio to string')
            stringAudio = usersAudioManager.convertAudioToString(
                f"Audio/Users/{author.id}.mp3"
            )
            await self.client.log('Deleting previous audio from db')
            usersAudioManager.deleteFromDb(
                self.client.dbs['db_users'], f'{str(author.id)}.mp3'
            )
            await self.client.log('Adding new audio to db')
            usersAudioManager.addToDb(
                self.client.dbs['db_users'], f'{str(author.id)}.mp3',
                stringAudio, nameUser=str(author),
            )

            await interaction.followup.send(
                content='Done!', ephemeral=True,
            )
            await self.client.log("\tDone")
            return

    @audio_group.command(
        name='remove',
        description='Removes audio played when you enter a voice channel 😔',
    )
    async def audio_remove_func(
        self, interaction: discord.Interaction,
    ):
        author = await self.client.log_command_call(interaction)
        await interaction.response.defer(ephemeral=True, thinking=True)

        if (
            usersAudioManager.deleteFromDb(
                self.client.dbs['db_users'], f'{author.id}.mp3'
            )
        ):
            await interaction.followup.send(
                "You didn't have an audio 😘",
                ephemeral=True,
            )
            await self.client.log(f"\t{author} didn't have any audio.")
            return
        else:
            os.remove(f'Audio/Users/{author.id}.mp3')
            await interaction.followup.send(
                "You were removed from the audio list. We'll miss you! 🥲",
                ephemeral=True,
            )
            await self.client.log("\tRemoved successfully.")
            return

    @audio_group.command(
        name='add',
        description='Adds a new audio with the provided name',
    )
    @discord.app_commands.describe(
        name='Audio\'s name',
        attach='Audio attachment',
        link='Link to audio',
    )
    async def audio_add_func(
        self, interaction: discord.Interaction,
        name: str,
        attach: Optional[discord.Attachment] = None,
        link: Optional[str] = None,
    ):
        author = await self.client.log_command_call(interaction, name=name)
        await interaction.response.defer(ephemeral=True, thinking=True)

        nameFile = name.lower()
        if (nameFile + '.mp3' in self.client.aux_vars['audioInfos'].keys()):
            await interaction.followup.send(
                "Audio name already in use!", ephemeral=True,
            )
            await self.client.log("\tAudio name already in use!")
            return

        if attach:
            selected_url = attach.url
            default_name_file = attach.filename
            file_type = attach.content_type
        elif link:
            selected_url = link
            default_name_file = None
            file_type = None
        else:
            await interaction.followup.send(
                content='No audio received.',
                ephemeral=True,
            )
            await self.client.log('\tNo audio received.')
            return

        # Validation and download of file
        listExtensions = [
            "3gp", "aa", "aac", "aax", "act", "aiff",
            "alac", "amr", "ape", "au", "awb", "dss",
            "dvf", "flac", "gsm", "iklax", "ivs", "m4a",
            "m4b", "m4p", "mmf", "mp3", "mpc", "msv",
            "nmf", "ogg", "oga", "mogg", "opus", "ra",
            "rm", "raw", "rf64", "sln", "tta", "voc",
            "vox", "wav", "wma", "wv", "webm", "8svx", "cda"
        ]
        try:
            (errorCode, errorMess, nomeArq) = self.handle_link(
                selected_url, max_mb=2, list_extensions=listExtensions, default_name_file=default_name_file,
                img=False,
            )
        except Exception as e:
            await interaction.followup.send(
                content=f'Couldn\'t handle file. 😔 [{e}]',
                ephemeral=True,
            )
        if (errorCode != 0):  # Returned error
            await interaction.followup.send(
                content=errorMess, ephemeral=True,
            )
            await self.client.log(f'{errorMess}')
            return

        # Verifica se o áudio é válido e o coloca em -30dB
        res = self.authAudio(
            originalFile=nomeArq,
            fileName=f'{nameFile}.mp3',
            limit=30, max_secs=7,
        )

        if nomeArq != f'{nameFile}.mp3':
            os.remove(nomeArq)

        # Confirmação de áudio
        if (res == -1):
            await interaction.followup.send(
                "Invalid audio. Did you send an audio file?.",
                ephemeral=True,
            )
            await self.client.log(
                "\tInvalid audio. Couldn't read audio file with library."
            )
            return
        elif (res == -2):
            await interaction.followup.send(
                "Invalid audio. It's more than 7 seconds long.",
                ephemeral=True
            )
            await self.client.log(
                "\tInvalid audio. It's more than 7 seconds long."
            )
            return
        else:
            stringAudio = listAudioManager.convertAudioToString(
                f'{nameFile}.mp3'
            )

            os.replace(
                f'{nameFile}.mp3', f'Audio/Audio_in/{nameFile.lower()}.mp3'
            )
            nameFile = nameFile.lower()

            post = listAudioManager.addToDb(
                self.client.dbs['db_audios'], f'{nameFile}.mp3',
                stringAudio, f'{author.id}',
            )
            self.client.aux_vars['audioInfos'][post['Name']] = \
                [post['Creator'], post['date']]

            await interaction.followup.send(
                f"Done! Added audio [{str(nameFile)}] to our database."
            )
            await self.client.log(
                f'\tDone. Added {nameFile}.'
            )
            return

    @audio_group.command(
        name='delete',
        description='Removes audio from out database',
    )
    @discord.app_commands.describe(
        name='Audio\'s name',
    )
    async def audio_delete_func(
        self, interaction: discord.Interaction,
        name: str,
    ):
        author = await self.client.log_command_call(interaction, name=name)
        await interaction.response.defer(ephemeral=True, thinking=True)

        nameFile = name.lower() if name.endswith('.mp3') \
            else f'{name.lower()}.mp3'

        if (nameFile not in self.client.aux_vars['audioInfos'].keys()):
            await author.send("Audio name isn't in our database!")
            await self.client.log("\tAudio name isn't in our database!")
            return
        else:  # Audio exists - Check owner
            if (
                not await self.client.validate_admin(interaction)
                and self.client.aux_vars['audioInfos'][nameFile]['Creator']
                != author.id
            ):
                interaction.followup.send(
                    "You can't delete this audio", ephemeral=True,
                )
                await self.client.log("\tYou can't delete this audio")
                return

            try:
                os.remove(f"Audio/Audio_in/{nameFile}")
            except Exception as e:  # Didn't download it yet
                await self.client.log(
                    f'\tCouldn\'t delete local file {nameFile}. [{e}]'
                )

            listAudioManager.deleteFromDb(
                self.client.dbs['db_audios'], nameFile,
            )
            self.client.aux_vars['audioInfos'].pop(nameFile, None)

            await interaction.followup.send("Done!")
            await self.client.log(f'\tDone. Removed {nameFile}')

    @audio_group.command(
        name='play',
        description=('Plays audio on connected voice channel.'
                     'Many effects are available through '
                     'input variables.'),
    )
    @discord.app_commands.describe(
        audio_name='Audio\'s name',
        pitch_change='Change audio pitch',
        wacky='Applies wacky effect on audio',
        reverse='Reverses audio',
        random='Gets random audio. <audio_name> is ignored if provided.',
        user='Plays user audio. <audio_name> is ignored if provided.'
    )
    async def audio_play_func(
        self, interaction: discord.Interaction,
        audio_name: Optional[str] = '',
        pitch_change: Optional[float] = 0.,
        wacky: Optional[bool] = False,
        reverse: Optional[bool] = False,
        random: Optional[bool] = False,
        user: Optional[discord.User] = None,
    ):
        await self.client.log_command_call(
            interaction, audio_name=audio_name, pitch_change=pitch_change,
            wacky=wacky, reverse=reverse, random=random, user=user,
        )
        await interaction.response.defer(ephemeral=True, thinking=True)

        if (audio_name == '' and random is False and user is None):
            await self.client.log('\tNo input. Playing random audio.')
            random = True

        # Gets channel
        channel = self.client.get_channel(interaction)
        if (channel is None):
            await interaction.followup.send(
                "You're not in a voice channel.",
                ephemeral=True,
            )
            await self.client.log("\tNot in a voice channel")
            return

        if user:
            audio_name = f'{str(user.id)}.mp3'
        elif random:
            audio_name = listAudioManager.getRandomAudio(
                self.client.dbs['db_audios']
            ).lower()[:-4]
            if (audio_name == -1):
                await interaction.followup.send(
                    'Unexpected error when obtaining audio.',
                    ephemeral=True,
                )
                await self.client.log(
                    "\tUnexpected error when obtaining audio."
                )
                return

        if user:
            downloaded_file = self.client.checkForAudio(
                audioname=audio_name, check_db=self.client.dbs['db_users'],
                audioFolder='Users/',
            )
        else:
            # Check if audio exists
            audio_name = f'{audio_name}.mp3'.lower()
            if (audio_name not in self.client.aux_vars['audioInfos'].keys()):
                await interaction.followup.send(
                    f"Sorry, no audio named '{audio_name}' was found.",
                    ephemeral=True,
                )
                await self.client.log(
                    f"\tCouldn't find file '{audio_name}'"
                )
                return

            # Tries to either download or use local file
            downloaded_file = self.client.checkForAudio(
                audioname=audio_name,
                audioFolder='Audio_in/',
                check_db=self.client.dbs['db_audios'],
            )

        if not downloaded_file:
            await interaction.followup.send(
                f"Error downloading file. Does it exist?",
                ephemeral=True,
            )
            await self.client.log(
                f"\tError downloading file."
            )
            return

        # Move to aux, to preprocess audio
        if user:
            shutil.copy(
                f'Audio/Users/{audio_name}',
                f'Audio/Audio_aux/{audio_name}',
            )
        else:
            shutil.copy(
                f'Audio/Audio_in/{audio_name}',
                f'Audio/Audio_aux/{audio_name}',
            )

        res = await self.process_audio(
            interaction=interaction,
            path_file=f'Audio/Audio_aux/{audio_name}',
            pitch_change=pitch_change,
            wacky=wacky,
            reverse=reverse,
        )

        if res == -1:
            await interaction.followup.send(
                'Error processing audio', ephemeral=True,
            )
            await self.client.log('\tError processing audio')
            return

        await self.playAudio(channel, f'Audio/Audio_aux/{audio_name}')
        await interaction.followup.send(
            'Done!', ephemeral=True,
        )
        await self.client.log('\tDone!')

    # TTS GROUP #
    tts_group = discord.app_commands.Group(
        name='tts',
        description=('Group of TTS (Text To Speech) commands. '
                     'Type "/help tts" for help.'),
    )

    @tts_group.command(
        name='play',
        description=('Plays TTS of the message written'
                     'in selected language.')
    )
    @discord.app_commands.describe(
        message='Message to be said',
        language='Language in which the message will be said [e.g. "pt"]',
        pitch_change='Change TTS pitch',
        wacky='Applies wacky effect on TTS',
        reverse='Reverses TTS',
    )
    async def tts_play_func(
        self, interaction: discord.Interaction,
        message: str,
        language: Optional[str] = 'pt',
        pitch_change: Optional[float] = 0.,
        wacky: Optional[bool] = False,
        reverse: Optional[bool] = False,
    ):
        await self.client.log_command_call(
            interaction, message=message, language=language,
            pitch_change=pitch_change, wacky=wacky, reverse=reverse,
        )
        await interaction.response.defer(ephemeral=True, thinking=True)

        # Gets channel
        channel = self.client.get_channel(interaction)
        if (channel is None):
            await interaction.followup.send(
                "You're not in a voice channel.",
                ephemeral=True,
            )
            await self.client.log("\tNot in a voice channel")
            return

        # Check if it's a valid language
        language = language.lower()
        approx_lang = False

        # If language is not valid, get closer in list
        if (language not in list(
            self.client.aux_vars['language_list'].keys()
        )):
            fratio = 0
            for key, value in self.client.aux_vars['language_list'].items():
                fratio_1 = fuzz.ratio(language, key.lower())
                fratio_2 = fuzz.ratio(language, value.lower())
                fratio_comp = max(fratio_1, fratio_2)

                if (fratio_comp > fratio):
                    language = key
                    approx_lang = True

        # Create the TTS
        try:
            tts = gTTS(text=message, lang=language, slow=False)
        except Exception as e:
            await interaction.followup.send(
                'Problem connecting to Google\'s TTS API. Try again later.',
                ephemeral=True
            )
            await self.client.log(
                f'\tProblem connecting to Google\'s TTS API. [{e}]'
            )
            return

        tts.save('Audio/Audio_aux/TTS.mp3')

        shutil.copy(
            f'Audio/Audio_aux/TTS.mp3',
            f'Audio/Audio_aux/pTTS.mp3',
        )

        res = await self.process_audio(
            interaction=interaction,
            path_file=f'Audio/Audio_aux/pTTS.mp3',
            pitch_change=pitch_change,
            wacky=wacky,
            reverse=reverse,
        )

        if res == -1:
            await interaction.followup.send(
                'Error processing audio', ephemeral=True,
            )
            await self.client.log('\tError processing audio')
            return

        await self.playAudio(channel, 'Audio/Audio_aux/pTTS.mp3')
        await interaction.followup.send(
            f'{"[Assuming language]"*approx_lang} Playing audio in {language}',
            ephemeral=True,
        )

    @tts_group.command(
        name='translate',
        description='Translates and play a TTS of the translated message'
    )
    @discord.app_commands.describe(
        message='Message to be said',
        say_it='Play the TTS in a voice channel',
        language_from='Language to translate from [e.g. "pt"]',
        language_to='Language in which the message will be said [e.g. "en"]',
        pitch_change='Change TTS pitch',
        wacky='Applies wacky effect on TTS',
        reverse='Reverses TTS',
    )
    async def tts_translate_func(
        self, interaction: discord.Interaction,
        message: str,
        say_it: Optional[bool] = True,
        language_from: Optional[str] = 'pt',
        language_to: Optional[str] = 'en',
        pitch_change: Optional[float] = 0.,
        wacky: Optional[bool] = False,
        reverse: Optional[bool] = False,
    ):
        await self.client.log_command_call(
            interaction, message=message, say_it=say_it,
            language_from=language_from, language_to=language_to,
            pitch_change=pitch_change, wacky=wacky, reverse=reverse,
        )
        await interaction.response.defer(ephemeral=True, thinking=True)

        language_from = language_from.lower()
        language_to = language_to.lower()

        approx_lang_from = False
        approx_lang_to = False

        all_lgs = self.client.aux_vars['language_list'].keys()
        all_lgs_tp = self.client.aux_vars['language_list'].items()

        # Check if language_from is available. If not, get closer match
        if language_from in all_lgs:
            src_key = language_from
            src_nm = self.client.aux_vars['language_list'][src_key]
        else:
            fratio = 0
            for key, value in all_lgs_tp:
                fratio_1 = fuzz.ratio(language_from, key.lower())
                fratio_2 = fuzz.ratio(language_from, value.lower())
                fratio_comp = max(fratio_1, fratio_2)

                if (fratio_comp > fratio):
                    src_key = key
                    src_nm = value
                    approx_lang_from = True

        # Check if language_to is available. If not, get closer match
        if language_from in all_lgs:
            dst_key = language_to
            dst_nm = self.client.aux_vars['language_list'][dst_key]
        else:
            fratio = 0
            for key, value in all_lgs_tp:
                fratio_1 = fuzz.ratio(language_to, key.lower())
                fratio_2 = fuzz.ratio(language_to, value.lower())
                fratio_comp = max(fratio_1, fratio_2)

                if (fratio_comp > fratio):
                    dst_key = key
                    dst_nm = value
                    approx_lang_to = True

        translator = Translator()

        try:
            translation = translator.translate(
                message, src=src_key, dest=dst_key
            )
        except Exception as e:
            await interaction.followup.send(
                'Problem connecting to Google\'s translation API.',
                ephemeral=True,
            )
            await self.client.log(
                f'\t Google Translate API raised an exception. [{e}]',
            )
            return

        # Creates message, and logs everything
        msg = ''
        if approx_lang_from:
            msg += '[Aproximated language_from]\n'
            await self.client.log('\t[Aproximated language_from]')
        if approx_lang_to:
            msg += '[Aproximated language_to]\n'
            await self.client.log('\t[Aproximated language_to]')
        msg += (f"```Original from {src_nm}: {message}\n"
                f"To {dst_nm}: {translation.text}```")
        await self.client.log(f"\tOriginal from {src_nm}: {message}")
        await self.client.log(f"\tTo {dst_nm}: {translation.text}")

        # Message already translated, if not "say_it", we're done
        if not say_it:
            await interaction.followup.send(
                msg,
                ephemeral=False,
            )
            return

        # Gets channel
        channel = self.client.get_channel(interaction)

        if (channel is None):
            await interaction.followup.send(
                f"{msg}\nYou're not in a voice channel!",
                ephemeral=False,
            )
            await self.client.log("\tNot in a voice channel")
            return

        # Create the TTS
        try:
            tts = gTTS(text=translation.text, lang=language_to, slow=False)
        except Exception as e:
            await interaction.followup.send(
                (f'{msg}\n'
                 'Problem connecting to Google\'s TTS API. Try again later.'),
                ephemeral=False,
            )
            await self.client.log(
                f'\tProblem connecting to Google\'s TTS API. [{e}]'
            )
            return

        tts.save('Audio/Audio_aux/TranslateTTS.mp3')

        shutil.copy(
            'Audio/Audio_aux/TranslateTTS.mp3',
            'Audio/Audio_aux/pTranslateTTS.mp3',
        )

        res = await self.process_audio(
            interaction=interaction,
            path_file='Audio/Audio_aux/pTranslateTTS.mp3',
            pitch_change=pitch_change,
            wacky=wacky,
            reverse=reverse,
        )

        if res == -1:
            await interaction.followup.send(
                'Error processing audio', ephemeral=True,
            )
            await self.client.log('\tError processing audio')
            return

        await self.playAudio(channel, 'Audio/Audio_aux/pTranslateTTS.mp3',)
        await interaction.followup.send(
            f'{msg}\nDone"',
            ephemeral=False,
        )
        await self.client.log(f'\tDone!')

    # STANDALONE COUNT FUNCTIONS #
    @discord.app_commands.command(
        name='panda',
        description='Don\'t do that with the panda :(',
    )
    @discord.app_commands.describe(
    )
    async def panda_func(
        self, interaction: discord.Interaction,
    ):
        """- Don't use this command 🐼;"""
        await self.client.log_command_call(interaction)
        await interaction.response.defer(ephemeral=False, thinking=True)

        posts = self.client.dbs['db_users'].posts
        query = {"tag": "counterPharmercy"}
        dbPharmercy = posts.find_one(query)
        if (dbPharmercy is not None):
            counter = int(dbPharmercy["valor"]) + 1
            posts.delete_one(query)
        else:
            counter = 1

        post = {
            "tag": "counterPharmercy",
            "valor": counter,
            "date": datetime.datetime.utcnow(),
        }
        posts = self.client.dbs['db_users'].posts
        posts.insert_one(post).inserted_id

        url = r"https://i.imgur.com/4pWGt0W.gif"

        embed = discord.Embed(
            type='rich', title='😭',
            colour=0x7CC77C, description=f'Já morreram {counter} pandas',
        )
        embed.set_image(url=url)

        await interaction.followup.send(
            embed=embed,
        )
        await self.client.log(f"\tDone!")

    @discord.app_commands.command(
        name='god',
        description='Add a god internet point to the person.',
    )
    @discord.app_commands.describe(
        person='Member to add the point to'
    )
    async def god_func(
        self, interaction: discord.Interaction,
        person: discord.Member,
    ):
        author = await self.client.log_command_call(
            interaction, person=person.id
        )
        await interaction.response.defer(ephemeral=False, thinking=True)

        counterName = str(person.id)

        res = trashVariables.getVarFromDb(
            self.client.dbs['db_trash_var'], counterName, 'God_Counter'
        )

        if (res is not None):
            counter = int(res['Variable']) + 1
            trashVariables.deleteFromDb(
                self.client.dbs['db_trash_var'], counterName, 'God_Counter'
            )
        else:
            counter = 1

        trashVariables.addToDb(
            self.client.dbs['db_trash_var'], counterName,
            counter, 'God_Counter',
        )

        await interaction.followup.send(
            content=('https://cdn.discordapp.com/attachments/'
                     '183784872114913280/796554042187710494/'
                     'mercy.jpg\n'
                     f'Hey, <@!{str(author.id)}>\n'
                     f'God Counter [<@!{counterName}>]: {counter}'),
            ephemeral=False,
        )

        await self.client.log(f"\tDone.")

    # COUNT GROUP #
    count_group = discord.app_commands.Group(
        name='count',
        description=('Group of count commands. '
                     'Type "/help count" for help.'),
    )

    @count_group.command(
        name='check',
        description='Check the value of a variable',
    )
    @discord.app_commands.describe(
        variable='Variable name',
    )
    async def count_variable_check_func(
        self, interaction: discord.Interaction,
        variable: str,
    ):
        author = await self.client.log_command_call(
            interaction, variable=variable
        )
        await interaction.response.defer(ephemeral=False, thinking=True)

        variable = variable.lower()

        res = trashVariables.getVarFromDb(
            self.client.dbs['db_trash_var'], variable, 'Variable_Counter'
        )

        if (res is not None):
            counter = int(res['Variable'])
        else:
            counter = 0

        await interaction.followup.send(
            content=(f'Hey, <@!{author.id}>\n'
                     f'Counter [{variable.capitalize()}]: {counter}'),
            ephemeral=False,
        )
        await self.client.log(
            f"\tCounter [{variable.capitalize()}]: {counter}"
        )

    @count_group.command(
        name='add',
        description='Add [number] points to the variable. By default 1',
    )
    @discord.app_commands.describe(
        variable='Variable name',
        number='How many points to add',
    )
    async def count_variable_add_func(
        self, interaction: discord.Interaction,
        variable: str, number: Optional[int] = 1,
    ):
        author = await self.client.log_command_call(
            interaction, variable=variable, number=number
        )
        await interaction.response.defer(ephemeral=False, thinking=True)

        variable = variable.lower()

        res = trashVariables.getVarFromDb(
            self.client.dbs['db_trash_var'], variable, 'Variable_Counter'
        )

        if (res is not None):
            counter = int(res['Variable']) + number
            trashVariables.deleteFromDb(
                self.client.dbs['db_trash_var'], variable, 'Variable_Counter'
            )
        else:
            counter = number

        trashVariables.addToDb(
            self.client.dbs['db_trash_var'], variable,
            counter, 'Variable_Counter',
        )

        await interaction.followup.send(
            content=(f'Hey, <@!{author.id}>\n'
                     f'Counter [{variable.capitalize()}]: {counter}'),
            ephemeral=False,
        )
        await self.client.log(
            f"\tCounter [{variable.capitalize()}]: {counter}"
        )

    @count_group.command(
        name='set',
        description='Sets <number> points to the variable',
    )
    @discord.app_commands.describe(
        variable='Variable name',
        number='How many points to set the variable'
    )
    async def count_variable_set_func(
        self, interaction: discord.Interaction,
        variable: str, number: int,
    ):
        author = await self.client.log_command_call(
            interaction, variable=variable, number=number
        )
        await interaction.response.defer(ephemeral=True, thinking=True)

        variable = variable.lower()

        res = trashVariables.getVarFromDb(
            self.client.dbs['db_trash_var'], variable, 'Variable_Counter'
        )

        if (res is not None):
            counter = number
            trashVariables.deleteFromDb(
                self.client.dbs['db_trash_var'], variable, 'Variable_Counter'
            )
        else:
            counter = number

        trashVariables.addToDb(
            self.client.dbs['db_trash_var'], variable,
            counter, 'Variable_Counter',
        )

        await interaction.followup.send(
            content=(f'Hey, <@!{str(author.id)}>\n'
                     f'Counter [{str(variable).capitalize()}]: {counter}'),
            ephemeral=True,
        )
        await self.client.log(
            f"\tCounter [{str(variable).capitalize()}]: {counter}"
        )

    # CURRENCY GROUP #
    currency_group = discord.app_commands.Group(
        name='currency',
        description=('Group of currency commands. '
                     'Type "/help currency" for help.'),
    )

    @currency_group.command(
        name='list',
        description='Lists all currencies',
    )
    @discord.app_commands.describe(
    )
    async def currency_list_func(
        self, interaction: discord.Interaction,
    ):
        """- Lists all currencies;"""
        await self.client.log_command_call(interaction)
        await interaction.response.defer(ephemeral=True, thinking=True)

        try:
            last_update = self.client.aux_vars['converter'].lastUpdate
            seconds_since = (last_update - datetime.datetime.now()).seconds
        except AttributeError:
            seconds_since = 0

        if (self.client.aux_vars['converter'] is None
                or seconds_since > 3600):
            self.client.aux_vars['converter'] = getCurrency.CurrencyConverter()

        await interaction.followup.send(
            embeds=self.client.aux_vars['converter'].embedsOfCurrencies,
            ephemeral=True,
        )
        await self.client.log('Done!')

    @currency_group.command(
        name='convert',
        description=('Converts a value from source currency'
                     ' to destination currency;'
                     'If value is not given, it\'s set as 1;')
    )
    @discord.app_commands.describe(
        source='Currency to convert from',
        dest='Currency to convert to',
        value='How many points to set the variable'
    )
    async def currency_convert_func(
        self, interaction: discord.Interaction,
        source: str, dest: str,
        value: Optional[float] = 1.0,
    ):
        await self.client.log_command_call(
            interaction, source=source, dest=dest, value=value
        )
        await interaction.response.defer(ephemeral=True, thinking=True)

        source = source.upper()
        dest = dest.upper()

        # Create another converter if it was used more than 1 hour ago or
        # if it was never created
        try:
            last_update = self.client.aux_vars['converter'].lastUpdate
            seconds_since = (last_update - datetime.datetime.now()).seconds
        except AttributeError:
            seconds_since = 0
        if (self.client.aux_vars['converter'] is None
                or seconds_since > 3600):
            self.client.aux_vars['converter'] = getCurrency.CurrencyConverter()

        converter = self.client.aux_vars['converter']

        converted_value = converter.convert(
            source, dest, value
        )

        msg = ''
        if (converted_value == -1 or converted_value == -2):
            if (converted_value == -1):
                converter.convert('USD', dest, value)
                source_aux = converter.getCurrency(source)
                dest_aux = converter.getCurrency(dest)
            else:
                source_aux = converter.getFromList(source)
                dest_aux = converter.getCurrency(dest)

            msg = (f'Source {source_aux[1]} from {source_aux[0]}'
                   f' to {dest_aux[1]} from {dest_aux[0]}\n')
            converted_value = converter.convert(
                source_aux[-1], dest_aux[-1], value
            )
            source = source_aux[-1]
            dest = dest_aux[-1]

        title = f'💰 {source} to {dest} 💰'
        msg += (f'```css\n{value} {source}'
                f' = {converted_value} {dest}```')

        embed = discord.Embed(
            type='rich', title=title,
            colour=0x7CC77C, description=msg,
        )
        embed.set_image(url='https://i.imgur.com/8XhBzhx.png')

        await interaction.followup.send(
            embeds=[embed], ephemeral=False,
        )
        await self.client.log(
            f'\t{value} {source} = {converted_value} {dest}'
        )


async def setup(client):
    await client.add_cog(MainCog(client))
