import json

class Recipe:

    def __init__(self):
        self.source = ''
        self.url = ''
        self.title = ''
        self.yields = ''
        self.ingredients = []
        self.instructions = []
        self.time = {}
        self.description = ''
        self.credits = ''
        self.notes = ''
        self.categories = []
        self.photo_url = ''
        self._parser = ''

    def get_array(self):
        array = {
            'title' : self.title,
            'description' : self.description,
            'credits' : self.credits,
            'notes' : self.notes,
            'yields' : self.yields,
            'source' : self.source,
            'url' : self.url,
            'categories' : self.categories,
            'photo_url' : self.photo_url,
            'time' : self.time,
            'ingredients' : self.ingredients,
            'instructions' : self.instructions,
            '_parser' : self._parser,
        }
        return array

    def get_json(self):
        return json.dumps(self.get_array())

    def add_ingredient(self, ingredient):
        if ingredient != None:
            self.ingredients.append(ingredient)

    def add_instruction(self, instruction):
        if instruction != None:
            self.instructions.append(instruction)
            
    def append_category(self, category):
        if category != None:
            self.categories.append(category)

    

