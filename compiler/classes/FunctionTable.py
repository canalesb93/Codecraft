class FunctionTable:
    '''
    Class that manages a symbol table for scopes (global, local)
    '''

    def __init__(self):
        self.functions = {}

    def insert(self, function):
        if self.lookup(function.name) is not None:
            print "Function error : ", function.name, "is already declared"
        else:
            # print(function)
            self.functions[function.name] = function
            return self.functions[function.name]
        return 0

    def lookup(self, name):
        if name in self.functions:
            return self.functions[name]
        else:
            # Symbol does not exist
            return None

    def clear(self):
        self.functions.clear()

    def __str__(self):
        description = ''
        for name, function in self.functions.iteritems():
            description = description + '\n%s: ()' % (function.name)
        return description