import logging
from slackclient import SlackClient
from . import settings


logger = logging.getLogger(__name__)


def init():
    global client
    client = SlackClient(settings.SLACK_API_TOKEN)


def api_call(*args, **kwargs):
    res = client.api_call(*args, **kwargs)
    assert res['ok'] == True, res
    return res


def get_user_info(user_id):
    return api_call('users.info', user=user_id)['user']


def send_msg(msg, dest=None, user=None, channel=None):
    if user:
        dest = '@%s' % user
    elif channel:
        dest = '#%s' % channel
    assert dest, 'No recipient set.'

    from .models import me
    if dest == me.at:
        # don't talk to yourself
        return

    logger.info('Sending to %s: %s' % (dest, msg))
    return api_call('chat.postMessage', channel=dest, text=str(msg),
                    as_user=True)


def add_reaction(emoji, chan_id=None, ts=None, _dest=None):
    if chan_id and ts:
        logger.info('Giving emoji to %s: %s' % (_dest, emoji))
        api_call('reactions.add', name=emoji, channel=chan_id,
                 timestamp=ts)




# probably we don't need this
def get_users_list():
    return api_call('users.list')['members']
def get_channel_info(chan_id):
    return api_call('channels.info', channel=chan_id)['channel']
def upload_file(file, title=None, msg=None, channels=None):
    if getattr(file, 'file', None):
        # e.g. type(file) == bot.images.Image
        file = file.file

    if not title:
        title = ''
    if not msg:
        msg = ''

    logger.info('Uploading %s to %s' % (title, channels))
    return api_call('files.upload', file=file,
                    title=title, initial_comment=msg,
                    channels=channels)

