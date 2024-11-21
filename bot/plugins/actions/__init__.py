"""
- initialize the actions module
"""

from bot.plugins.actions.start_message_handler import handle_start_message
from bot.plugins.actions.setup_message_handler import handle_setup_command
from bot.plugins.actions.source_command_handler import handle_source_command
from bot.plugins.actions.remove_command_handler import handle_remove_command
from bot.plugins.actions.groups_command_handler import handle_groups_command
from bot.plugins.actions.forward_message_handler import handle_message_forwarding
