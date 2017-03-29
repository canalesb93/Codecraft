from enumerators import Type

class Var:
    '''
    Object containing information about variables
    '''

    def __init__(self, name, variableType):
        self.id = -1
        self.name = name
        self.variableType = variableType
        self.value = None
        self.isArray = False

    def clear(self):
        self.id = -1
        self.name = ""
        self.variableType = 0
        self.value = None

    def setIsArray(self, isArray):
        self.isArray = isArray

    def __str__(self):
        return 'Variable: (%s, %s, %r)' % (self.name, self.variableType, self.isArray)