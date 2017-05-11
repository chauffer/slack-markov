import os

SLACK_API_TOKEN = os.environ['MARKOV_SLACK_API_TOKEN']

SLACK_CHANNEL_MAP = os.getenv('MARKOV_SLACK_CHANNEL_MAP', 'devs-off-topic:devs-on-topic').split(',') # "original:fake,original:fake"

channels, channels_original, channels_fake = [], [], []

for channel_map in SLACK_CHANNEL_MAP:
    c_map = SLACK_CHANNEL_MAP.split(':')

    channels_original.append(c_map[0])
    channels_fake.append(c_map[1])
    channels.append([c_map[0], c_map[1]])
