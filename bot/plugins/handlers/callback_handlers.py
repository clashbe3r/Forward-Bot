"""
- This script is responsible for handling all the callback requests
"""
import asyncio

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from pyrogram.errors import RPCError, ChannelInvalid, ChatInvalid, ChatIdInvalid, FloodWait

from bot.config import Config
from bot.forwarder_bot import ForwarderBot
from bot.utils.text_button import TextButton


@ForwarderBot.on_callback_query(filters.regex("add_"))
async def add_callback_handler(bot: Client, update: CallbackQuery) -> None:
    """
    Handles add callback query
    :param bot: pyrogram.Client - Main client
    :param update: pyrogram.types.CallbackQuery - CallbackQuery data
    :return: None
    """
    config = Config()
    if update.from_user.id in config.ADMINS:
        group_id = int(update.data.split("_")[-1])
        if group_id in config.TARGET_GROUP_IDS:
            await update.edit_message_text(
                text="Already in the target list!"
            )
        else:
            try:
                chat = await bot.get_chat(
                    chat_id=group_id
                )
            except ChannelInvalid:
                await update.edit_message_text(
                    text="Could not access the group! Make sure to add me to the group as admin!"
                )
            except ChatInvalid:
                await update.edit_message_text(
                    text="Could not access the group! Make sure to add me to the group as admin!"
                )
            except ChatIdInvalid:
                await update.edit_message_text(
                    text="Could not access the group! Make sure to add me to the group as admin!"
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await bot.get_chat(
                    chat_id=group_id
                )
                config.data["target_group_ids"].append(group_id)
                config.write_data()
                for admin in config.ADMINS:
                    if admin not in config.NO_NOTIFICATION_ADMINS:
                        if admin != update.from_user.id:
                            await bot.send_message(
                                chat_id=admin,
                                text=TextButton.get_group_added_notification_text().replace(
                                    "{mention}", update.from_user.mention).replace(
                                    "{group_name}", chat.title).replace("{group_id}",
                                                                        str(chat.id))
                            )
            except RPCError:
                await update.edit_message_text(
                    text="Could not access the group! Make sure to add me to the group as admin!"
                )
            else:
                config.data["target_group_ids"].append(group_id)
                config.write_data()
                for admin in config.ADMINS:
                    if admin not in config.NO_NOTIFICATION_ADMINS:
                        if admin != update.from_user.id:
                            await bot.send_message(
                                chat_id=admin,
                                text=TextButton.get_group_added_notification_text().replace(
                                    "{mention}", update.from_user.mention).replace(
                                    "{group_name}", chat.title).replace("{group_id}",
                                                                        str(chat.id))
                            )


@ForwarderBot.on_callback_query(filters.regex("dont"))
async def dont_callback_handler(_: Client, update: CallbackQuery) -> None:
    """
    Don't call back handler
    :param _: pyrogram.Client
    :param update: pyrogram.types.CallbackQuery
    :return: None
    """
    await update.edit_message_text(
        text="Okay! Doing nothing!"
    )
