from enumerators import Type

class Var:
    '''
    Object containing information about variables
    '''

    def __init__(self, name, symbolType):
        self.id = -1
        self.name = name
        self.symbolType = symbolType
        self.size = 1

    def setSize(self, size):
        self.size = size


    def address(self):
        return self.id

    def __str__(self):
        return 'Variable: (%d, %s, %s, %r)' % (self.id, self.name, self.symbolType, self.isArray)