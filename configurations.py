import logging
import os

import pytz as tz

# singleton for logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
LOGGER = logging.getLogger('crypto_rl_log')

BITFINEX_ENDPOINT = 'wss://api.bitfinex.com/ws/2'
MAX_RECONNECTION_ATTEMPTS = 100
TIMEZONE = tz.utc