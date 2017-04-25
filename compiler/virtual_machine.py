import sys
import csv

from enumerators import *
from classes import *
from memory import MemorySystem

__quadruples = QuadrupleList()
__constantTable = SymbolTable()
__varsGlobal = SymbolTable()
__varsLocal = SymbolTable()
__funcsGlobal = FunctionTable()
__memory = MemorySystem()

def import_memory(filename):
  with open(filename, 'rb') as f:
    reader = csv.reader(f)
    stage = 0 # 0 = quadruples, 1 = constants
    for row in reader:
      if row[0] == 'END':
        stage += 1
        continue
      if stage == 0:
        # Load Quadruples
        __quadruples.add(Quadruple(row[0], row[1], row[2], row[3]))
      elif stage == 1:
        # Load Contants to Memory
        __memory.setValue(int(row[0]), row[1])

def execute():
  # Instruction Pointer
  ip = 0
  while ip < __quadruples.size():
    q = __quadruples.lookup(ip)

    op = q.operator

    if isExpression(op):
      # Arithmetic Operations and Comparisons
      left = __memory.getValue(q.operand1)
      right = __memory.getValue(q.operand2)
      value = performArithmeticExpression(left, op, right)
      # print str(left) + " " + op + " " + str(right) + " = " + str(value)
      __memory.setValue(q.result, value)
    elif op == '=':
      # Assignment of Value
      left = __memory.getValue(q.operand1)
      __memory.setValue(q.result, left)
    elif op == "OUTPUT":
      value = __memory.getValue(q.result)
      print value

    ip += 1

# =============== Helpers ===============

def isExpression(s):
  if s in ['+', '-', '*', '/', '<', '>', '<=', '>=', '==', '!=', 'and', 'or']:
    return True
  else:
    return False

def performArithmeticExpression(left, op, right):
  if op == '+':
    return left + right
  elif op == '-':
    return left - right
  elif op == '*':
    return left * right
  elif op == '/':
    if right != 0:
      return left / right
    else:
      print "Expression error: division by zero"
      exit(1)
  elif op == '<':
    return left < right
  elif op == '>':
    return left > right
  elif op == '<=':
    return left <= right
  elif op == '>=':
    return left >= right
  elif op == '==':
    return left == right
  elif op == '!=':
    return left != right
  elif op == 'and':
    return left and right
  elif op == 'or':
    return left or right
  else:
    print "Operation error: operator not found (!)"
    exit()

# =============== Main ===============

if __name__ == '__main__':
  if (len(sys.argv) > 1):
    file = sys.argv[1]
    import_memory(file)
    execute()
  else:
    print "Execution error: no filename given"