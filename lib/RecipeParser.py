import requests
from lxml import html

class RecipeParser:
    @staticmethod
    def parse(url=None):
        url = 'https://www.bonappetit.com/recipe/healthyish-barbecued-chicken'
        pageContent=requests.get(url)
        tree = html.fromstring(pageContent.content)

        # Title
        title = tree.xpath('//*[@id="react-app"]/div/div[2]/header/div/h1/a/text()')
        
        # Yield
        yields = tree.xpath('//*[@id="react-app"]/div/div[2]/div[1]/div/div[1]/span[1]/span/text()[last()]')
        
        # Ingredients
        ingredients = tree.xpath('//*[@id="react-app"]/div/div[2]/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/ul/li/div/text()') 

        # Instructions
        instructions = tree.xpath('//*[@id="react-app"]/div/div[2]/div[2]/div/div/div[1]/div[1]/div[3]/div/ul/li/div/p/text()');
        
        print(title)
        print(yields)
        print(ingredients)
        print(instructions)


def main():
    RecipeParser.parse()

if __name__ == '__main__':
    main();