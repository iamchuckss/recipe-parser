import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from lxml import html
from TextUtils import TextUtils
from Recipe import Recipe
import re
import requests

def parse(html_content, url=None):
    recipe = Recipe()
    tree = html.fromstring(html_content)

    nodes = tree.xpath('//*[contains(@itemtype, "//schema.org/Recipe") or contains(@type, "//schema.org/recipe")]')
    microdata = None
    if len(nodes) > 0:
        microdata = nodes[0]

    # parse elements
    if microdata != None:

        # title
        # Ideally, this should look for other schema.org entities like
        # BreadcrumList and ListItem to make sure that the "name" object isn't 
        # within either of these.
        nodes = microdata.xpath('.//*[@itemprop="name"]/text()')
        if len(nodes) > 0:
            recipe.title = TextUtils.format_title(nodes[0])

        # summary
        nodes = microdata.xpath('.//*[@itemprop="description"]/text()')
        if len(nodes) > 0:
            recipe.description = nodes[0]

        # cooking times
        searches = {'prepTime' : 'prep',
                    'cookTime' : 'cook',
                    'totalTime' : 'total'}
        for itemprop in searches:
            nodes = microdata.xpath('.//*[@itemprop="' + itemprop + '"]/@content')
            if not nodes:
                nodes = microdata.xpath('.//*[@itemprop="' + itemprop + '"]/@datetime')
            if not nodes:
                nodes = microdata.xpath('.//*[@itemprop="' + itemprop + '"]/text()') 

            recipe.time = TextUtils.format_time_iso8601_to_minutes(nodes[0])

        # yield
        nodes = microdata.xpath('.//*[@itemprop="recipeYield"]/@content')
        if not nodes:
            nodes = microdata.xpath('.//*[@itemprop="recipeyield"]/@content')
        if not nodes:
            nodes = microdata.xpath('.//*[@itemprop="recipeyield"]/@text')
        recipe.yields = TextUtils.format_yields(nodes[0])

        # ingredients
        nodes = microdata.xpath('//*[@itemprop="recipeIngredient"]/text()')
        if not nodes:
            nodes = microdata.xpath('//*[@itemprop="ingredients"]/text()')
        if len(nodes):
            for ingredient in nodes:
                recipe.add_ingredient(TextUtils.format_as_one_line(ingredient))

        # instructions
        found = False

        # look for marup that uses <li> tags for each instruction
        if not found:
            nodes = microdata.xpath('//*[@itemprop="recipeInstructions"]//li/*/text()')
            if nodes:
                nodes = TextUtils.parse_instructions_from_nodes(nodes)
                found = True
        # look for instructions as direct descendents of "recipeInstructions"
        if not found:
            nodes = microdata.xpath('//*[@itemprop="recipeInstructions"]/*/text()')
            if nodes:
                nodes = TextUtils.parse_instructions_from_nodes(nodes)
                found = True
        # some sites will use an "instruction" class for each line
        if not found:
            nodes = microdata.xpath('.//*[@itemprop="recipeInstructions"]//*[contains(concat(" ", normalize-space(@class), " "), " instruction ")]/text()')
            if nodes:
                nodes = TextUtils.parse_instructions_from_nodes(nodes)
                found = True
        # either multiple recipeInstructions nodes, or one node with a blob of text
        if not found:
            nodes = microdata.xpath('.//*[@itemprop="recipeInstructions"]/text()')
            if nodes:
                nodes = TextUtils.parse_instructions_from_nodes(nodes)
                found = True

        recipe.instructions = nodes
        
        # photo_url
        photo_url = ""
        if not photo_url:
            nodes = tree.xpath('//meta[@property="og:image"]/@content')
            if nodes:
                photo_url = nodes[0]
        if not photo_url:
            nodes = microdata.xpath('.//*[@itemprop="image"]/@src')
            if nodes:
                photo_url = nodes[0]
        if not photo_url:
            nodes = microdata.xpath('.//*[@itemprop="image"]//img/@src')
            if nodes:
                photo_url = nodes[0]
        
        if photo_url:
            recipe.photo_url = TextUtils.url_relative_to_absolute(url, photo_url)

        return recipe

def main():
    pageContent= requests.get("https://www.allrecipes.com/recipe/126398/crock-pot-cheesy-mushroom-chicken/?internalSource=recipe%20hub&referringId=1203&referringContentType=Recipe%20Hub&clickId=cardslot%2095")
    pageContent.encoding = pageContent.apparent_encoding
    html_content = pageContent.text
    recipe = parse(html_content)
    print(recipe.get_array())

if __name__ == '__main__':
    main()

