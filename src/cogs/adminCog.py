import discord
from discord.ext import commands

from typing import Optional


class AdminCog(commands.Cog, name='AdminCog', command_attrs=dict(hidden=True)):
    def __init__(self, client):
        super().__init__()
        self.client = client

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

    admin_group = discord.app_commands.Group(
        name='admin',
        description=('Admin group commands. Send /help admin for help.'),
    )

    # ADMIN COMMANDS #
    @admin_group.command(
        name='getlog',
        description='Sends log txt',
    )
    @discord.app_commands.describe(
    )
    async def getlog_func(self, interaction: discord.Interaction):
        await self.client.log_command_call(interaction)

        if not (await self.client.validate_admin(interaction)):
            await self.client.log('\tAccess denied.')
            return

        with open('log.txt', 'rb') as fp:
            file = discord.File(fp, filename='Log_virus.txt')
            await interaction.response.send_message(
                file=file, ephemeral=True,
            )
        await self.client.log(f'\tDone!')

    @admin_group.command(
        name='close',
        description='Closes bot',
    )
    @discord.app_commands.describe(
    )
    async def close_func(self, interaction: discord.Interaction):
        await self.client.log_command_call(interaction)

        if not (await self.client.validate_admin(interaction)):
            await self.client.log('\tAccess denied.')
            return

        await self.client.log('\tGoodbye!')
        await interaction.response.send_message(
            f'\tGoodbye!.', ephemeral=True,
        )
        await self.client.close(-1)

    @admin_group.command(
        name='fix',
        description='Tries to set presence again',
    )
    @discord.app_commands.describe(
        gamename='Name of the game'
    )
    async def fixpresence_func(
        self, interaction: discord.Interaction,
        gamename: Optional[str] = None,
    ):
        await self.client.log_command_call(interaction)

        if not (await self.client.validate_admin(interaction)):
            await self.client.log('\tAccess denied.')
            return

        if not gamename:
            gamename = self.client.aux_vars['gameName']

        try:
            await self.client.change_presence(
                activity=discord.Activity(
                    name=gamename,
                    url="https://play.barbie.com",
                    type=discord.ActivityType.streaming,
                    start=1, state='Epic Gamer Moment', details='Being Toxic',
                    assets={
                        'large_image': 'ow_6', 'large_text': 'Scooby Dooby',
                        'small_image': 'ow_6', 'small_text': 'Scooby Dooby Doo'
                    }
                )
            )
            await self.client.log("\tGame title set again.")
            await interaction.response.send_message(
                '\tDone.', ephemeral=True,
            )
        except discord.InvalidArgument:
            await self.client.log("\tInvalid game.")
            await interaction.response.send_message(
                '\tInvalid game', ephemeral=True,
            )
        except Exception as e:
            await self.client.log(f"\tUnexpected error on /admin fix. [{e}]")
            await interaction.response.send_message(
                f'\tUnknown error [{e}].', ephemeral=True,
            )

    @admin_group.command(
        name='profile',
        description='Changes bot nickname',
    )
    @discord.app_commands.describe(
        nickname='New nickname',
    )
    async def profile_func(
        self, interaction: discord.Interaction,
        nickname: str,
    ):
        await self.client.log_command_call(interaction)

        if not (await self.client.validate_admin(interaction)):
            await self.client.log('\tAccess denied.')
            return

        try:
            await self.client.user.edit(username=nickname)
            await self.client.log(f"\tNew nickname: {nickname}")
            await self.client.log("\tProfile updated.")
            await interaction.response.send_message(
                'Done', ephemeral=True,
            )
        except Exception as e:
            await self.client.log(f"\tCouldn't update profile. [{e}]")
            await interaction.response.send_message(
                f'\tUnknown error [{e}].', ephemeral=True,
            )

    @admin_group.command(
        name='cmon',
        description='Calls bot to current channel'
    )
    @discord.app_commands.describe(
    )
    async def cmon_func(self, interaction: discord.Interaction):
        await self.client.log_command_call(interaction)

        if not (await self.client.validate_admin(interaction)):
            await self.client.log('\tAccess denied.')
            return

        channel = self.client.get_channel(interaction)
        if (channel is None):
            await self.client.log(f"\tNo voice channel.")
            return

        await channel.connect()
        await self.client.log(f"\tDone.")
        await interaction.response.send_message(
            'Done', ephemeral=True,
        )

    @admin_group.command(
        name='gtfo',
        description='Makes bot disconnect from every voice client it sees'
    )
    @discord.app_commands.describe(
    )
    async def gtfo_func(self, interaction: discord.Interaction):
        await self.client.log_command_call(interaction)

        if not (await self.client.validate_admin(interaction)):
            await self.client.log('\tAccess denied.')
            return

        voice_clients = self.client.voice_clients

        for voice_client in voice_clients:
            await voice_client.disconnect()

        await self.client.log(f"\tDone.")
        await interaction.response.send_message(
            'Done', ephemeral=True,
        )


async def setup(client):
    server_id = client.aux_vars['admin_svr_id']
    await client.add_cog(
        AdminCog(client),
        guild=discord.Object(id=server_id),
    )
