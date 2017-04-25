from enumerators import *

# Memory System
class MemorySystem:

  def __init__(self):
    self.tempPointer = {}
    self.localPointer = {}
    self.globalPointer = {}
    self.constantPointer = {}

    # Generate Memory Maps
    self.space = 1000 # memory space per type
    for t in Type:
      if t is Type.VOID:
        continue
      self.tempPointer[t] = t.value * self.space
      self.localPointer[t] = (t.value + 5) * self.space
      self.globalPointer[t] = (t.value + 10) * self.space
      self.constantPointer[t] = (t.value + 15) * self.space

    self.memory = [None]*self.space*20

  def generateTemporary(self, variableType, size=1):
    if variableType is not None:
      return self.__generateAddress(self.tempPointer, variableType, size)
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

  def __validateAddress(self, address):
    if not isinstance(address, int):
      address = int(address)
    if address >= 0 and address < len(self.memory):
      return address
    else:
      print "Memory error: address out of bounds"

  def getAddressType(self, address):
    address = self.__validateAddress(address)
    address = address % (self.space * 5)
    for t in Type:
      if t is Type.VOID:
        continue
      if address >= t.value * self.space and address < t.value * self.space + self.space:
        return t
    print "Memory error: address not in type bounds"
    return None

  def setValue(self, address, value):
    address = self.__validateAddress(address)
    if (address >= 0 and address < len(self.memory)):
      if self.memory[address] is None:
        self.memory[address] = value
      else:
        print "Memory error: address is already used"
    else:
      print "Memory error: address out of bounds"

  def getValue(self, address):
    address = self.__validateAddress(address)
    if self.memory[address] is not None:
      t = self.getAddressType(address)
      v = self.memory[address]
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
    else:
      print "Memory error: address is empty"

  def getAddressScope(self, address):
    address = self.__validateAddress(address)
    if address >= self.space * 5 and address < self.space * 10:
      return Scope.LOCAL
    elif address >= self.space * 10 and address < self.space * 15:
      return Scope.GLOBAL
    else:
      print "Memory error: address out of scope"
      return None