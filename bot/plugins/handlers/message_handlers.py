"""
- This script is responsible for getting message updates from users using the main client
  This script also handles the updates and process them
"""

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.forwarder_bot import ForwarderBot
from bot.plugins.actions import (
    handle_start_message,
    handle_setup_command,
    handle_source_command,
    handle_remove_command,
    handle_groups_command,
    handle_message_forwarding)
from bot.config import Config
from bot.utils.text_button import TextButton


@ForwarderBot.on_message(~filters.me & filters.command("start"))
async def start_command_handler(_: Client, update: Message) -> None:
    """
    Receives the start command and handles that as well
    :param _: pyrogram.Client - main bot client
    :param update: pyrogram.types.Message - actual message received by the bot
    :return: None
    """
    await handle_start_message(update)


@ForwarderBot.on_message(~filters.me & filters.command("setup"))
async def setup_command_handler(bot: Client, update: Message) -> None:
    """
    Receives the setup command and handles that as well
    :param bot: pyrogram.Client - main bot client
    :param update: pyrogram.types.Message - actual message received by the bot
    :return: None
    """
    await handle_setup_command(bot, update)


@ForwarderBot.on_message(~filters.me & filters.command("source"))
async def source_command_handler(bot: Client, update: Message) -> None:
    """
    Receives the source command and handles that as well
    :param bot: pyrogram.Client - main bot client
    :param update: pyrogram.types.Message - actual message received by the bot
    :return: None
    """
    await handle_source_command(bot, update)


@ForwarderBot.on_message(~filters.me & filters.command("remove"))
async def remove_command_handler(bot: Client, update: Message) -> None:
    """
    Receives the remove command and handles that as well
    :param bot: pyrogram.Client - main bot client
    :param update: pyrogram.types.Message - actual message received by the bot
    :return: None
    """
    await handle_remove_command(bot, update)


@ForwarderBot.on_message(~filters.me & filters.command("groups"))
async def groups_command_handler(_: Client, update: Message) -> None:
    """
    Receives the groups command and handles that as well
    :param _: pyrogram.Client - main bot client
    :param update: pyrogram.types.Message - actual message received by the bot
    :return: None
    """
    await handle_groups_command(update)


@ForwarderBot.on_message(~filters.me & filters.command("id"))
async def id_command_handler(_: Client, update: Message) -> None:
    """
    Receives the groups command and handles that as well
    :param _: pyrogram.Client - main bot client
    :param update: pyrogram.types.Message - actual message received by the bot
    :return: None
    """
    await update.reply_text(
        text=f"Chat id: `{update.chat.id}`"
    )


@ForwarderBot.on_message(~filters.private & ~filters.me)
async def handle_all_channel_message(bot: Client, update: Message) -> None:
    """
    Receives all the messages sent to the channel
    :param bot: pyrogram.Client - main bot client
    :param update: pyrogram.types.Message - actual message received by the bot
    :return: None
    """
    await handle_message_forwarding(bot, update)


@ForwarderBot.on_message(filters.private & ~filters.me)
async def all_private_message_handler(_: Client, update: Message) -> None:
    """
    Receives all the messages sent privately
    :param _: pyrogram.Client - main bot client
    :param update: pyrogram.types.Message - actual message received by the bot
    :return: None
    """
    config = Config()
    if update.from_user.id in config.ADMINS:
        admins_count = len(config.ADMINS)
        target_groups_count = len(config.TARGET_GROUP_IDS)
        await update.reply_text(
            text=f"{TextButton.get_admin_welcome_text()}\n"
                 f"We have total {admins_count} users with admin access!\n"
                 f"We have total {target_groups_count} groups setup as target.\n"
                 f"{'We also have source channel setup' if config.SOURCE_CHANNEL_ID else ''}\n"
                 f"To get any help related to commands, send /help."
        )

    else:
        await update.reply_text(
            text=TextButton.get_others_notification_text()
        )
