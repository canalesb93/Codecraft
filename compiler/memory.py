from enumerators import Type

# Memory System
class MemorySystem:

  def __init__(self):
    self.tempPointer = {}
    self.localPointer = {}
    self.globalPointer = {}
    self.constantPointer = {}

    # Generate Memory Maps
    space = 1000 # memory space per type
    types = [Type.BOOL, Type.INT, Type.FLOAT, Type.CHAR, Type.STRING]
    for index, t in enumerate(types):
      self.tempPointer[t] = index * space
      self.localPointer[t] = (index + 5) * space
      self.globalPointer[t] = (index + 10) * space
      self.constantPointer[t] = (index + 15) * space

    self.memory = [None]*space*20

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

    # Fill Array with defaults
    # if size > 1:
    #   for a in range(address, memoryMap[variableType]):
    #     if variableType is Type.BOOL:
    #       self.memory[a] = False
    #     elif variableType is Type.INT:
    #       self.memory[a] = 0
    #     elif variableType is Type.FLOAT:
    #       self.memory[a] = 0.0
    #     elif variableType is Type.CHAR:
    #       self.memory[a] = 0
    #     elif variableType is Type.STRING:
    #       self.memory[a] = ""

    return address

  def setValue(self, address, value):
    if (address >= 0 and address < len(self.memory)):
      if self.memory[address] is None:
        self.memory[address] = value
      else:
        print("Memory error: address is already used")
    else:
      print("Memory error: address out of bounds")

  def getValue(self, address):
    if (address >= 0 and address < len(self.memory)):
      if self.memory[address] is not None:
        return self.memory[address]
      else:
        print("Memory error: address is empty")
    else:
      print("Memory error: address out of bounds")