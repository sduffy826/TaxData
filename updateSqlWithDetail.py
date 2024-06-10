import sys

import mySqlDetailTable as detailSql

import getSpreadsheetData as getData

def dumpDetailForCategoryAndYear(theYear, category):
  theListOfDict = detailSql.getDetailRecordsForYearAndCategory(theYear, category)
  for aRow in theListOfDict:
    print("Got row: {0}".format(str(aRow)))
  return

def dumpDetailForYear(theYear):
  theListOfDict = detailSql.getDetailRecordsForYear(theYear)
  for aRow in theListOfDict:
    print("Got row: {0}".format(str(aRow)))
  return

def updateDetailDataFromSpreadsheet(theYear):
  # Get the data from the spreadsheet
  theList   = getData.getSheetDetail()
  sheetName = getData.programDictionary["sheetName"]
  print("Got {0} records from sheet: {1}".format(len(theList),sheetName))
  if len(theList) > 0:
    detailSql.deleteDetailRecordsForYear(theYear)
    for aRow in theList:     
      # print("Category:{0}, Description:{1}, lineNumber:{2}".format(aRow["category"],aRow["description"],aRow["lineNumber"]))
      detailSql.insertDetailRecord(theYear, sheetName, aRow["itemDate"], aRow["description"], aRow["amount"],
                                  aRow["category"], aRow["notesRef"], aRow["notesRefSub"], aRow["source"],aRow["lineNumber"],
                                  aRow["lineSubNumber"],aRow["runningTotal"],aRow["frequency"],aRow["refOrCheckNum"],
                                  aRow["memoOrIdentifier"],aRow["iagCode"],aRow["iagIdentifier"],aRow["break"])

if __name__ == "__main__":
  if 1 == 0:  # Test dump data for year
    dumpDetailForYear(2019)
  
  if 1 == 1:  # Test loading data from spreadsheet into table
    argList = []
    theYear = 0
    if len(sys.argv) > 1:  # Pos sys.argv[0] is the program name
      theYear = int(sys.argv[1])
      if len(sys.argv) > 2:
        argList = sys.argv[2:]
  
    if theYear == 0:
      print("Must pass year and optional arguments into this routine")
    else:
      getData.procParms(argList)
      if 1 == 1:
        updateDetailDataFromSpreadsheet(theYear)  # Update sql table
      if 1 == 0:
        print(str(getData.programDictionary)) # Show the programDictionary values
      if 1 == 0:
        categoryList = detailSql.getDistinctCategories() # Show category list
        print(str(categoryList))
      if 1 == 0:
        categoryList = detailSql.getDistinctCategoriesForYear(2019) # Show categories for year
        print(str(categoryList))