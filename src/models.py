from . import settings, slack


class SlackAbstract:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def send_file(self, file, title=None, msg=None):
        slack.upload_file(file, title, msg, channels=self.at)


class User(SlackAbstract):

    def __repr__(self):
        return '<User %s>' % self.login

    def __str__(self):
        return self.login

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.login == other.login
        return False

    @classmethod
    def from_id(cls, id):
        if id.startswith('@'):
            id = id[1:]

        user = cls()
        user.id = id
        user.info = slack.get_user_info(id)
        user.login = user.info['name']
        return user

    @classmethod
    def from_login(cls, login):
        if login.startswith('@'):
            login = login[1:]

        user = cls()
        user.login = login
        user.info = next(filter(lambda u: u['name'] == login,
                                slack.get_users_list()
                        ))
        user.id = user.info['id']
        return user

    @classmethod
    def from_event(cls, event):
        if 'user' in event:
            return cls.from_id(event['user'])

    def __getattr__(self, name):
        if 'profile' in self.info and name in self.info['profile']:
            return self.info['profile'][name]
        return self.info[name]

    @property
    def at(self):
        return '@%s' % self.login

    @property
    def id_at(self):
        return '<@%s>' % self.id

    @property
    def is_me(self):
        return self == me

    @property
    def name(self):
        return self.first_name or self.login

    #@property
    #def image(self):
    #    from grab import Grab
    #    from .images import Image

    #    g = Grab()
    #    resp = g.go(self.image_original)
    #    # not saving, because it's probably gonna be edited
    #    return Image(resp.body)

    def send_msg(self, msg):
        slack.send_msg(msg, user=self.login)


class Channel(SlackAbstract):

    def __repr__(self):
        return '<Channel %s>' % self.name

    def __str__(self):
        return self.name

    @classmethod
    def from_id(cls, id):
        if id.startswith('#'):
            id = id[1:]

        chan = cls()
        chan.id = id
        chan.info = slack.get_channel_info(id)
        chan.name = chan.info['name']
        return chan

    @classmethod
    def from_event(cls, event):
        if 'channel' in event:
            if event['channel'][0] == 'D':
                # not a channel, but a private message
                return
            return cls.from_id(event['channel'])

    def __getattr__(self, name):
        return self.info[name]

    @property
    def at(self):
        return '#%s' % self.name

    def send_msg(self, msg):
        slack.send_msg(msg, channel=self.name)


class Message(SlackAbstract):

    def __repr__(self):
        origin = self.channel or self.user
        return '<Message (%s): %s>' % (origin, self.text)

    def __str__(self):
        return self.text

    @classmethod
    def from_event(cls, event):
        msg = cls()
        msg.event = event
        msg.channel_id = event['channel']
        msg.channel = Channel.from_event(event)
        msg.user = User.from_event(event)
        return msg

    @property
    def is_direct(self):
        return not self.channel

    @property
    def reply_channel(self):
        return self.user if self.is_direct else self.channel

    @property
    def am_i_mentioned(self):
        return (me.login.lower() in self.text.lower()
                or me.name.lower() in self.text.lower()
                or '@%s' % me.id in self.text)

    def __getattr__(self, name):
        return self.event[name]

    def tag_emoji(self, emoji):
        slack.add_reaction(emoji, chan_id=self.channel_id, ts=self.ts,
                           _dest=self)


def init():
    global me
    me = User.from_id(settings.SLACK_BOT_ID)
