#!/usr/bin/env python

import sys
import string
try:
    import urllib.request
except ImportError:
    print("This script doesn't compatalbe with python2.")
    print("Please run this script with python3.")
    print("exiting...")
    sys.exit()
from html.parser import HTMLParser

class YoudaoParser(HTMLParser):
    """parse data from dict.youdao.com"""
    def __init__(self):
        self.position = ''
        self.content = {
            'definition_zh':[], 'definition_en':[], 'definition_web':[]}
        super().__init__()
        self.strict = False

    def handle_data(self, data):
        if self.position:
            if self.position == 'definition_zh':
                for i in data:
                    # if has chinese character, append
                    if ord(i) > 128:
                        self.content['definition_zh'].append(data)
                        break
            elif self.position == 'definition_en':
                for i in data:
                    # if has chinese character, abort
                    if ord(i) > 128:
                        break
                else:
                    self.content['definition_en'].append(data)
            elif self.position == 'definition_web':
                for i in data:
                    data = data.strip('\n ')
                    # if has chinese character, append
                    if ord(i) > 128:
                        self.content['definition_web'].append(data)
                        break
            elif self.position == 'phonetic':
                # the second phonetic on webpage has bad format, so ignore it
                if not self.content.get('phonetic'):
                    self.content['phonetic'] = data
            elif self.position == 'title':
                # choose title like "con·gratu·late"
                if data.find('·') != -1:
                    self.content['title'] = data

    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            attrs = dict(attrs)
            if attrs.get('name') == 'keywords':
                self.content['keywords'] = attrs['content']
        if tag == 'span':
            for k, v in attrs:
                if k == 'class':
                    if v == 'title':
                        self.position = 'title'
                    elif v == 'phonetic':
                        self.position = 'phonetic'
                    elif v == 'def':
                        self.position = 'definition_en'
        if tag == 'div':
            for k, v in attrs:
                if k == 'class' and v == 'trans-container':
                    self.position = 'definition_zh' 
        # webtrans, for those have no normal translation
        if tag == 'a':
            if dict(attrs).get('title') == "详细释义":
                self.position = 'definition_web'

    def handle_endtag(self, tag):
        if tag == 'span' or tag == 'div' or tag == 'ul' or tag == 'p':
            self.position = ''

if __name__ == "__main__":
    url = 'http://dict.youdao.com/search?q='
    for argv in sys.argv[1:]:
        url += argv + '+'
    webpage = urllib.request.urlopen(url)
    data = str(webpage.read(), encoding='utf-8')
    data = data.strip('\'b')
    f = YoudaoParser()
    f.feed(data)
    content = f.content
    if content.get('title'):
        print(content['title'], end='')
    else:
        print(content['keywords'], end='')
    if content.get('phonetic'):
        print("\t", content['phonetic'])
    else:
        print()
    if not content.get('definition_zh') and\
            not content.get('definition_en') and\
            not content.get('definition_web'):
        print("Not found.")
        sys.exit()
    if content.get('definition_zh'):
        print()
        print("中文翻译：")
        for definition in content['definition_zh'][0:5]:
            print(' '*4, definition)
    elif content.get('definition_web'):
        print()
        print("中文翻译：")
        for definition in content['definition_web'][0:5]:
            print(' '*4, definition)
    if content.get('definition_en'):
        print()
        print("English translation:")
        for definition in content['definition_en'][0:5]:
            print(' '*4, definition)

