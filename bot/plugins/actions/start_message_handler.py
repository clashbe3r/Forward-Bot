"""
- This script process the start message and takes appropriate actions
"""

from pyrogram.types import Message

from bot.config import Config
from bot.utils.text_button import TextButton


async def handle_start_message(update: Message) -> None:
    """
    Process the start command
    :param update: pyrogram.types.Message - message received by the bot
    :return: None
    """
    config = Config()
    if update.from_user.id not in config.ADMINS:
        await update.reply_text(
            text=TextButton.get_others_notification_text()
        )
    else:
        config = Config()
        admins_count = len(config.ADMINS)
        target_groups_count = len(config.TARGET_GROUP_IDS)
        await update.reply_text(
            text=f"{TextButton.get_admin_welcome_text()}\n"
                 f"We have total {admins_count} user(s) with admin access!\n"
                 f"We have total {target_groups_count} group(s) setup as target.\n"
                 f"{'We also have source channel setup' if config.SOURCE_CHANNEL_ID else ''}\n"
                 f"To get any help related to commands, send /help."
        )
