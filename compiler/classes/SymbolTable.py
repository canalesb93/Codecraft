from enumerators import Type

class SymbolTable:
    '''
    Class that manages a symbol table for scopes (global, local)
    '''

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