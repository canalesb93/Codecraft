import sys
import csv

from enumerators import *
from classes import *
from memory import MemorySystem
from memory import ActivationRecord

__quadruples = QuadrupleList()
__constantTable = SymbolTable()
__funcsGlobal = FunctionTable()

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
            v.size = int(row[3])
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
      sys.stdout.write(str(value))
      sys.stdout.flush()

    elif op == "OUTPUTLN":
      sys.stdout.write('\n')
      sys.stdout.flush()

    elif op == "GOTOF":
      # Handles teleport on false condition
      conditional = __memory.getValue(q.operand1)
      if conditional is False:
        ip = int(q.result)

    elif op == "GOTO" or op == "SKIP":
      # Handles teleport
      ip = int(q.result)

    elif op == "ERA":
      # Push ActivationRecord to control stack
      name = q.operand1
      func = __funcsGlobal.lookup(name)
      ar = ActivationRecord(func.limits)
      ar.parameters = func.parameters
      __memory.callStack.push(ar)

    elif op == "PARAM":
      # Setup ActivationRecord local values
      value = __memory.getValue(q.operand1)
      position = int(q.result)
      ar = __memory.callStack.top()
      # HACK: Push and pop ar after setting param value
      __memory.controlStack.push(ar)
      __memory.setValue(ar.parameters[position].address(), value)
      __memory.controlStack.pop()

    elif op == "GOSUB":
      # Setup ActivationRecord callPos and returnAddress
      # Handles teleport
      name = q.operand1
      func = __funcsGlobal.lookup(name)
      ar = __memory.callStack.pop()
      ar.callPosition = ip
      if q.result:
        ar.returnAddress = q.result
      __memory.controlStack.push(ar)
      # Sends to method
      ip = func.quadruplePosition

    elif op == "RETURN":
      # Pop ActivationRecord send return value
      ar = __memory.controlStack.top()
      if q.result:
        value = __memory.getValue(q.result)
        __memory.controlStack.pop()
        __memory.setValue(ar.returnAddress, value)
      else:
        __memory.controlStack.pop()
      # Return to call position
      ip = ar.callPosition

    elif op == "ENDPROC":
      ar = __memory.controlStack.pop()
      ip = ar.callPosition


    
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
    print
  else:
    print "Execution error: no filename given"