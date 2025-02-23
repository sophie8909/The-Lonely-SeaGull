
# ===============================================
# String and constant dictionaries
# ===============================================
#
class Dict:

    # Set the default language
    #
    language = "en"

    # The same dictionary structure contains both languages.
    # .
    #
    dictionary = {
        "en": {
            'reset': "Reset entry",
            'quit': "Leave application",
            'update': "Update Data",
            'content': "Data Base Content",
            '<--': "Undo",
            '-->': "Redo",
            'contentDisp': "",
            'empty': ""
        },
        "se": {
            'reset': "Återställ text",
            'quit': "Avsluta",
            'update': "Uppdatera Data",
            'content': "Innehåll i databasen",
            '<--': "Ångra",
            '-->': "Gör igen",
            'contentDisp': "",
            'empty': ""
        }
    }

    # A variable used to keep track of the strings in the system, so that we can change them
    # when we change language dynamically.
    #
    string_containers = []

    # Every time we add create a StringVar or an IntVar it has to be "registered" so that we can change
    # it easily. Since these variables are directly connected to the String in the interface, it is only
    # necessary to change the content of that specific variable.
    #
    # The combo of a key and a value is called a container her.
    #
    def add_container(self, cont):
        self.string_containers.append(cont)

    # We get the value for the key in the container.
    #
    def get_container(self, key):
        for p in self.string_containers:
            if p[0] == key:
                return p[1]
        return ''

    # When we want to update the strings in the interface, we have them all here.
    #
    def update_strings(self):
        for c in self.string_containers:
            c.text = self.get_string(c)

    # This function should be used to change the language of the application..
    #
    def set_language(self, lang):
        self.language = lang
        self.update_strings()

    # Get the string for the key given as argument. The current language is taken from the
    # variable defined in the class.
    #
    def get_string(self, key):
        d = self.dictionary[self.language]
        return d[key]

# An unused class for storing other things than strings, such as image references, etc.
class Common:

    # Again we use a python dictionary.
    #
    storage = { }

    def add_common(self, key, value):
        self.storage[key] = value

    def get_common(self, key):
        return self.storage[key]
