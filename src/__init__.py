from . import models, slack


def init():
    slack.init()
    models.init()


init()
