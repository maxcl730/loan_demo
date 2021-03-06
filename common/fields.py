# -*- coding: utf-8 -*-
import json
from html.parser import HTMLParser
from flask_restful import fields


class HTMLField(fields.Raw):
    """Define a new fields for filter the HTML tags string."""
    def format(self, value):
        return strip_tags(str(value))


class HTMLStripper(HTMLParser):
    """HTML Parser of Stripper."""
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, data_object):
        self.fed.append(data_object)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    """Filter the tags string of HTML for data object of Restful api."""
    stripper = HTMLStripper()
    stripper.feed(html)

    return stripper.get_data()


def str2json(value=''):
    try:
        result = json.loads(value)
    except json.decoder.JSONDecodeError:
        return ''
    return result


def show_unicode(unicode_str=''):
    if type(unicode_str) == str:
        return unicode_str.encode("utf-8").decode("unicode-escape")
    else:
        return 'Null'
