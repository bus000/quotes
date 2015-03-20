#!/usr/bin/python

import xml.etree.ElementTree as ET
import random
import os

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

# Read xml file.
tree = ET.parse(os.path.dirname(os.path.realpath(__file__)) + '/quotes.xml')
root = tree.getroot()

# Find all quotes and choose a random.
quotes = root.findall('./quote')
i = random.randint(0, len(quotes)-1)
quote = strip_space(quotes[i].find('content').text)
author = '\n   - ' + (quotes[i].find('author').text.lstrip())

print quote + author
