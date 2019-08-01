import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from lxml import html
from Recipe import Recipe
import re
import requests

def parse(html_content, url=None):
    recipe = Recipe()
    tree = html.fromstring(html_content)

    nodes = tree.xpath('//*[contains(@type, "//schema.org/Recipe") or contains(@type, "//schema.org/recipe")]')
    microdata = None
    if len(nodes) > 0:
        microdata = nodes[0]
    print(nodes)

    # parse elements
    if microdata != None:

        # title
        # Ideally, this should look for other schema.org entities like
        # BreadcrumList and ListItem to make sure that the "name" object isn't 
        # within either of these.
        nodes = microdata.xpath('.//*[@itemprop="name"]')
        if len(nodes) > 0:
            print(nodes[0])


def main():
    pageContent= requests.get("https://www.foodnetwork.com/recipes/alton-brown/honey-mustard-dressing-recipe-1939031")
    pageContent.encoding = pageContent.apparent_encoding
    html_content = pageContent.text

    recipe = parse(html_content)
    # print(recipe.get_array())

if __name__ == '__main__':
    main()

