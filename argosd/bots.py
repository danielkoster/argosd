"""This module contains functionality related to bots.

TelegramBot: A bot to interact with a user on Telegram.
"""
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from argosd import settings
from argosd.threading import Threaded


class TelegramBot(Threaded):
    """A bot that offers interactive communication on Telegram.
    It notifies the user of any downloaded episodes."""

    _updater = None
    _chat_id_file = None

    def __init__(self):
        super().__init__()

        self._chat_id_file = '{}/argosd_chat_id'.format(settings.ARGOSD_PATH)

        # Updater for interactive commands
        self._updater = Updater(token=settings.TELEGRAM_BOT_TOKEN)

    def send_message(self, text):
        """Sends a message to the user without the need for
        initial input from the user."""
        chat_id = None
        with open(self._chat_id_file, 'r') as file:
            chat_id = file.read()

        if chat_id:
            self._updater.bot.send_message(chat_id=chat_id, text=text)
        else:
            logging.info('No chat ID found. Conversation with bot probably '
                         'not yet started.')

    def _stop(self):
        """Stops the updater before stopping the thread."""
        self.send_message('ArgosD is shutting down.')
        self._updater.stop()

    def deferred(self):
        """Runs the TelegramBot, adds command handlers and waits for input."""
        self.send_message('ArgosD is running again!')

        start_handler = CommandHandler('start', self._command_start)
        self._updater.dispatcher.add_handler(start_handler)

        echo_handler = MessageHandler(Filters.text, self._command_echo)
        self._updater.dispatcher.add_handler(echo_handler)

        unknown_handler = MessageHandler(Filters.command,
                                         self._command_unknown)
        self._updater.dispatcher.add_handler(unknown_handler)

        self._updater.start_polling()

    @staticmethod
    def _command_start(bot, update):
        # Save the chat ID to a file for future reference
        filename = '{}/argosd_chat_id'.format(settings.ARGOSD_PATH)
        with open(filename, 'w') as file:
            file.write(str(update.message.chat_id))

        message = 'Hi! I\'m ArgosD, keeping track of your TV shows. ' \
                  'I\'ll send you notifications whenever ' \
                  'new episodes are downloaded.'
        bot.send_message(chat_id=update.message.chat_id, text=message)

    @staticmethod
    def _command_echo(bot, update):
        message = 'Sorry, I don\'t speak that language. '
        bot.send_message(chat_id=update.message.chat_id, text=message)

    @staticmethod
    def _command_unknown(bot, update):
        message = 'Sorry, I didn\'t understand that command.'
        bot.send_message(chat_id=update.message.chat_id, text=message)
