from enumerators import Type

class Function:
    '''
    Object containing information about variables
    '''

    def __init__(self, name, functionType, parameters):
        self.id = -1
        self.name = name
        self.functionType = functionType
        self.parameters = parameters

    def __del__(self):
      class_name = self.__class__.__name__
      print class_name, self.name, "destroyed"

    def clear(self):
        self.id = -1
        self.name = ""
        self.functionType = 0
        self.parameters = []

    def __str__(self):
        return 'Function: (%s, %s, %s)' % (self.name, self.functionType, self.parameters)