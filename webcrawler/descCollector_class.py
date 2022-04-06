from matplotlib.cbook import flatten
from bs4 import BeautifulSoup
import requests
import sqlite3
from bs4 import BeautifulSoup
from bs4.element import Tag
import re
import time
from alive_progress import alive_bar
from googletrans import Translator

class desc_collect:

    def __init__(self, html, container):
        self.html = html
        self.container = container

        soup = BeautifulSoup(
            self.html,
            'html.parser'
        ).find(container).decode_contents()

        self.soup = BeautifulSoup(str(soup), 'html.parser')

    def get_base(self):
        return self.soup


    def get_description(self, tag):
        desc_title = []
        desc_content = []
        block = []
        h3 = False
        for el in self.soup.contents:
            if type(el) == Tag and el.name == tag:
                if h3:
                    desc_title.append(el)
                    desc_content.append(block)
                    block = []
                h3 = True
            elif h3 and type(el) != Tag:
                block.append(el)

        if block:
            desc_content.append(block)

        desc_temp = desc_content
        desc_content = []
        for block in desc_temp:
            # Concatenate String
            get_text = ''.join(block)

            check_name = bool(
                re.match(
                    string=get_text.lower().strip(),
                    pattern="\s+"
                )
            )

            if check_name:
                continue

            desc_content.append(get_text)
        # Index 0: Title; Index 1: Content
        self.container = [desc_title, desc_content]

        return self.container


    def translate(self):
        translator = Translator()
        description = []
        for index in self.container[1]:
            description_en = translator.translate(index, dest='en')
            description.append(description_en.text)

        return description





# Test Function
# Create Connection
# to sql
# connection = sqlite3.connect(
#     'hq/dstHQraw.sqlite'
# )
#
# cursor = connection.cursor()
#
#
#
# sample = cursor.execute(
#     '''
#     SELECT * FROM variable WHERE id = 1
#     '''
# ).fetchall()
#
#
#
# extract_html = sample[0][6]
#
# base = desc_collect(extract_html, 'div')
#
#
# desc = base.get_description()
#
# translator = Translator()
# description = []
#
#
# for index in desc[1]:
#     print(index)
#     print("---")
#     description_en = translator.translate(text="fisk", dest='en')
#     description.append(description_en.text)
#
#
#
# print(description)

