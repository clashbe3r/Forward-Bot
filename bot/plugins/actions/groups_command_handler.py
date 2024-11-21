"""
- This script is responsible for handling the groups command
"""

from pyrogram.types import Message

from bot.config import Config
from bot.utils.text_button import TextButton


async def handle_groups_command(update: Message) -> None:
    """
    Handles the groups command
    :param update: pyrogram.types.Message
    :return:None
    """
    if update.from_user.id == update.chat.id:
        config = Config()
        if update.from_user.id in config.ADMINS:
            text = f"ALL TARGET GROUP'S DETAILS:\nTOTAL GROUPS: {len(config.TARGET_GROUP_IDS)}\n\n"
            count = 0
            for i, group in enumerate(config.TARGET_GROUP_IDS):
                text += f"{group}\n"
                count += 1
                if count == 20:
                    await update.reply_text(
                        text=text
                    )
                    count = 0
                    text = ""
            if text:
                await update.reply_text(
                    text=text
                )
        else:
            await update.reply_text(
                text=TextButton.get_others_notification_text()
            )
