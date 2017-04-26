from enumerators import Type

class Function:
    '''
    Object containing information about variables
    '''

    def __init__(self, name, functionType, parameters, position):
        self.name = name
        self.functionType = functionType
        self.parameters = parameters
        self.quadruplePosition = position

    def parametersSize(self):
        return len(self.parameters)

    def __str__(self):
        return 'Function: (%s, %s, %s, %d)' % (self.name, self.functionType, self.parameters, self.quadruplePosition)