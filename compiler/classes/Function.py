from enumerators import Type

# ------------------------------------------------------------------
# Function object
#
# Object that represents a function, holds its data. Limits of a 
# functions addresses are held here. They are used when initializing
# memory for any instance of the function.
# ------------------------------------------------------------------
class Function:

    def __init__(self, name, functionType, parameters, position):
        self.name = name
        self.functionType = functionType
        self.parameters = parameters
        self.quadruplePosition = position
        self.limits = []

    def parametersSize(self):
        return len(self.parameters)

    def __str__(self):
        return 'Function: (%s, %s, %s, %d)' % (self.name, self.functionType, self.parameters, self.quadruplePosition)