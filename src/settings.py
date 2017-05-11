import logging.config
import os

SLACK_API_TOKEN = os.environ['MARKOV_SLACK_API_TOKEN']
SLACK_BOT_ID = os.getenv('MARKOV_SLACK_BOT_ID', 'U2C3DJYAJ')

# "original:fake,original:fake"
SLACK_CHANNEL_MAP = os.getenv('MARKOV_SLACK_CHANNEL_MAP',
                              'hack-days-markov:hack-days-markov-2,'
                              'devs-off-topic:devs-on-topic,announcements:lost-earphones,'
                              'stand-up:stand-down').split(',')
SLACK_CHANNEL_READONLY = os.getenv('MARKOV_SLACK_CHANNEL_READONLY', 'announcements,stand-up').split(',')

ENGINE_CYCLE_SLEEP = float(os.getenv('MARKOV_ENGINE_CYCLE_SLEEP', '0.1'))


channels, channels_original, channels_fake = [], [], []

for channel_map in SLACK_CHANNEL_MAP:
    c_map = channel_map.split(':')

    channels_original.append(c_map[0])
    channels_fake.append(c_map[1])
    channels.append(c_map[0])
    channels.append(c_map[1])


LOGGING = lambda: {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'verbose': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s '
                      '%(filename)s:%(funcName)s:%(lineno)d | %(message)s',
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },

    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


LOGGING = LOGGING()
logging.config.dictConfig(LOGGING)
