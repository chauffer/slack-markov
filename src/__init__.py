from . import models, slack


def init():
    slack.init()
    models.init()


init()  # when testing & mocking, don't run this
