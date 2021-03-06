
# ------------------------------------------------------------------
# SymbolTable object
#
# Object holding quadruple data
# ------------------------------------------------------------------
class Quadruple:

    def __init__(self, operator, operand1, operand2, result):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.result = result

    def __str__(self):
        return '[%9s, %9s, %9s, %9s]' % (str(self.operator), str(self.operand1), str(self.operand2), str(self.result))