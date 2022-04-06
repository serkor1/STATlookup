# Importing All needed
# modules for the programs to work
from matplotlib.cbook import flatten
from bs4 import BeautifulSoup
import requests
import sqlite3
from bs4 import BeautifulSoup
import re
import time
from alive_progress import alive_bar
from googletrans import Translator
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

# Import Custom Classes;
from webcrawler.lprCollector_class import *
from webcrawler.hqCollector_class import *
from webcrawler.timesCollector_class import *
from webcrawler.descCollector_class import *
from webcrawler.dbCreate_class import *



# Custom Functions; ####
def get_html(url, selector):
    content = BeautifulSoup(
        requests.get(url).content,
        'html.parser'
    ).select(selector)

    return content