from enumerators import Type

class Var:
    '''
    Object containing information about variables
    '''

    def __init__(self, name, symbolType):
        self.id = -1
        self.name = name
        self.symbolType = symbolType
        self.value = None
        self.isArray = False

    def setIsArray(self, isArray):
        self.isArray = isArray

    def address(self):
        return self.id

    def __str__(self):
        return 'Variable: (%s, %s, %r)' % (self.name, self.symbolType, self.isArray)