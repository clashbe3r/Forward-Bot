"""
- This script is responsible for handling the source command
"""
import asyncio

from pyrogram import Client
from pyrogram.types import Message

from bot.config import Config
from bot.utils.text_button import TextButton


async def handle_source_command(bot: Client, update: Message) -> None:
    """
    Handles the source command received by the bot
    :param bot: Client
    :param update: Message
    :return: None
    """
    config = Config()
    # if update from group or channel
    if update.chat:
        if update.from_user:
            # if message received from pm
            if update.chat.id == update.from_user.id:
                if update.command[-1] == "source":
                    # if sender is an admin
                    if update.from_user.id in config.ADMINS:
                        if config.SOURCE_CHANNEL_ID:
                            chat = await bot.get_chat(
                                chat_id=config.SOURCE_CHANNEL_ID
                            )
                            await update.reply_text(
                                text=f"""
Current Source Channel:
Channel Name: {chat.title}
Channel ID: {chat.id}
Members Count: {chat.members_count}"""
                            )
                        else:
                            await update.reply_text(
                                text="No channel is added as source!"
                            )
                    # if sender not an admin
                    else:
                        await update.reply_text(
                            text=TextButton.get_others_notification_text()
                        )
                # if a parameter has been sent with source
                else:
                    if len(update.command) == 2:
                        if update.command[-1] == "r":
                            await update.reply_text(
                                text="Source removed! No message will be forwarded until new source added!"
                            )
                            config.data["source_channel_id"] = 0
                            config.write_data()
                            for admin in config.ADMINS:
                                if admin not in config.NO_NOTIFICATION_ADMINS:
                                    if admin != update.from_user.id:
                                        await bot.send_message(
                                            chat_id=admin,
                                            text=f"""
{update.from_user.mention} removed existing source channel!"""
                                        )
                        else:
                            await update.reply_text(
                                text=f"""
Invalid parameter provided!

* To view details about source send /source in pm
* To add a channel to the source, open the channel and send /source
* To remove existing source send /source r"""
                            )
                    else:
                        await update.reply_text(
                            text=f"""
Invalid parameter provided!

* To view details about source send /source in pm
* To add a channel to the source, open the channel and send /source
* To remove existing source send /source r"""
                        )

        # if update from channel
        elif not update.from_user:
            if config.SOURCE_CHANNEL_ID:
                msg = await update.reply_text(
                    text=TextButton.get_another_channel_added_text()
                )
                await asyncio.sleep(5)
                await msg.delete()
                await update.delete()
            else:
                config.data["source_channel_id"] = update.chat.id
                config.write_data()
                msg = await update.reply_text(
                    text=TextButton.get_channel_added_text()
                )
                for admin in config.ADMINS:
                    if admin not in config.NO_NOTIFICATION_ADMINS:
                        await bot.send_message(
                            chat_id=admin,
                            text=f"""
Added source channel!
Channel Name: {update.chat.title}
Channel ID: {update.chat.id}"""
                        )
                await asyncio.sleep(5)
                await msg.delete()
