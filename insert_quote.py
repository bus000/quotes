#!/usr/bin/python

import json
import os
import sys

minimum_distance = 10

# Calculate the distance between two strings as the number of changes needed to
# go from one string to the other.  Implementation stolen from
# en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def yes(decision):
    return decision == '' or decision.lower() == 'yes' or\
        decision.lower() == 'y'

if __name__ == '__main__':
    quote_list = None
    quotes_json = None
    current_dir = os.path.dirname(os.path.realpath(__file__))
    with open(current_dir + '/quotes.json') as f:
        quotes_json = json.load(f)
        quote_list = quotes_json['quotes']

    if len(sys.argv) != 3:
        print('Script expects 2 arguments, an author and a quote.')
        sys.exit()

    new_author = str(sys.argv[1])
    new_quote = str(sys.argv[2])

    for quote in quote_list:
        quote = quote['content']
        if levenshtein_distance(new_quote, quote) < minimum_distance:
            print('The new quote\n\n"', new_quote, '"\n')
            print('is very similar to the quote\n\n\"', quote, '"\n')

            user_in = input('Do you still want to insert it? [Y/n] ')

            if not yes(user_in):
                sys.exit()

    quote_list.append({'author': new_author, 'content': new_quote})
    with open(current_dir + '/quotes.json', 'w') as f:
        f.write(json.dumps(quotes_json))
