import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from parsers.General import General
from TextUtils import TextUtils
from XPath import XPath
from Recipe import Recipe
import re

class Bonappetitcom:
    @staticmethod
    def parse(url):
        xpath = XPath(url)

        # use general parser to parse basic fields
        recipe = General.parse(url)

        # Yield
        yields = xpath.single_node_query('//*[@id="react-app"]/div/div[2]/div[1]/div/div[1]/span[1]/span/text()[last()]', 'yields')
        if len(yields):
            recipe.yields = yields
        
        # Ingredients
        ingredients = xpath.ingredients_query('//*[@id="react-app"]/div/div[2]/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/ul/li/div/text()') 
        if len(ingredients):
            for ingredient in ingredients:
                recipe.add_ingredient(TextUtils.format_as_one_line(ingredient))
            
        # Instructions
        instructions = xpath.instructions_query('//*[@id="react-app"]/div/div[2]/div[2]/div/div/div[1]/div[1]/div[3]/div/ul/li/div/p/text()');
        if len(instructions):
            for instruction in instructions:
                recipe.add_instruction(TextUtils.format_as_one_line(instruction))

        return recipe
