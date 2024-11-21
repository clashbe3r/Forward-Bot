"""
- This script is responsible for handling message forwarding
"""
import asyncio

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import RPCError, FloodWait

from bot.config import Config


async def handle_message_forwarding(bot: Client, update: Message) -> None:
    """
    Handles the message forwarding task
    :param bot: pyrogram.Client
    :param update: pyrogram.types.Message
    :return: None
    """
    config = Config()
    if update.chat.id == config.SOURCE_CHANNEL_ID:
        count = 0
        for target in config.TARGET_GROUP_IDS:
            try:
                await bot.copy_message(
                    chat_id=target,
                    from_chat_id=update.chat.id,
                    message_id=update.id
                )
                count += 1

            except FloodWait as e:
                await asyncio.sleep(e.value)
                await bot.copy_message(
                    chat_id=target,
                    from_chat_id=update.chat.id,
                    message_id=update.id
                )
                count += 1

            except RPCError:
                pass
        for admin in config.ADMINS:
            try:
                await bot.copy_message(
                    chat_id=admin,
                    from_chat_id=update.chat.id,
                    message_id=update.id
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await bot.copy_message(
                    chat_id=admin,
                    from_chat_id=update.chat.id,
                    message_id=update.id
                )
            except RPCError:
                pass
            else:
                try:
                    await bot.send_message(
                        chat_id=admin,
                        text="sent!"
                    )
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await bot.send_message(
                        chat_id=admin,
                        text="sent!"
                    )
