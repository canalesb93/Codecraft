# import sys
# import os
# sys.path.append(os.path.abspath('../libraries'))
from libraries.enum import *

class Type(Enum):
  __order__ = 'BOOL INT FLOAT CHAR STRING VOID'
  BOOL = 0
  INT = 1
  FLOAT = 2
  CHAR = 3
  STRING = 4
  VOID = 5

class Scope(Enum):
  LOCAL = 0
  GLOBAL = 1
  TEMPORARY = 2
  CONSTANT = 3