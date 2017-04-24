class Quadruple:
    '''
    '''

    def __init__(self, operator, operand1, operand2, result):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.result = result

    def __str__(self):
        return '[%7s, %7s, %7s, %7s]' % (str(self.operator), str(self.operand1), str(self.operand2), str(self.result))