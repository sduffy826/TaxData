import sys

import mySqlMisc as miscSql
import getSpreadsheetData as getData

import pandas as pd 
from datetime import datetime

if __name__ == "__main__":
  # Insert a record (this handles inserts and updates) arguments to function:
  #   taxYear, catgory, description, Notes/Ref and amount.  The taxYear/description
  #   are the lookup key to the misc table
  if 1 == 0:
    miscSql.updateMisc(2020, "CortiCategory", "CortiGroup", "Cool dogs", 213.92)

  # Get category for a year/description
  if 1 == 0:
    print(miscSql.getMiscCategoryForYearDescription(2019,"CortiGroup"))

  # Get id for a year/description
  if 1 == 0:
    print(miscSql.getMiscIdForYearDescription(2019,"CortiGroup"))

  # See if on file
  if 1 == 0:
    print(miscSql.isOnFileMisc(2019,"CortiGroup"))

  if 1 == 1:    
    listOfDict = miscSql.getAllMiscDict()
    for aRow in listOfDict:
      print(str(aRow))

  if 1 == 0:
    print("Records deleted: {0}".format(miscSql.deleteMisc(2019,"CortiGroup")))

  # Get values from spreadsheet and update table
  if 1 == 0:
    listOfDict = getData.getMiscSheetData("/home/dev/taxes/miscellaneousItems.ods")
    for aRow in listOfDict:
      miscSql.updateMisc(aRow["taxYear"], aRow["category"], aRow["description"], aRow["notesRef"], aRow["amount"] )
      print(str(aRow))
