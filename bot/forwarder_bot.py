"""
- Main script, responsible for creating bot clients, starting them, and listening to updates
"""

from pyrogram import Client

from bot.config import Config
from bot.log import logger

config = Config()


class ForwarderBot(Client):
    """
    ForwarderBot class to represent and manage bot client
    """
    def __init__(self):
        """
        Initializing the instances of ForwarderBot class
        """
        super().__init__(
            name=self.__class__.__name__.lower(),
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            plugins={"root": "bot/plugins"},
            sleep_threshold=180
        )

    async def start(self) -> None:
        """
        Starts the main bot client and listens for updates
        :return: None
        """
        client: Client = await super().start()
        me = await client.get_me()
        logger.info("bot started")
        print(f"Forwarder bot started on {me.username}")

    async def stop(self, *args):
        """
        Stops the main client and stops the program as well
        :param args: list of args
        :return: None
        """
        await super().stop()
        logger.info("bot stopped")
        print("Bye")
