import logging
import time

from . import settings, slack
from .markov import Markov
from .models import Message, User

logger = logging.getLogger(__name__)


def process_message(event):
    msg = Message.from_event(event)
    print('1')

    from .models import me
    if msg.user == me:  # ignoring messages coming from me
        return
    print('2')

    channel = msg.channel.name

    if channel not in settings.channels:
        return
    print('3')
    input_message = str(msg.text)
    input_username = msg.user.login

    channels = find_the_other_channel(channel)
    print(channels)
    markov = Markov(channels['original_id'])
    markov.learn(input_message)

    markov_message = markov.speak(input_message)
    if not markov_message:
        print('no message...')
        return

    slack.send_msg(
        username=input_username,
        channel=channels['other'],
        msg=markov_message,
    )


def find_the_other_channel(channel):
    print(channel)
    channels_fake, channels_original = settings.channels_fake, settings.channels_original

    if channel in channels_fake:
        other_channel = channels_original[channels_fake.index(channel)]
        channels = {'fake': channel, 'original': other_channel, 'other': other_channel}
        print("it's fake")

    if channel in channels_original:
        other_channel = channels_fake[channels_original.index(channel)]
        channels = {'original': channel, 'fake': other_channel, 'other': other_channel}
        print("it's real")

    channels['original_id'] = slack.get_channel_from_channel_name(channels['original'])['id']
    channels['fake_id'] = slack.get_channel_from_channel_name(channels['fake'])['id']
    channels['other_id'] = slack.get_channel_from_channel_name(channels['other'])['id']

    return channels

# we might not need this
def process_presence_change(event):
    if event['presence'] == 'active':
        User.from_event(event)
        # user.send_msg(...)


def process(event):
    if not 'type' in event:
        return

    logger.debug('Processing %s' % event)
    if event['type'] == 'message':
        if not event.get('subtype', None): #original message, edits etc have subtypes
            process_message(event)


def run():
    slack.client.rtm_connect()
    logger.info('Connected, ready for customers!')

    while True:
        data = slack.client.rtm_read()
        for event in data:
            try:
                process(event)
            except KeyboardInterrupt:
                logger.info('Going to bed.')
                return
            except:
                logger.exception('Failed to process event.')

        try:
            time.sleep(settings.ENGINE_CYCLE_SLEEP)
        except KeyboardInterrupt:
            logger.info('Going to bed.')
            return
