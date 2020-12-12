import sys

import mySqlCategoryRemap as remapSql

if __name__ == "__main__":

  if 1 == 1:  # Insert a record
    remapSql.insertRemappedRecord("Auto - Ticket","Auto - Misc")

  if 1 == 1:  # Test dump data for year
    theDict = remapSql.getCategoryRemap()
    print("Remapped listing:")
    for theKey in theDict.keys():
      print("OldValue: {0}  NewValue: {1}".format(theKey,theDict[theKey]))
  
  if 1 == 0:
    remapSql.deleteCategoryRemap("foo")
