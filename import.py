import json
import os
from pprint import pprint

from src import markov as m

BRAIN = os.getenv('MARKOV_BRAIN_ID', 'C0SEHHVKQ') # devs-off-topic

markov = m.Markov(BRAIN)

files = [f for f in os.listdir('to_import')]
for i in files:
    with open(f'to_import/{i}', 'r') as f:
        content = json.loads(f.read())
    messages = [message['text'] for message in content if message['type'] == 'message' and 'subtype' not in message]
    for message in messages:
        print('learning...')
        markov.learn(message)
