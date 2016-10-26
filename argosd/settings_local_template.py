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

"""Optional override for the download directory where the torrentclient
will download the episodes to. If set to None, episodes will be downloaded
to the default location as determined by the torrentclient."""
TORRENTCLIENT_DOWNLOAD_DIR = None
