import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from TextUtils import TextUtils
from XPath import XPath
from Recipe import Recipe
import re

class General:

    @staticmethod
    def parse(url):
        recipe = Recipe()
        xpath = XPath(url)

        # Title
        title = xpath.single_node_query('//meta[@itemprop="og:title/@content"]', 'title')
        if title == None:
           title = xpath.single_node_query('//title/text()', 'title') 
        if title == None:
           title = "Recipe from {}".format(url) 

        recipe.title = title

        # Photo
        photo_url = xpath.single_node_query('//meta[@property="og:image"]/@content', 'photo_url')
        if re.search("\.(jpeg|jpg)", photo_url, re.I):
            photo_url = TextUtils.url_relative_to_absolute(url, photo_url)
            print(photo_url)
            recipe.photo_url = photo_url

        return recipe

