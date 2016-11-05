"""This module contains functionality related to bots.

TelegramBot: A bot to interact with a user on Telegram.
"""
import os
import re
import logging

from peewee import DoesNotExist
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    CallbackQueryHandler

from argosd import settings
from argosd.models import Episode
from argosd.parallelising import Multiprocessed
from argosd.torrentclient import Transmission, TorrentClientException


class TelegramBot(Multiprocessed):
    """A bot that offers interactive communication on Telegram.
    It notifies the user of any downloaded episodes."""

    _updater = None
    _chat_id_file = None

    def __init__(self):
        super().__init__()

        self._chat_id_file = '{}/argosd_chat_id'.format(settings.ARGOSD_PATH)

        # Updater for interactive commands
        self._updater = Updater(token=settings.TELEGRAM_BOT_TOKEN)

    def deferred(self):
        """Runs the TelegramBot, adds handlers and waits for input."""
        logfile = '{}/telegrambot.log'.format(settings.LOG_PATH)
        logformat = '%(message)s'

        logging.basicConfig(format=logformat, level=logging.INFO,
                            filename=logfile, filemode='a')

        self._create_handlers()

        self.send_message('ArgosD is running again!')

        self._updater.start_polling()

    def _create_handlers(self):
        start_handler = CommandHandler('start', self._command_start)
        self._updater.dispatcher.add_handler(start_handler)

        echo_handler = MessageHandler(Filters.text, self._command_echo)
        self._updater.dispatcher.add_handler(echo_handler)

        unknown_handler = MessageHandler(Filters.command,
                                         self._command_unknown)
        self._updater.dispatcher.add_handler(unknown_handler)

        button_handler = CallbackQueryHandler(self._handle_button)
        self._updater.dispatcher.add_handler(button_handler)

        self._updater.dispatcher.add_error_handler(self._handle_error)

    def before_stop(self):
        """Stops the updater before stopping the process."""
        self.send_message('ArgosD is shutting down.')
        self._updater.stop()

    def send_message(self, text, *args, **kwargs):
        """Sends a message to the user without the need for
        initial input from the user."""
        chat_id = self._get_chat_id()

        if chat_id:
            kwargs['text'] = text
            kwargs['chat_id'] = chat_id
            self._updater.bot.send_message(*args, **kwargs)
        else:
            logging.warning('No chat ID found. Conversation with bot probably '
                            'not yet started.')

    def _get_chat_id(self):
        chat_id = None
        if os.path.isfile(self._chat_id_file):
            with open(self._chat_id_file, 'r') as file:
                chat_id = file.read()

        return chat_id

    def _command_start(self, bot, update):
        # Save the chat ID to a file for future reference
        with open(self._chat_id_file, 'w') as file:
            file.write(str(update.message.chat_id))

        message = 'Hi! I\'m ArgosD, keeping track of your TV shows. ' \
                  'I\'ll send you notifications whenever ' \
                  'new episodes are downloaded.'
        bot.send_message(chat_id=update.message.chat_id, text=message)

    @staticmethod
    def _command_echo(bot, update):
        message = 'Sorry, I don\'t speak that language.'
        bot.send_message(chat_id=update.message.chat_id, text=message)

    @staticmethod
    def _command_unknown(bot, update):
        message = 'Sorry, I didn\'t understand that command.'
        bot.send_message(chat_id=update.message.chat_id, text=message)

    @staticmethod
    def _handle_error(bot, update, error):
        del bot  # Unused
        logging.error('Update "%s" caused error "%s"' % (update, error))

    def _handle_button(self, bot, update):
        query = update.callback_query
        text = query.message.text
        reply_markup = None

        if query.data.startswith('download'):
            if self._process_download_command(query.data):
                text += '\n[Episode downloaded]'
            else:
                text += '\n[Error downloading episode]'
                reply_markup = self.create_button_markup('Download now',
                                                         query.data)
        else:
            logging.warning('Unknown command received: %s' % query.data)

        bot.edit_message_text(text=text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=reply_markup)

    @staticmethod
    def _process_download_command(data):
        matches = re.search('download (\d{1,})', data)
        if matches is not None:
            episode_id = int(matches.group(1))
            try:
                episode = Episode.get(Episode.id == episode_id)
                torrentclient = Transmission()

                torrentclient.download_episode(episode)
                episode.is_downloaded = True
                episode.save()
                return True
            except DoesNotExist:
                error = 'Tried to download non-existing episode with ID: %d'
                logging.error(error % episode_id)
                return False
            except TorrentClientException as e:
                logging.error('TorrentClientException occured: %s' % str(e))
                return False
        else:
            logging.error('Incorrect download command received: %s' % data)
            return False

    @staticmethod
    def create_button_markup(text, callback_data):
        """Creates markup for a single inline keyboard button in a message."""
        keyboard = [[InlineKeyboardButton(text, callback_data=callback_data)]]
        return InlineKeyboardMarkup(keyboard)
