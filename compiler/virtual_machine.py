#!python2 
# -----------------------------------------------------------------------------
# virtual_machine.py
#
# Author: Ricardo Canales and Gabriel Berlanga
#
# This module simulates memory and executes the compiled program.
# -----------------------------------------------------------------------------

from __future__ import division
import sys
import csv
import time

from enumerators import *
from classes import *
from memory import MemorySystem
from memory import ActivationRecord

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# =============================================================================
# Setup and Import
#
# Prepend "__" to all global variables for easy undestanding. Remember to use 
# "global" when modifying these variables in a different scope.
# 
# Handles importing memory from compiled program file.
# =============================================================================
# /////////////////////////////////////////////////////////////////////////////

__quadruples = QuadrupleList()
__funcsGlobal = FunctionTable()

# -----------------------------------------------------------------------------
# import_memory()
#
# Opens the compiled program and parsers its data into memory. The process
# is divided in 4 stages:
# 
#     1. Load Limits
#     2. Load Quadruples
#     3. Load Constants
#     4. Load Function Table
# 
# Once done the program will begin execution.
# -----------------------------------------------------------------------------

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
            params.append(v)
      except csv.Error:
        print "CSV error: import memory failed"
      except StopIteration:
        break

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# =============================================================================
# Execution
# 
# General execution of program file instructions
# =============================================================================
# /////////////////////////////////////////////////////////////////////////////

# -----------------------------------------------------------------------------
# execute()
#
# Iterates through the list of quadruples with "ip"(instruction pointer). 
# Each processed quadruple will contain a expression of ID of an action which 
# will be realized. Memory manipulation happens here.
# -----------------------------------------------------------------------------

def execute():
  ip = 0 # Instruction Pointer

  while ip < __quadruples.size():
    q = __quadruples.lookup(ip)
    op = q.operator
    ip += 1
    # pause()

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

    elif op == "INPUT":
      value = input()
      address = q.result
      __memory.setValue(address, value)

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
      __memory.setValue(str(ar.parameters[position].address()), value)
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

    elif op == "VER":
      index = __memory.getValue(q.operand1)
      low = int(q.operand2)
      high = int(q.result)
      if not (index >= low and index < high):
        print "Array error: index out of bounds"
        exit(1)

    elif op == "ACUM":
      left = __memory.getValue(q.operand1)
      arrAddress = left + int(q.operand2)
      __memory.setValue(q.result[1:-1], arrAddress)

# =============================================================================
# Helpers
# =============================================================================

# -----------------------------------------------------------------------------
# rowToLimitDict()
#
# Converts a OBJ file row to a dictionary with types limit. Used by the
# importer.
# -----------------------------------------------------------------------------

def rowToLimitDict(row):
  limit = {}
  limit[Type.BOOL] = int(row[0])
  limit[Type.INT] = int(row[1])
  limit[Type.FLOAT] = int(row[2])
  limit[Type.CHAR] = int(row[3])
  limit[Type.STRING] = int(row[4])
  return limit

# -----------------------------------------------------------------------------
# isExpression()
#
# Confirms wether the string is an operation.
# -----------------------------------------------------------------------------

def isExpression(s):
  return s in ['+', '-', '*', '/', '<', '>', '<=', '>=', '==', '!=', 'and', 'or']

# -----------------------------------------------------------------------------
# performArithmeticExpression()
#
# Given a left value, str(operator) and right value. Performs the expression. 
# Returns the performed expression value.
# -----------------------------------------------------------------------------

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
    exit(1)

def pause():
  programPause = raw_input("Press the <ENTER> key to continue...")

# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
  if (len(sys.argv) > 1):
    file = sys.argv[1]
    import_memory(file)
    executionTime = time.time()
    execute()
    print "\n%% Execution ended, total time: %fs" % (time.time() - executionTime)
  else:
    print "Execution error: no filename given"