#!/usr/bin/python

import json
import os
import sys
import getopt

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

def usage():
    print("usage:", sys.argv[0], "-a author -q quote")
    print("  -a: author of the quote")
    print("  -q: the quote to insert")

if __name__ == '__main__':
    try:
        long_args = ["help", "author", "quote"]
        opts, args = getopt.getopt(sys.argv[1:], "ha:q:", long_args)
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    new_author = None
    new_quote = None
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-a", "--author"):
            new_author = a
        elif o in ("-q", "--quote"):
            new_quote = a
        else:
            usage()
            sys.exit()

    if new_author is None or new_quote is None:
        usage()
        sys.exit()

    quote_list = None
    quotes_json = None
    current_dir = os.path.dirname(os.path.realpath(__file__))
    with open(current_dir + '/quotes.json') as f:
        quotes_json = json.load(f)
        quote_list = quotes_json['quotes']

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
