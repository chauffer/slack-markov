from . import models, slack

def init():
    slack.init()
    models.init()


if __name__ == 'main':
    init()
