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

    def __del__(self):
      class_name = self.__class__.__name__
      print class_name, self.name, "destroyed"

    def clear(self):
        self.id = -1
        self.name = ""
        self.variableType = 0
        self.value = None

    def __str__(self):
        return 'Variable: (%s, %s)' % (self.name, self.variableType)