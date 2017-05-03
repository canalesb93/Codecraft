from enumerators import Type

# ------------------------------------------------------------------
# SymbolTable object
#
# A dictionary with utility methods. Keeps track of symbols in 
# the program. Insert and Lookup methods are used at parser.py
# There are 3 instances of this object.
#   1. Global Variables
#   2. Local Variables
#   3. Constants
# ------------------------------------------------------------------
class SymbolTable:

    def __init__(self):
        self.symbols = {}

    def insert(self, variable):
        if self.lookup(variable.name) is not None:
            print "Symbol error : ", variable.name, "is already declared"
        else:
            self.symbols[variable.name] = variable
            return self.symbols[variable.name]
        return 0

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        else:
            # Symbols does not exist
            return None

    def size(self):
        return len(self.symbols)

    def clear(self):
        self.symbols.clear()

    def __str__(self):
        description = ''
        for name, variable in self.symbols.iteritems():
            description = description + '\n%s: (%s, %s)' % (variable.name, variable.symbolType, variable.address())
        return description