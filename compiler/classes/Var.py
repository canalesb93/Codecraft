from enumerators import Type

# ------------------------------------------------------------------
# Variable object
# 
# Holds the variable data: name, type and dimensions if the var
# is an array. Can calculate total size based on dimension.
# ------------------------------------------------------------------
class Var:

    def __init__(self, name, symbolType):
        self.id = -1
        self.name = name
        self.symbolType = symbolType
        self.dimensions = []

    def addDimension(self, size):
        self.dimensions.append(size)

    def dimensionCount(self):
        return len(self.dimensions)

    def totalSpace(self):
        total = 1
        for d in self.dimensions:
            total *= d
        return total

    def address(self):
        return self.id

    def __str__(self):
        return 'Variable: (%r, %s, %s, %r)' % (self.id, self.name, self.symbolType, self.dimensions)