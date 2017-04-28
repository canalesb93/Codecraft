# -----------------------------------------------------------------------------
# memory.py
#
# Author: Ricardo Canales and Gabriel Berlanga
#
# This module implements the memory management for CodeCraft programming
# language.
# -----------------------------------------------------------------------------

from enumerators import *
from classes import *

# -----------------------------------------------------------------------------
# AddressSystem
#
# This object holds information about memory address pointers
#
# When an address is requested, pointers are increased. This keeps track of 
# the amount of space the program will need to run. Addresses are used in 
# generated quadruples.
# Note: This class is only used in compilation phase
# -----------------------------------------------------------------------------

class AddressSystem:

  def __init__(self):
    self.tempPointer = {}
    self.gtempPointer = {}
    self.localPointer = {}
    self.globalPointer = {}
    self.constantPointer = {}

    # Generate Memory Maps
    self.space = 1000 # memory space per type
    for t in Type:
      if t is Type.VOID:
        continue
      self.tempPointer[t] = t.value * self.space
      self.gtempPointer[t] = t.value * self.space
      self.localPointer[t] = (t.value + 5) * self.space
      self.globalPointer[t] = (t.value + 10) * self.space
      self.constantPointer[t] = (t.value + 15) * self.space

    self.memory = [None]*self.space*20

  def retrieveLocalLimits(self):
    t = dict(self.tempPointer)
    l = dict(self.localPointer)
    self.__resetLocalPointers()
    return [t, l]

  def __resetLocalPointers(self):
    for t in Type:
      if t is Type.VOID:
        continue
      self.tempPointer[t] = t.value * self.space
      self.localPointer[t] = (t.value + 5) * self.space

  def generateTemporary(self, variableType, size=1):
    if variableType is not None:
      return self.__generateAddress(self.tempPointer, variableType, size)
    else:
      print("Memory error: variable type not found")
      return None

  def generateGlobalTemporary(self, variableType, size=1):
    if variableType is not None:
      return self.__generateAddress(self.gtempPointer, variableType, size)
    else:
      print("Memory error: variable type not found")
      return None

  def generateLocal(self, variableType, size=1):
    if variableType is not None:
      return self.__generateAddress(self.localPointer, variableType, size)
    else:
      print("Memory error: variable type not found")
      return None

  def generateGlobal(self, variableType, size=1):
    if variableType is not None:
      return self.__generateAddress(self.globalPointer, variableType, size)
    else:
      print("Memory error: variable type not found")
      return None

  def generateConstant(self, variableType, size=1):
    if variableType is not None:
      return self.__generateAddress(self.constantPointer, variableType, size)
    else:
      print("Memory error: variable type not found")
      return None

  def __generateAddress(self, memoryMap, variableType, size):
    address = memoryMap[variableType]
    memoryMap[variableType] += size
    return address

# -----------------------------------------------------------------------------
# MemorySystem
#
# This object holds the values used during a program's run-time.
#
# Functioning as the main gateway to all values, global and constant 
# values are held directly here. When a value is requested or modified 
# it's type and scope are parsed from the address (based on ranges).
# The MemorySystem also manages the control-stack, sending and requesting
# local and temporary values through it.
# Note: This class is only used in Execution phase
# -----------------------------------------------------------------------------

class MemorySystem():

  def __init__(self, limits):
    self.gtempLimit = limits[0]
    self.localLimit = limits[1]
    self.globalLimit = limits[2]
    self.constantLimit = limits[3]

    self.space = 1000 # memory space per type
    
    # Global Memory
    self.globalMemory = range(5)
    for t in Type:
      if t is Type.VOID:
        continue
      self.globalMemory[t.value] = [None]* (self.globalLimit[t] % self.space) 

    # Constant Memory
    self.constantMemory = range(5)
    for t in Type:
      if t is Type.VOID:
        continue
      self.constantMemory[t.value] = [None]* (self.constantLimit[t] % self.space) 

    # Holds ActivationRecord
    self.controlStack = Stack()
    self.callStack = Stack()
    self.controlStack.push(ActivationRecord([self.gtempLimit, self.localLimit]))


  def __validateAddress(self, address):
    if not isinstance(address, int):
      address = int(address)
    return address

  def __getAddressType(self, address):
    address = address % (self.space * 5)
    for t in Type:
      if t is Type.VOID:
        continue
      if address >= t.value * self.space and address < t.value * self.space + self.space:
        return t
    print "Memory error: address not in type bounds"
    return None

  def __getAddressScope(self, address):
    if address < self.space * 5:
      return Scope.TEMPORARY
    elif address >= self.space * 5 and address < self.space * 10:
      return Scope.LOCAL
    elif address >= self.space * 10 and address < self.space * 15:
      return Scope.GLOBAL
    elif address >= self.space * 15 and address < self.space * 20:
      return Scope.CONSTANT
    else:
      print "Memory error: address out of scope"
      return None

  def setValue(self, address, value):
    address = self.__validateAddress(address)
    scope = self.__getAddressScope(address)
    aType = self.__getAddressType(address)
    address = address % self.space

    if scope is Scope.GLOBAL:
      for t in Type:
        if aType is t:
          self.globalMemory[t.value][address] = value

    elif scope is Scope.CONSTANT:
      for t in Type:
        if aType is t:
          self.constantMemory[t.value][address] = value

    elif scope is Scope.TEMPORARY or scope is Scope.LOCAL:
      self.controlStack.top().setValue(address, value, aType, scope)

  def getValue(self, address):
    address = self.__validateAddress(address)
    scope = self.__getAddressScope(address)
    aType = self.__getAddressType(address)
    address = address % self.space

    if scope is Scope.GLOBAL:
      for t in Type:
        if aType is t:
          return self.__safeValue(self.globalMemory[t.value][address], t)

    elif scope is Scope.CONSTANT:
      for t in Type:
        if aType is t:
          return self.__safeValue(self.constantMemory[t.value][address], t)

    elif scope is Scope.TEMPORARY or scope is Scope.LOCAL:
      return self.__safeValue(self.controlStack.top().getValue(address, aType, scope), aType)

  def __safeValue(self, v, t):
    if t is Type.BOOL:
      # If value is set as string compare
      # Else return as is
      if isinstance(v, str):
        return v == "True"
      else:
        return v
    elif t is Type.INT:
      return int(v)
    elif t is Type.FLOAT:
      return float(v)
    elif t is Type.CHAR:
      return str(v)
    elif t is Type.STRING:
      return str(v)

# -----------------------------------------------------------------------------
# ActivationRecord
#
# This object holds the local and temporary values used during a FUNCTION in 
# the program's run-time.
#
# Created during run-time, ActivationRecords are added and removed from the 
# control-stack in the MemorySystem. An activation record will contain 
# values from an instance(important!) of a function. When that function 
# has concluded the activation record is removed from the control-stack. 
# This allows recursive calls and more.
# Note: This class is only used in Execution phase
# -----------------------------------------------------------------------------      

class ActivationRecord():
  
  def __init__(self, limits):
    self.tempLimit = limits[0]
    self.localLimit = limits[1]

    self.parameters = []
    self.callPosition = 0
    self.returnAddress = None

    self.space = 1000

    # Temporary Memory
    self.tempMemory = range(5)
    for t in Type:
      if t is Type.VOID:
        continue
      self.tempMemory[t.value] = [None]* (self.tempLimit[t] % self.space)

    # Local Memory
    self.localMemory = range(5)
    for t in Type:
      if t is Type.VOID:
        continue
      self.localMemory[t.value] = [None]* (self.localLimit[t] % self.space)

  def setValue(self, address, value, aType, scope):
    if scope is Scope.TEMPORARY:
      for t in Type:
        if aType is t:
          self.tempMemory[t.value][address] = value

    elif scope is Scope.LOCAL:
      for t in Type:
        if aType is t:
          self.localMemory[t.value][address] = value

  def getValue(self, address, aType, scope):
    if scope is Scope.TEMPORARY:
      for t in Type:
        if aType is t:
          return self.tempMemory[t.value][address]

    elif scope is Scope.LOCAL:
      for t in Type:
        if aType is t:
          return self.localMemory[t.value][address]
