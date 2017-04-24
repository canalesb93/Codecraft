class QuadrupleList:
    '''
    '''

    def __init__(self):
        self.list = []

    def add(self, quadruple):
        print self.size(), ". Quadruple: ", quadruple
        self.list.append(quadruple)

    def clear(self):
        self.list.clear()

    def size(self):
        return len(self.list)

    def __str__(self):
        description = ''
        for i, val in enumerate(self.list):
            number = ("%-2d" % (i))
            description = description + number + ". " + str(val)
            if i != len(self.list) - 1:
                 description = description + '\n'
        return description