import sys
import csv

from enumerators import *
from classes import *
from memory import MemorySystem

__quadruples = QuadrupleList()
__constantTable = SymbolTable()
__funcsGlobal = FunctionTable()


__executionStack = Stack()

def import_memory(filename):
  global __memory

  with open(filename, 'rb') as f:
    reader = csv.reader(f)
    stage = 0 # 0 = quadruples, 1 = constants
    while True:
      try: 
        row = reader.next()
        if row[0] == 'END':
          stage += 1
          continue

        if stage == 0:
          # Load Limits and Start Memory
          tgl = rowToLimitDict(row)
          ll = rowToLimitDict(reader.next())
          gl = rowToLimitDict(reader.next())
          cl = rowToLimitDict(reader.next())
          __memory = MemorySystem([tgl, ll, gl, cl])
        elif stage == 1:
          # Load Quadruples
          __quadruples.add(Quadruple(row[0], row[1], row[2], row[3]))
        elif stage == 2:
          # Load Contants to Memory
          __memory.setValue(row[0], row[1])
        elif stage == 3:
          # Load Function Table
          params = []
          f = __funcsGlobal.insert(Function(row[0], Type(int(row[1])), params, int(row[3])))
          tLimit = rowToLimitDict(reader.next())
          lLimit = rowToLimitDict(reader.next())
          f.limits = [tLimit, lLimit]
          paramlen = int(row[2])
          for i in range(0, paramlen):
            row = reader.next()
            v = Var(row[1], Type(int(row[2])))
            v.id = int(row[0])
            v.isArray = row[3] == "True"
            params.append(v)
      except csv.Error:
        print "CSV error: import memory failed"
      except StopIteration:
        break

def execute():
  ip = 0 # Instruction Pointer

  while ip < __quadruples.size():
    q = __quadruples.lookup(ip)
    op = q.operator
    ip += 1

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
      # Handles printing data
      value = __memory.getValue(q.result)
      print value

    elif op == "GOTOF":
      # Handles teleport on false condition
      conditional = __memory.getValue(q.operand1)
      if conditional is False:
        ip = int(q.result)

    elif op == "GOTO":
      # Handles teleport
      ip = int(q.result)

    # elif op == "GOSUB":
    #   # Sends to method
    #   __executionStack.push(ip)
    #   ip = int(q.result)

    # elif op == "ERA":

    
# =============== Helpers ===============

def rowToLimitDict(row):
  limit = {}
  limit[Type.BOOL] = int(row[0])
  limit[Type.INT] = int(row[1])
  limit[Type.FLOAT] = int(row[2])
  limit[Type.CHAR] = int(row[3])
  limit[Type.STRING] = int(row[4])
  return limit

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