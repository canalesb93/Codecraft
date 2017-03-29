from enumerators import Type

cube = {}

# Assignment
cube['BOOL=BOOL'] = Type.BOOL
cube['INT=INT'] = Type.INT
cube['INT=FLOAT'] = Type.INT
cube['INT=CHAR'] = Type.INT
cube['FLOAT=FLOAT'] = Type.FLOAT
cube['FLOAT=INT'] = Type.FLOAT
cube['CHAR=INT'] = Type.CHAR
cube['CHAR=CHAR'] = Type.CHAR
cube['STRING=STRING'] = Type.STRING

# Sum
cube['INT+INT'] = Type.INT
cube['INT+FLOAT'] = Type.FLOAT
cube['INT+CHAR'] = Type.INT
cube['FLOAT+INT'] = Type.FLOAT
cube['FLOAT+FLOAT'] = Type.FLOAT
cube['CHAR+INT'] = Type.INT
cube['CHAR+CHAR'] = Type.INT
cube['STRING+STRING'] = Type.STRING

# Substraction
cube['INT-INT'] = Type.INT
cube['INT-FLOAT'] = Type.FLOAT
cube['INT-CHAR'] = Type.INT
cube['FLOAT-INT'] = Type.FLOAT
cube['FLOAT-FLOAT'] = Type.FLOAT
cube['CHAR-INT'] = Type.INT
cube['CHAR-CHAR'] = Type.INT

# Divison
cube['INT/INT'] = Type.INT
cube['INT/FLOAT'] = Type.FLOAT
cube['INT/CHAR'] = Type.INT
cube['FLOAT/INT'] = Type.FLOAT
cube['FLOAT/FLOAT'] = Type.FLOAT
cube['CHAR/INT'] = Type.INT
cube['CHAR/CHAR'] = Type.INT

# Multiplication
cube['INT*INT'] = Type.INT
cube['INT*FLOAT'] = Type.FLOAT
cube['INT*CHAR'] = Type.INT
cube['FLOAT*INT'] = Type.FLOAT
cube['FLOAT*FLOAT'] = Type.FLOAT
cube['CHAR*INT'] = Type.INT
cube['CHAR*CHAR'] = Type.INT

# Equal
cube['BOOL==BOOL'] = Type.BOOL
cube['INT==INT'] = Type.BOOL
cube['INT==FLOAT'] = Type.BOOL
cube['INT==CHAR'] = Type.BOOL
cube['FLOAT==INT'] = Type.BOOL
cube['FLOAT==FLOAT'] = Type.BOOL
cube['CHAR==INT'] = Type.BOOL
cube['CHAR==CHAR'] = Type.BOOL

# Unequal
cube['BOOL!=BOOL'] = Type.BOOL
cube['INT!=INT'] = Type.BOOL
cube['INT!=FLOAT'] = Type.BOOL
cube['INT!=CHAR'] = Type.BOOL
cube['FLOAT!=INT'] = Type.BOOL
cube['FLOAT!=FLOAT'] = Type.BOOL
cube['CHAR!=INT'] = Type.BOOL
cube['CHAR!=CHAR'] = Type.BOOL

# Less
cube['INT<INT'] = Type.BOOL
cube['INT<FLOAT'] = Type.BOOL
cube['INT<CHAR'] = Type.BOOL
cube['FLOAT<INT'] = Type.BOOL
cube['FLOAT<FLOAT'] = Type.BOOL
cube['CHAR<INT'] = Type.BOOL
cube['CHAR<CHAR'] = Type.BOOL

# Greater
cube['INT>INT'] = Type.BOOL
cube['INT>FLOAT'] = Type.BOOL
cube['INT>CHAR'] = Type.BOOL
cube['FLOAT>INT'] = Type.BOOL
cube['FLOAT>FLOAT'] = Type.BOOL
cube['CHAR>INT'] = Type.BOOL
cube['CHAR>CHAR'] = Type.BOOL

# Less and equal
cube['INT<=INT'] = Type.BOOL
cube['INT<=FLOAT'] = Type.BOOL
cube['INT<=CHAR'] = Type.INT
cube['FLOAT<=INT'] = Type.BOOL
cube['FLOAT<=FLOAT'] = Type.BOOL
cube['CHAR<=INT'] = Type.BOOL
cube['CHAR<=CHAR'] = Type.BOOL

# Greater and equal
cube['INT>=INT'] = Type.BOOL
cube['INT>=FLOAT'] = Type.BOOL
cube['INT>=CHAR'] = Type.BOOL
cube['FLOAT>=INT'] = Type.BOOL
cube['FLOAT>=FLOAT'] = Type.BOOL
cube['CHAR>=INT'] = Type.BOOL
cube['CHAR>=CHAR'] = Type.BOOL

# && and ||
cube['BOOL&&BOOL'] = Type.BOOL
cube['BOOL||BOOL'] = Type.BOOL

def getResultType(leftType, operator, rightType):
  l = leftType.name
  r = rightType.name
  key = l + operator + r
  if not key in cube.keys():
    return -1
  else:
    return cube[key]
