from argosd.settings_default import *


"""The URL to your RSS-feed. This should be a feed containing a channel
with items that have a title and a link."""
RSS_FEED = ''

"""Specify how we can connect to the Transmission server.
An RPC connection is made, so check these settings in Transmission."""
TRANSMISSION_HOST = 'localhost'
TRANSMISSION_PORT = 9091
TRANSMISSION_USERNAME = ''
TRANSMISSION_PASSWORD = ''

"""Create an API token. You will have to send this token
with each API request you make. Keep it safe!"""
API_TOKEN = ''

"""Defines how the directories where downloads are saved are structured.
Possible options are:
1 = Shows are lowercased, spaces replaced by periods.
2 = Shows are grouped per season, foldernames can contain spaces.
    This is particularly suited for Plex."""
DOWNLOAD_STRUCTURE_STRATEGY = 1

"""Optional override for the download directory where the torrentclient
will download the episodes to. If set to None, episodes will be downloaded
to the default location as determined by the torrentclient."""
TORRENTCLIENT_DOWNLOAD_DIR = None

"""Optional token for Telegram bot. This bot will send you notifications
whenever a new episode is downloaded."""
TELEGRAM_BOT_TOKEN = None
