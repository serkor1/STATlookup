
from matplotlib.cbook import flatten
from bs4 import BeautifulSoup
import requests
import sqlite3
from bs4 import BeautifulSoup
import re


class dstCollector:

    # This is the main container for
    # all values
    container = []

    # Initialize the class
    # and pass the url you need to extract
    def __init__(self, url, selector, do_ul = True, is_variable = False):
        self.url = url
        self.selector = selector
        self.is_variable = is_variable

        self.content = BeautifulSoup(
            requests.get(self.url).content,
            'html.parser'
        ).select(selector=self.selector)


        if do_ul:
            if is_variable:
                delopgaver = re.findall(
                    string=str(self.content),
                    pattern="<h3>Delopgaver</h3>"
                )

                variable = re.findall(
                    string=str(self.content),
                    pattern="(<h3>Variable)</h3>"
                )

                if len(delopgaver) == 1 and len(variable) == 0:
                    # This returns a list of length
                    # minimum 1. 2 if there is additional stuff
                    self.content = [BeautifulSoup(
                        str(self.content),
                        "html.parser"
                    ).select('ul'),[]]

                if len(delopgaver) == 0 and len(variable) == 1:
                    self.content = [[],BeautifulSoup(
                        str(self.content),
                        "html.parser"
                    ).select('ul')]

                else:
                    self.content = BeautifulSoup(
                        str(self.content),
                        "html.parser"
                    ).select('ul')

            else:
                # This returns a list of length
                # minimum 1. 2 if there is additional stuff
                self.content = BeautifulSoup(
                    str(self.content),
                    "html.parser"
                ).select('ul')



    def get_url(self):

        # Get URLS
        if self.is_variable:
            try:
                list_url = re.findall(
                    string  = str(self.content[1]),
                    pattern = "<a href=[\"\'](.*?)[\"\']" # HAD LI
                )
            except:
                list_url = []
        else:
            list_url = re.findall(
                string=str(self.content[0]),
                pattern="<a href=[\"\'](.*?)[\"\']"
            )

        # Modify each URL to contain
        # the base URL
        list_url =  [f'https://www.dst.dk{index}' for index in list_url]

        return list_url

    def get_name(self):

        if self.is_variable:
            try:
                list_names = re.findall(
                    string = str(self.content[1]),
                    pattern=".+>(.+)</a>.+"
                )
            except:
                list_names = []
        else:
            list_names = re.findall(
                string=str(self.content[0]),
                pattern=".+>(.+)</a>.+"
            )


        return list_names

    def get_additional(self):
        # NOTE: If the length is above 1
        # it imples that there is additional variables
        try:
            self.additional_url = re.findall(
                string=str(self.content[0]),
                pattern="<li><a href=[\"\'](.*?)[\"\']"
            )

            self.additional_url = [f'https://www.dst.dk{index}' for index in self.additional_url]
        except:
            self.additional_url = []

        return self.additional_url

    def get_content(self, selector, url_list):
        container = []
        iteration = 0
        for url in url_list:

            html_content = BeautifulSoup(
                requests.get(url).content,
                'html.parser'
            ).select(selector=selector)

            container.append(html_content[0])

        return container

