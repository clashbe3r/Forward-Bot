"""
- This script handles the job of reading and writing data from and to the config.json file
"""
import json
import sys
from typing import Dict, List, Union

from bot.log import logger


class Config:
    """
    _ Config class to get and manage config data
    """
    _CONFIG_FILE_PATH = "bot/config/config.json"

    def __init__(self):
        """
        Initializing the Config class instances
        """
        self.data: Dict[str, Union[int, str, bool, List[int]]] = self._read_data()
        self.API_ID: int = self._get_api_id()
        self.API_HASH: str = self._get_api_hash()
        self.BOT_TOKEN: str = self._get_bot_token()
        self.ADMINS: List[int] = self._get_admins()
        self.SOURCE_CHANNEL_ID: int = self._get_source_channel_id()
        self.TARGET_GROUP_IDS: List[int] = self._get_target_groups()
        self.ADMIN_VERIFICATION_STATUS: bool = self._get_admin_verification_status()
        self.NO_NOTIFICATION_ADMINS: List[int] = self._get_no_notification_admins()
        # self.EVERYONE_MODE_STATUS: bool = self._get_everyone_mode_status()

    def _read_data(self) -> Dict[str, Union[int, str, bool, List[int]]]:
        """
        Reads the data from the config file and return the serialized data as dict
        :return: Dict[str, Union[int, str, List[int]]
        """
        with open(self._CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("config file(bot/config/config.json) file is mal-formatted!")
                logger.error("config file mal-formatted")
                sys.exit()
            else:
                return data

    def write_data(self) -> None:
        """
        Writes data back to the config file
        :return: None
        """
        with open(self._CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)
        logger.info("written data to config file!")

    def _get_api_id(self) -> int:
        """
        Gets the api id from the config file and returns it to set to the attributes of the instance
        :return: int - API ID of the telegram account
        """
        try:
            api_id = int(self.data["api_id"])
        except KeyError:
            print("api_id key not found in the config file")
            logger.error("api_id key not found")
            sys.exit()
        except ValueError:
            print("api_id is invalid")
            logger.error("api_id is non integer")
            sys.exit()
        else:
            return api_id

    def _get_api_hash(self) -> str:
        """
        Gets the api hash from the config file and returns
        :return: str - API HASH of the telegram account
        """
        try:
            api_hash = self.data["api_hash"]
        except KeyError:
            print("api_hash key not found")
            logger.error("api_hash key not found")
            sys.exit()
        else:
            if not api_hash:
                print("api_hash invalid")
                logger.error("api_hash empty")
                sys.exit()
            else:
                return api_hash

    def _get_bot_token(self) -> str:
        """
        Gets the bot token from the config file and returns it
        :return: str - BOT TOKEN of the bot we are going to use
        """
        try:
            bot_token = self.data["bot_token"]
        except KeyError:
            print("bot_token key not found")
            logger.error("bot_token key not found")
            sys.exit()
        else:
            if not bot_token:
                print("bot_token invalid")
                logger.error("bot_token empty")
                sys.exit()
            else:
                return bot_token

    def _get_admins(self) -> List[int]:
        """
        Gets the list of admins and returns the list
        :return: List[int] - int - telegram user id of the admin
        """
        try:
            admins = self.data["admins"]
        except KeyError:
            print("admins key not found in config file")
            logger.error("admins key not found")
            sys.exit()
        else:
            if not isinstance(admins, list):
                print("admins are invalid")
                logger.error("admins key doesn't represent list of user_ids")
                sys.exit()
            else:
                return admins

    def _get_source_channel_id(self) -> int:
        """
        Gets and returns the id of the source channel
        :return: int - id of the source channel
        """
        try:
            source_channel_id = int(self.data["source_channel_id"])
        except KeyError:
            print("source_channel_id key not found in the config file")
            logger.error("source_channel_id key not found")
            sys.exit()
        else:
            return source_channel_id

    def _get_target_groups(self) -> List[int]:
        """
        Gets and returns the ids of the target groups
        :return: int
        """
        try:
            target_group_ids = self.data["target_group_ids"]
        except KeyError:
            print("target_group_ids key not found in the config file")
            logger.error("target_group_ids key not found")
            sys.exit()
        else:
            if not isinstance(target_group_ids, list):
                print("target_group_ids is not valid")
                logger.error("target_group_ids is not a list")
                sys.exit()
            else:
                return target_group_ids

    def _get_admin_verification_status(self) -> bool:
        """
        Returns the status of admin verification
        :return: bool, True- admin needs to verify every setup, False - Admins don't need to verify
        """
        try:
            verification_status: bool = self.data["admin_verification"]
        except KeyError:
            print("admin_verification key not found in the config file")
            logger.error("admin_verification key not found")
            sys.exit()
        else:
            return verification_status
    #
    # def _get_everyone_mode_status(self) -> bool:
    #     """
    #     Returns the status of everyone mode
    #     :return: bool
    #     """
    #     try:
    #         everyone_mode: bool = self.data["everyone_mode"]
    #     except KeyError:
    #         print("everyone_mode key not found in the config file")
    #         logger.error("everyone_mode key not found")
    #         sys.exit()
    #     else:
    #         return everyone_mode

    def _get_no_notification_admins(self) -> List[int]:
        """
        Returns the ids of the admins those don't want notifications
        :return: List[int] - List of admin ids
        """
        try:
            no_notification_admins = self.data["no_notification_admins"]
        except KeyError:
            print("no_notification_admins key not found in the config file")
            logger.error("no_notification_admins key not found")
            sys.exit()
        else:
            if not isinstance(no_notification_admins, list):
                print("no_notification_admins invalid")
                logger.error("no_notification_admins is not a list")
                sys.exit()
            else:
                return no_notification_admins
