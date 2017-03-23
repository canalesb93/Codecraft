# import sys
# import os
# sys.path.append(os.path.abspath('../libraries'))
from libraries.enum import *

class Type(Enum):
  VOID = 0
  INT = 1
  FLOAT = 2
  CHAR = 3
  BOOL = 4
  STRING = 5

class Scope(Enum):
  LOCAL = 0
  GLOBAL = 1