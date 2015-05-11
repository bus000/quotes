#!/usr/bin/python2.7

import xml.etree.ElementTree as ET
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

def strip_space(string):
    new_string = ""
    last_char = ""

    for c in string:
        if last_char.isspace() and c.isspace():
            last_char = c
        else:
            new_string += c
            last_char = c

    return new_string

def get_quotes(root):
    # Get list of all quotes as strings.
    quote_list = root.findall('./quote/content')
    quote_strings = map((lambda quote: quote.text), quote_list)
    return map(strip_space, quote_strings)

def yes(decision):
    return decision == '' or decision.lower() == 'yes' or\
        decision.lower() == 'y'

def insert(root, author, quote):
    quote_tree = ET.Element('quote')

    author_tree = ET.Element('author')
    author_tree.text = author

    content_tree = ET.Element('content')
    content_tree.text = quote

    quote_tree.append(author_tree)
    quote_tree.append(content_tree)

    root.append(quote_tree)

if __name__ == '__main__':
    # Read xml file.
    tree = ET.parse(os.path.dirname(os.path.realpath(__file__)) + '/quotes.xml')
    root = tree.getroot()

    if len(sys.argv) != 3:
        print 'Script expects 2 arguments, an author and a quote.'
        sys.exit()

    new_author = str(sys.argv[1])
    new_quote = str(sys.argv[2])

    all_quotes = get_quotes(root)

    for quote in all_quotes:
        if levenshtein_distance(new_quote, quote) < minimum_distance:
            print 'The new quote\n\n"', new_quote, '"\n'
            print 'is very similar to the quote\n\n\"', quote, '"\n'

            user_in = raw_input('Do you still want to insert it? [Y/n] ')

            if not yes(user_in):
                sys.exit()
            else:
                break

    insert(root, new_author, new_quote)
    tree.write(os.path.dirname(os.path.realpath(__file__)) + '/quotes.xml',
            encoding='utf-8')
