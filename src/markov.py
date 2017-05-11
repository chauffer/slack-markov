import os
import re

from cobe.brain import Brain


class Markov:
    def __init__(self, brain_id):
        self.brain_id = brain_id
        brain_path = f'data/cobe/{brain_id}'
        os.makedirs('data/cobe/', exist_ok=True)

        self.brain = Brain(brain_path)


    def filter(self, message):
        message = re.sub('\<@[A-Z0-9a-z]{9}\>', '', message) # remove mentions
        message = re.sub('\s{2,}', ' ', message) #remove double spaces
        message = re.sub('\<[^\<]+\>', '', message) #remove shit like links
        message = message.strip() # remove unneeded spaces
        valid = False
        if len(message) > 5:
            valid = True
        return [valid, message]

    def learn(self, message):
        valid, message = self.filter(message)
        if not valid:
            return
        self.brain.learn(message)


    def speak(self, message):
        response = self.brain.reply(message)
        valid, response = self.filter(response)
        if not valid:
            return None
        return response
