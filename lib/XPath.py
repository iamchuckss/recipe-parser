import requests
from lxml import html
from TextUtils import TextUtils

class XPath:
    def __init__(self, html_content):
        self.tree = html.fromstring(html_content)
    
    def single_node_query(self, query, key):
        nodes = self.tree.xpath(query)

        if len(nodes) > 0:
            value = nodes[0]

            if key == "title":
                return value
            elif key == "description":
                value = TextUtils.format_as_one_line(value)
                return value
            elif key == "yields":
                value = TextUtils.format_yields(value)
                return value
            elif key == "photo_url":
                return value
            else:
                raise BaseException("key not found.")
    
    def ingredients_query(self, query):
        return self.tree.xpath(query)

    def instructions_query(self, query):
        return self.tree.xpath(query)


    
    