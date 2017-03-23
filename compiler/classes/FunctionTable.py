class FunctionTable:
    '''
    Class that manages a symbol table for scopes (global, local)
    '''

    def __init__(self):
        self.functions = {}

    def insert(self, function):
        if self.lookup(function.name) != 0:
            print "function error : ", name, "is already declared"
        else:
            print(function)
            self.functions[function.name] = function
            return self.functions[function.name]
        return 0

    def lookup(self, name):
        if name in self.functions:
            return self.functions[name]
        else:
            # Symbol does not exist
            return 0

    def clear(self):
        self.functions.clear()