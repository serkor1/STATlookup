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

# Import Custom Classes;
from webcrawler.dstCollector_class import *
from webcrawler.lprCollector_class import *




# Function;
def get_html(url, selector):
    content = BeautifulSoup(
        requests.get(url).content,
        'html.parser'
    ).select(selector)

    return content