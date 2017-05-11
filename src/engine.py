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

    channels = get_channel_set(channel)
    is_readonly = is_channel_set_readonly(channel)
    is_primary = bool(get_primary_channel(channel) == channel)
    if is_readonly and not is_primary:
        return
    markov = Markov(slack.get_channel_from_channel_name(get_primary_channel(channel))['id'])
    markov.learn(input_message)

    markov_message = markov.speak(input_message)
    if not markov_message:
        return

    dest_channel = get_other_channel(channel)

    if is_readonly:
        dest_channel = get_other_channel(get_primary_channel(channel))
        if channel == dest_channel:
            return

    slack.send_msg(
        username=input_username,
        channel=dest_channel,
        msg=markov_message,
    )


def get_primary_channel(channel):
    channels_fake, channels_original = settings.channels_fake, settings.channels_original

    if channel in channels_fake:
        return channels_original[channels_fake.index(channel)]
    if channel in channels_original:
        return channel


def get_other_channel(channel):
    channels_fake, channels_original = settings.channels_fake, settings.channels_original

    if channel in channels_fake:
        other_channel = channels_original[channels_fake.index(channel)]
    if channel in channels_original:
        other_channel = channels_fake[channels_original.index(channel)]
    return other_channel


def is_channel_set_readonly(channel):
    channels = [channel, get_other_channel(channel)]
    for channel in channels:
        if channel in settings.SLACK_CHANNEL_READONLY:
            return True
    return False


def get_channel_set(channel):
    return [get_primary_channel(channel), get_other_channel(get_primary_channel(channel))]

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
