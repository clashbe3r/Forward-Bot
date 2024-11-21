"""
- This script is responsible for getting all the texts and buttons that the bot needs to send to different
users
"""
import json
import sys

from bot.log import logger

_LANGUAGE_FILE_PATH = "bot/utils/english.json"
with open(_LANGUAGE_FILE_PATH, "r", encoding="utf-8") as f:
    try:
        language_data = json.load(f)
    except json.JSONDecodeError:
        print("language file is mal-formatted")
        logger.error("english.json file is mal-formatted")
        sys.exit()


class TextButton:
    """
    TextButton class to get Text and Buttons
    """

    @staticmethod
    def get_admin_welcome_text() -> str:
        """
        Returns the welcome text
        :return: str - welcome text for the admins
        """
        try:
            welcome_text = language_data["admin_welcome_text"]
        except KeyError:
            return "Howdy, admin. I'm online!"
        else:
            return welcome_text

    @staticmethod
    def get_others_notification_text() -> str:
        """
        Returns the text that needs to be sent when a normal user tries to send  a message to the bot
        :return: str - notification message that you are not allowed to use this bot
        """
        try:
            notification_text = language_data["notification_text"]
        except KeyError:
            return "Hey, you are not allowed use this bot. Contact admins to get permission!"
        return notification_text

    @staticmethod
    def get_check_inbox_text() -> str:
        """
        Returns the text that needs to be sent to the group when admin_verification is turned on
        :return: str - message text that needs to be sent
        """
        try:
            check_inbox_text = language_data["check_inbox_text"]
        except KeyError:
            return "Okay, check your inbox, to complete the setup!"
        else:
            return check_inbox_text

    @staticmethod
    def get_verify_inbox_text() -> str:
        """
        Returns the text that needs to be sent to the admin's inbox when admin_verification is turned on and
        admin tried to add a group to the forwarding list
        :return: str - message text that needs to be sent
        """
        try:
            verify_inbox_text = language_data["verify_inbox_text"]
        except KeyError:
            return "Do you want add?\nGroup Name: {group_name}\nGroup ID: {group_id}\nMembers Count: {members_count}"
        else:
            return verify_inbox_text

    @staticmethod
    def get_setup_complete_group_text() -> str:
        """
        Returns the text that needs to be sent to the group when setup completes
        :return: str - text
        """
        try:
            setup_complete_group_text = language_data["setup_complete_group_text"]
        except KeyError:
            return "Setup complete!\nI'll forward the messages to this group as well. 😃"
        else:
            return setup_complete_group_text

    @staticmethod
    def get_setup_complete_inbox_text() -> str:
        """
        Returns the text that needs to be sent when the admin completes the setup
        :return: str - text of the message
        """
        try:
            setup_complete_inbox_text = language_data["setup_complete_inbox_text"]
        except KeyError:
            return "Setup complete!\nI'll forward the messages to the group. 😃"
        else:
            return setup_complete_inbox_text

    @staticmethod
    def get_group_added_notification_text() -> str:
        """
        Returns the text that needs to be sent to the other admins when some admin adds a group to
        the forwarding list
        :return: str - text contain of the message
        """
        try:
            group_added_notification_text = language_data["group_added_notification_text"]
        except KeyError:
            return "{mention} added new group.\nGroup Name: {group_name}\nGroup ID: {group_id}"
        else:
            return group_added_notification_text

    @staticmethod
    def get_sent_text() -> str:
        """
        Returns the text that needs to be sent when bot forwards a message
        :return: str - text contain of the message
        """
        try:
            sent = language_data["sent"]
        except KeyError:
            return "sent"
        else:
            return sent

    @staticmethod
    def get_channel_added_text() -> str:
        """
        Returns the text that needs to be sent when a channel added as source
        :return: str
        """
        try:
            channel_added_text = language_data["channel_added_text"]
        except KeyError:
            return "Okay, I'll forward messages from this channel, this message will be auto deleted after 5 seconds!"
        else:
            return channel_added_text

    @staticmethod
    def get_another_channel_added_text() -> str:
        """
        Returns the text that needs to be sent when admin tries to add a channel and another channel is alreay added
        :return: str
        """
        try:
            another_channel_added_text = language_data["another_channel_added_text"]
        except KeyError:
            return "Another channel is already added as source, please remove that firs to add new channel. " \
                   "This message will be auto deleted after 5 seconds!"
        else:
            return another_channel_added_text

    @staticmethod
    def get_channel_removed_text() -> str:
        """
        Returns the text that needs to be sent when a channel is removed
        :return: str
        """
        try:
            channel_removed_text = language_data["channel_removed_text"]
        except KeyError:
            return "Channel removed from source!"
        else:
            return channel_removed_text

    @staticmethod
    def get_group_removed_text() -> str:
        """
        Returns the text that needs to be sent when a group is removed from the list
        :return: str
        """
        try:
            group_removed_text = language_data["group_removed_text"]
        except KeyError:
            return "Group removed from target list!"
        else:
            return group_removed_text
