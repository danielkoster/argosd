DEBUG = False

"""The path where ArgosD is installed."""
ARGOSD_PATH = '/opt/argosd'

"""The path where logs are stored."""
LOG_PATH = '/var/log/argosd'

"""If an episode with this quality is found,
it will be downloaded regardless of how long it might wait
for a better quality episode."""
QUALITY_THRESHOLD = 1080

# These settings are supposed to be overwritten in a settings_local file.
RSS_FEED = None
TRANSMISSION_HOST = None
TRANSMISSION_PORT = None
TRANSMISSION_USERNAME = None
TRANSMISSION_PASSWORD = None
TORRENTCLIENT_DOWNLOAD_DIR = None
TELEGRAM_BOT_TOKEN = None
