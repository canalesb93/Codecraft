class SymbolTable:
    '''
    Class that manages a symbol table for scopes (global, local)
    '''

    def __init__(self):
        self.vars = {}

    def insert(self, variable):
        if self.lookup(variable.name) != 0:
            print "Variable error : ", variable.name, "is already declared"
        else:
            print(variable)
            self.vars[variable.name] = variable
            return self.vars[variable.name]
        return 0

    def lookup(self, name):
        if name in self.vars:
            return self.vars[name]
        else:
            # Symbol does not exist
            return 0

    def clear(self):
        self.vars.clear()