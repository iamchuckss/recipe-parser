import re
from urllib.parse import urljoin
import dateutil.parser as dateutil_parser

class TextUtils:
    @staticmethod
    def format_as_one_line(str):
        str = re.sub('/\s+/', ' ', str)  # squash multi spaces
        str = re.sub('/\s+,/', ',', str) # fix hanging commas
        str = str.strip() # trim trailing white spaces
        return str

    @staticmethod
    def format_title(title):
        title = re.sub("/.+\s+recipes\s+[\:\|\-]\s+/i", "", title);
        title = re.sub("/\s+[\:\|\-]\s+.+$/i", "", title);
        title = re.sub("/\s+recipe\s*$/i", "", title);
        title = re.sub("/^Recipe\s+for\s+/i", "", title);
        return title.strip();

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
        str = re.sub("^serves (\d+ to \d+)(.*)$", "$1 servings$2", str, re.I)
        str = re.sub("^serves ([\d\-]+)(.*)$", "$1 servings$2", str, re.I)
        str = re.sub("^1 servings(.*)$", "1 serving$1", str, re.I)

        # Remove leading "Yield:" or "Servings:"
        str = re.sub("^(yields?|servings|serves|makes about|makes)\:?\s+", "", str, re.I);

        # Condense spaces around hyphens
        str = re.sub("(\d+)\s*-\s*(\d+)", "$1-$2", str);
        return str

    @staticmethod
    def url_relative_to_absolute(base, rel):
        return urljoin(base, rel)

    @staticmethod
    def format_time_iso8601_to_minutes(str):
        # return if str is not in iso8601 format
        if re.search('^[P,Y,D,T,H,M,S,0-9,\.]+$', str) == None:
            return 0
        
        if str.find('P') == 0:
            str = str[1:]
        if str.find('T') == 0:
            str = str[1:]

        minutes = 0
        # time
        if re.search('([\d\,\.]+)([HMS])', str) != None:
            times = re.findall('\d+[HMS]', str)
            for time in times:
                if time[-1] == 'H':
                    minutes = minutes + int(time[:-1]) * 3600
                if time[-1] == 'M':
                    minutes = minutes + int(time[:-1]) * 60
                if time[-1] == 'S':
                    minutes = minutes + int(time[:-1])

        return int(minutes / 60)