import re

class TextUtils:
    @staticmethod
    def format_as_one_line(str):
        str = re.sub('/\s+/', ' ', str)  # squash multi spaces
        str = re.sub('/\s+,/', ',', str) # fix hanging commas
        str = str.strip() # trim trailing white spaces
        return str

    @staticmethod
    def convert_words_to_numbers(str):
        numbers = {
            'one' : 1,
            'two' : 2,
            'three' : 3,
            'four' : 4,
            'five' : 5,
            'six' : 6,
            'seven' : 7,
            'eight' : 8,
            'nine' : 9,
            'ten' : 10,
            'eleven' : 11,
            'twelve' : 12,
            'thirteen' : 13,
            'fourteen' : 14,
            'fifteen' : 15,
            'sixteen' : 16,
            'seventeen' : 17,
            'eighteen' : 18,
            'nineteen' : 19,
            'twenty' : 20
        }
        for number in numbers:
            if number in str:
                str.replace(number, numbers[number])
        return str

    @staticmethod
    def format_yields(str):
        str = TextUtils.format_as_one_line(str)
        str = str.lower()
        str = TextUtils.convert_words_to_numbers(str)

        # Convert "serves ## into ## servings"
        str = re.sub("/^serves (\d+ to \d+)(.*)$/i", "$1 servings$2", str)
        str = re.sub("/^serves ([\d\-]+)(.*)$/i", "$1 servings$2", str)
        str = re.sub("/^1 servings(.*)$/", "1 serving$1", str)

        # Remove leading "Yield:" or "Servings:"
        str = re.sub("/^(yields?|servings|serves|makes about|makes)\:?\s+/", "", str);

        # Condense spaces around hyphens
        str = re.sub("/(\d+)\s*-\s*(\d+)/", "$1-$2", str);
        return str

        
    