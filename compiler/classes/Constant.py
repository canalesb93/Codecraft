from enumerators import Type

class Constant:
    '''
    Object containing information about a constant
    '''

    def __init__(self, id, name, symbolType, value):
        self.id = id
        self.name = name
        self.symbolType = symbolType
        self.value = value

    def address(self):
        return self.id

    def __str__(self):
        return 'Constant: (%s, %s, %s)' % (self.name, self.symbolType.name, self.address())