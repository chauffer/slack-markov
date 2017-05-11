import logging
import time

from . import slack, settings


logger = logging.getLogger(__name__)


def process_message(event):
    msg = Message.from_event(event)

    if msg.user == me:
        # ignoring messages coming from me
        return

    # TODO, e.g.
    # msg.user.send_msg(...)

# we might not need this
def process_presence_change(event):
    if event['presence'] == 'active':
        user = User.from_event(event)
        # TODO, e.g.
        # user.send_msg(...)


def process(event):
    if not 'type' in event:
        return

    logger.debug('Processing %s' % event)

    if event['type'] == 'presence_change':
        process_presence_change(event)

    elif event['type'] == 'message':
        if not event.get('subtype', None):
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
