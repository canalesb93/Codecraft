from enumerators import Type

class SymbolTable:
    '''
    Class that manages a symbol table for scopes (global, local)
    '''

    def __init__(self):
        self.symbols = {}
        self.typeCounts = {}
        self.typeCounts[Type.BOOL] = 0
        self.typeCounts[Type.INT] = 0
        self.typeCounts[Type.FLOAT] = 0
        self.typeCounts[Type.CHAR] = 0
        self.typeCounts[Type.STRING] = 0

    def insert(self, variable):
        if self.lookup(variable.name) is not None:
            print "Symbol error : ", variable.name, "is already declared"
        else:
            variable.id = self.typeCounts[variable.symbolType]
            self.symbols[variable.name] = variable
            self.typeCounts[variable.symbolType] += 1
            return self.symbols[variable.name]
        return 0

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        else:
            # Symbols does not exist
            return None

    def delete(self, name):
        v = self.lookup(name)
        self.typeCounts[v.symbolType] -= 1
        del v

    def size(self):
        return self.typeCounts[Type.BOOL] + self.typeCounts[Type.INT] + self.typeCounts[Type.FLOAT] + self.typeCounts[Type.CHAR] + self.typeCounts[Type.STRING]

    def clear(self):
        self.symbols.clear()

    def __str__(self):
        description = ''
        for name, variable in self.symbols.iteritems():
            description = description + '\n%s: (%s)' % (variable.name, variable.symbolType)
        return description