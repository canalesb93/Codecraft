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

  def generateTemporary(self, variableType, size=1):
    if variableType is not None:
      return "t-" + self.__generateAddress(self.tempPointer, variableType, size)
    else:
      print("Memory error: variable type not found")
      return None

  def generateLocal(self, variableType, size=1):
    if variableType is not None:
      return "l-" + self.__generateAddress(self.localPointer, variableType, size)
    else:
      print("Memory error: variable type not found")
      return None

  def generateGlobal(self, variableType, size=1):
    if variableType is not None:
      return "g-" + self.__generateAddress(self.globalPointer, variableType, size)
    else:
      print("Memory error: variable type not found")
      return None

  def generateConstant(self, variableType, size=1):
    if variableType is not None:
      return "c-" + self.__generateAddress(self.constantPointer, variableType, size)
    else:
      print("Memory error: variable type not found")
      return None

  def __generateAddress(self, memoryMap, variableType, size):
      address = memoryMap[variableType]
      memoryMap[variableType] += size
      return variableType.name[0].lower() + str(address)
