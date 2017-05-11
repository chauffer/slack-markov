from src import engine, settings


settings.SLACK_CHANNELS = [
    (('stand-up', False), ('stand-down', True)),
    (('hack-days-markov', True), ('hack-days-markov-2', True)),
]


def test_get_the_other_channel():
    assert engine.get_the_other_channel('stand-up') == 'stand-down'
    assert engine.get_the_other_channel('hack-days-markov-2') \
           == 'hack-days-markov'


def test_is_channel_writeable():
    assert engine.is_channel_writeable('hack-days-markov')
    assert not engine.is_channel_writeable('stand-up')
