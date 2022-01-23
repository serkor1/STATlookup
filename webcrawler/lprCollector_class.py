from matplotlib.cbook import flatten
from bs4 import BeautifulSoup
import requests
import sqlite3
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.parse, urllib.error
import ssl
import http.client
from urllib.error import HTTPError
# ignore SSL erros

class lprCollector:

    base_url = "https://www.esundhed.dk/Dokumentation?"

    def __init__(self, url, selector, ctx):
        self.url = url
        self.selector = selector
        self.ctx = ctx


        # In some cases it throws
        # 500 error
        try:
            handler = urllib.request.urlopen(url, context=ctx, timeout=6000).read()
        except HTTPError as e:
            handler = e.read()
        except http.client.IncompleteRead as e:
            handler = e.partial


        self.base_html = BeautifulSoup(
            #urllib.request.urlopen(url, context=ctx).read(),
            handler.decode('utf-8'),
            'html.parser'
        ).select(selector=selector)

        self.content = BeautifulSoup(
            str(self.base_html),
            'html5lib'
        ).select('a')

    def get_base(self):
        return self.base_html

    def get_name(self):
        list_name = []
        for index in self.content:
            name = re.findall(
                string = str(index),
                pattern=".+>(.+)</a>"
            )

            list_name.append(name[0])

        return list(flatten(list_name))

    def get_url(self):
        temp_list = []
        for index in self.content:
            # Full URL:
            url = re.findall(
                string = str(index),
                pattern= ".+href=[\"\'](.*?)[\"\']"
            )

            url = re.split(
                string = url[0],
                pattern="\?",
                maxsplit=1

            )
            temp_list.append(lprCollector.base_url + url[1])

        return  list(flatten(temp_list))




# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE
#
# # USE list-tab-tables for tables inside registre
# # USE list-tab-registers for Headers
# # USE list-tab-variables for variables
# # USE col-md-4 col-12 result for descriptions
#
# # 1. Find Headers,
# # 2 Post those headers inside the function with tables selector
# # 3 Post Those URLS with list tab-variables
# # From the variables
# # Get the Col + downloads
#
# test = lprCollector(url = "https://www.esundhed.dk/Dokumentation?rid=5&amp;tid=7&amp;vid=66", selector= "div.col-md-4.col-12.result", ctx=ctx)
# print(
#     test.get_base()
# )
