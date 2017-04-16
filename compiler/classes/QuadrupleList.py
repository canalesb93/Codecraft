class QuadrupleList:
    '''
    '''

    def __init__(self):
        self.quadruples = []

    def add(self, quadruple):
        print self.size(), ". New Quadruple: ", quadruple
        self.quadruples.append(quadruple)

    def clear(self):
        self.quadruples.clear()

    def size(self):
        return len(self.quadruples)

    def __str__(self):
        description = ''
        for i, val in enumerate(self.quadruples):
            description = description + str(i) + ". " + str(val)
            if i != len(self.quadruples) - 1:
                 description = description + '\n'
        return description