import sys
import os
import math

# Return true if variable is not a number (only valid on float types)
def isNotANumber(theVar):
  rtnValue = False
  if (isinstance(theVar,float)):
    rtnValue = math.isnan(theVar)
  return rtnValue

# Return true if the variable is null (none) or not a number
def isNull(theVar):
  rtnValue = (theVar is None)
  if not rtnValue:
    rtnValue = isNotANumber(theVar)
  return rtnValue

def formatSqlVar(theVar, theType, isNullable):
  if isNullable and isNull(theVar):    
    newVar = None
  else:
    if isNull(theVar):  # Means it's not a nullable if isNull is true
      if theType == 'D': # Shouldn't happen, assign null string
        newVar = ""
      elif theType == 'C': # Use empty string
        newVar = ""
      elif theType == 'I':
        newVar = 0
      elif theType == 'F':
        newVar = 0.0
    else:  # Means the value is not null
      newVar = theVar
      if theType == 'C':
        newVar = str(theVar)
      elif theType == 'I':
        newVar = int(theVar)
      elif theType == 'F':
        newVar = float(theVar)
  return newVar




