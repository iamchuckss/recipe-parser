import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from parsers import MicrodataSchema
from XPath import XPath
from Recipe import Recipe
import requests

def parse(html_content, url=None):
    xpath = XPath(html_content)

    recipe = MicrodataSchema.parse(html_content)
    recipe.title = xpath.single_node_query('//h1/text()', 'title')
    recipe._parser = "MicrodataSchema"
    
    return recipe
