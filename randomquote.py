#!/usr/bin/python

import json
import random
import textwrap
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
with open(current_dir + '/quotes.json') as json_file:
    quotes = json.load(json_file)
    quote_list = quotes['quotes']

    chosen_quote = random.choice(quote_list)
    print("\n".join(textwrap.wrap(chosen_quote['content'], 72)))
    print('   -' + chosen_quote['author'])
