"""
- This script is responsible for handling the remove command
"""

from pyrogram import Client
from pyrogram.types import Message

from bot.config import Config
from bot.utils.text_button import TextButton


async def handle_remove_command(bot: Client, update: Message) -> None:
    """
    Handles the remove command
    :param bot: pyrogram.Client
    :param update: pyrogram.types.Message
    :return: None
    """
    config = Config()
    # if message received in group or channel
    if update.chat:
        # if message received in group
        if update.from_user:
            # if sender sending from pm
            if update.from_user.id == update.chat.id:
                if update.from_user.id in config.ADMINS:
                    if update.command[-1] != "remove":
                        try:
                            chat_id = int(update.command[-1])
                        except ValueError:
                            await update.reply_text(
                                text="Please enter a valid group id to remove from the target list!"
                            )
                        else:
                            if chat_id in config.TARGET_GROUP_IDS:
                                await update.reply_text(
                                    text=TextButton.get_group_removed_text()
                                )
                                config.data["target_group_ids"].remove(chat_id)
                                config.write_data()
                                chat = await bot.get_chat(
                                    chat_id=chat_id
                                )
                                for admin in config.ADMINS:
                                    if admin not in config.NO_NOTIFICATION_ADMINS:
                                        if admin != update.from_user.id:
                                            await bot.send_message(
                                                chat_id=admin,
                                                text=f"""
{update.from_user.mention} removed target group!
Group Name: {chat.title}
Group ID: {str(chat.id)}
Members Count: {str(chat.members_count)}"""
                                            )
                            else:
                                await update.reply_text(
                                    text="Group not added in the target list!"
                                )

                    else:
                        await update.reply_text(
                            text=f"""
Invalid parameter provided!

*To remove a group:
send /remove in the group
or send /remove group_id in the inbox!

* To view all the target groups, send /groups"""
                        )
                else:
                    await update.reply_text(
                        text=TextButton.get_others_notification_text()
                    )

            # if sender is admin and not sending from pm
            elif update.from_user.id in config.ADMINS:
                # if chat in target
                if update.chat.id in config.TARGET_GROUP_IDS:
                    await update.reply_text(
                        text=TextButton.get_group_removed_text()
                    )
                    config.data["target_group_ids"].remove(update.chat.id)
                    config.write_data()
                    for admin in config.ADMINS:
                        if admin not in config.NO_NOTIFICATION_ADMINS:
                            if admin != update.from_user.id:
                                await bot.send_message(
                                    chat_id=admin,
                                    text=f"""
{update.from_user.mention} removed target group!
Group Name: {update.chat.title}
Group ID: {str(update.chat.id)}
Members Count: {str(update.chat.members_count)}"""
                                )
