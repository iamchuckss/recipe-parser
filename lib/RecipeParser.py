import requests
from Recipe import Recipe
import RecipeSource
from urllib.parse import urlparse
import requests
import re
import configparser
import importlib


SCHEMA_SPEC                 = "MicrodataSchema";
DATA_VOCABULARY_SPEC        = "MicrodataDataVocabulary";
RDF_DATA_VOCABULARY_SPEC    = "MicrodataRdfDataVocabulary";
MICROFORMAT_SPEC            = "Microformat";
STRUCTURED_DATA_SPEC        = "StructuredData";
GENERAL_PARSER              = "General"

parsers_ini_file_relpath = "parsers/parsers.ini"


def get_matching_parser(url):
    registered_parsers = configparser.ConfigParser()
    registered_parsers.read(parsers_ini_file_relpath)

    # extract hostname from url
    hostname = urlparse(url).netloc
    if re.match("www\.", hostname):
        hostname = hostname[4:]

    # try to match hostname to a registered parser    
    if hostname in registered_parsers:
        return registered_parsers[hostname]["parser"]


def match_markup_format(html):
    if (("application/ld+json" in html) 
        and ("recipeIngredient" in html)
        and ("recipeInstructions" in html)):
        return STRUCTURED_DATA_SPEC
    elif "//schema.org/Recipe" in html:
        return SCHEMA_SPEC
    elif "//data-vocabulary.org/Recipe" in html:
        return DATA_VOCABULARY_SPEC
    elif (("//rdf.data-vocabulary.org/" in html) 
        and ("typeof=\"v:Recipe\"" in html)):
        return RDF_DATA_VOCABULARY_SPEC
    elif (("hrecipe" in html) 
        and ("fn" in html)):
        return MICROFORMAT_SPEC
    else:
        return None
        

def parse(url):
    # retrieve html from url
    pageContent= requests.get(url)
    pageContent.encoding = pageContent.apparent_encoding
    html_content = pageContent.text

    parser_name = None

    # search for a registered parser that matches the URL
    if parser_name == None:
        parser_name = get_matching_parser(url)

    # search for a microdata parser (data-vocabulary.org, schema.org) based
    # upon patterns in the HTML contents
    if parser_name == None:
        parser_name = match_markup_format(html_content)

    # if none of the parsers are matched, fall back to the general parser
    if parser_name == None:
        parser_name = GENERAL_PARSER

    # initialize the right parser and execute parse
    parser =  importlib.import_module('parsers.' + parser_name.strip('"'))
    print("Executing parser {}".format(parser_name))
    recipe = parser.parse(html_content, url)
    if recipe.source == None:
        recipe.source = RecipeSource.get_source_by_url(url)

    return recipe


def main():
    recipe = parse("https://www.bonappetit.com/recipe/healthyish-barbecued-chicken")
    print(recipe.get_array())

if __name__ == '__main__':
    main()