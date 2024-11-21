"""
- This script is responsible for handling the setup message received by the user
"""

from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import Config
from bot.utils.text_button import TextButton


async def handle_setup_command(bot: Client, update: Message) -> None:
    """
    Handles the setup command message received
    :param bot: Client
    :param update: pyrogram.types.Message
    :return: None
    """
    if update.chat:
        if update.from_user:
            if update.chat.id == update.from_user.id:
                config = Config()
                if update.chat.id in config.ADMINS:
                    await update.reply_text(
                        text="You can send /setup in groups to add those groups as target groups!"
                    )
                    return None
                else:
                    await update.reply_text(
                        text=TextButton.get_others_notification_text()
                    )
                    return None
    # if received from group or channel
    if update.chat:
        # if received from group
        if update.from_user:
            config = Config()
            # if the message is received from admins
            if update.from_user.id in config.ADMINS:
                if update.chat.id not in config.TARGET_GROUP_IDS:
                    # if verification is turned on
                    if config.ADMIN_VERIFICATION_STATUS:
                        await update.reply_text(
                            text=TextButton.get_check_inbox_text()
                        )
                        await bot.send_message(
                            chat_id=update.from_user.id,
                            text=TextButton.get_verify_inbox_text().replace("{group_name}", update.chat.title).replace(
                                "{group_id}", str(update.chat.id)).replace("{members_count}",
                                                                           str(update.chat.members_count)),
                            reply_markup=InlineKeyboardMarkup(
                                [
                                    [
                                        InlineKeyboardButton(
                                            text="Add ✅",
                                            callback_data=f"add_{update.from_user.id}_{update.chat.id}"
                                        ),
                                        InlineKeyboardButton(
                                            text="Don't add ❌",
                                            callback_data="dont"
                                        )
                                    ]
                                ]
                            )
                        )
                    # if verification is off
                    else:
                        await update.reply_text(
                            text=TextButton.get_setup_complete_group_text()
                        )
                        config.data["target_group_ids"].append(update.chat.id)
                        config.write_data()
                        for admin in config.ADMINS:
                            if admin not in config.NO_NOTIFICATION_ADMINS:
                                if admin != update.from_user.id:
                                    await bot.send_message(
                                        chat_id=admin,
                                        text=TextButton.get_group_added_notification_text().replace(
                                            "{mention}", update.from_user.mention).replace(
                                            "{group_name}", update.chat.title).replace("{group_id}",
                                                                                       str(update.chat.id))
                                    )

                else:
                    await update.reply_text(
                        text="Already added in the list!"
                    )
