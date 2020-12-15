import sys
import os

import mysqlUtils as myUtil
import mySqlCategoryRemap as remapSql
import mySqlCategory as catSql

from pandas_ods_reader import read_ods

DEBUGIT = False

validCategories = []

chars2Change = {
  "–" : "-" 
}

programDictionary = {
  "sheetName"       : "AllDetail",           # The sheet name
  "spreadsheetName" : "deleteme.oss",        # Default spreadsheet name
  "remapName"       : "remapCategories.ods"  # Remap of categories  
}

# This has the names of the columns in the spreadsheet that we're interested in; they should be the same for any 
# sheet we'll pull from.
sheetColumnDictionary = {
  "dateColName"           : {"xcelName" : "Date", "tabColName" : "itemDate", "tabColType" : "D", "nullable" : False, "required" : True},
  "descriptionColName"    : {"xcelName" : "Description", "tabColName" : "description", "tabColType" : "C", "nullable" : False, "required" : True},
  "amountColName"         : {"xcelName" : "Amount", "tabColName" : "amount", "tabColType" : "F", "nullable" : False, "required" : True},
  "categoryColName"       : {"xcelName" : "Category", "tabColName" : "category", "tabColType" : "C", "nullable" : False, "required" : True},
  "notesRefColName"       : {"xcelName" : "Notes/Ref", "tabColName" : "notesRef", "tabColType" : "C", "nullable" : False, "required" : False},
  "notesRefSubColName"    : {"xcelName" : "Notes/Ref Sub", "tabColName" : "notesRefSub", "tabColType" : "C", "nullable" : False, "required" : False},
  "sourceColName"         : {"xcelName" : "Source", "tabColName" : "source", "tabColType" : "C", "nullable" : False, "required" : True},
  "lineNumColName"        : {"xcelName" : "Line#", "tabColName" : "lineNumber", "tabColType" : "I", "nullable" : False, "required" : True},
  "subNumColName"         : {"xcelName" : "SubLine", "tabColName" : "lineSubNumber", "tabColType" : "I", "nullable" : True, "required" : False},
  "runTotalColName"       : {"xcelName" : "Run total", "tabColName" : "runningTotal", "tabColType" : "F", "nullable" : True, "required" : False},
  "frequencyColName"      : {"xcelName" : "Frequency", "tabColName" : "frequency", "tabColType" : "I", "nullable" : False, "required" : False},
  "refCheckNumColName"    : {"xcelName" : "Ref/Check#", "tabColName" : "refOrCheckNum", "tabColType" : "C", "nullable" : False, "required" : False},
  "memoIdentifierColName" : {"xcelName" : "Memo/Identifier", "tabColName" : "memoOrIdentifier", "tabColType" : "C", "nullable" : False, "required" : False},
  "iAGCodeColName"        :	{"xcelName" : "IAG Code", "tabColName" : "iagCode", "tabColType" : "C", "nullable" : False, "required" : False},
  "iAGIdentifierColName"  : {"xcelName" : "IAG Identifier", "tabColName" : "iagIdentifier", "tabColType" : "C", "nullable" : False, "required" : False},
  "breakColName"          : {"xcelName" : "Break", "tabColName" : "break", "tabColType" : "C", "nullable" : False, "required" : False}
}

# This is the old one, when I had the remapped values in a spreadsheet, it's
# now in a table, so this isn't necessary any longer
# --------------------------------------------------------------------------
def getCategoryRemapSpreadsheet(fileName):
  if os.path.exists(fileName) == False:
    print("Category Remap Spreadsheet does not exist, exiting")
    exit(99)
    
  df = read_ods(fileName,0) 
  remapped = {}  
  for row in range(len(df.index)):
    theCategory = df.iloc[row,0]
    if len(theCategory) > 0:
      remapped[df.iloc[row,0]] = df.iloc[row,1]  # col 0 has name, col 1 has name to map to
  return remapped  

# Get summary data, we're passed in the dictionary of category remapping
# ----------------------------------------------------------------------
def getCategorySummaryData():
  global validCategories
  
  catName   = sheetColumnDictionary["categoryColName"]["xcelName"]
  totName   = sheetColumnDictionary["runTotalColName"]["xcelName"]
  breakName = sheetColumnDictionary["breakColName"]["xcelName"]
  
  categoryRemap = remapSql.getCategoryRemap()
  if len(validCategories) == 0: # Have valid categories?  if not get em
    validCategories = catSql.getCategoryDict()
    print("Got validCategories, len({0})".format(len(validCategories)))
  
  # Returns an array where each row in the array is another array containing category and total
  rtnArray = []
  if os.path.exists(programDictionary["spreadsheetName"]) == False:
    print("Spreadsheet: {0} does not exist, exiting".format(programDictionary["spreadsheetName"]))
    exit(99)

  df = read_ods(programDictionary["spreadsheetName"], programDictionary["sheetName"])
  badData = False
  for row in range(len(df.index)):
    if df.loc[row,breakName].upper() == 'Y':
      if DEBUGIT:
        print(str(df.loc[row]))
      categoryName = df.loc[row,catName]
      for char2Change in chars2Change.keys():
        categoryName = categoryName.replace(char2Change,chars2Change[char2Change])
        print("Category changed to: {0}".format(categoryName))
      if categoryName in categoryRemap:
        if DEBUGIT:
          print("remapped category: {0} to {1}".format(categoryName,categoryRemap[categoryName]))
        categoryName = categoryRemap[categoryName]

      if categoryName not in validCategories:
        print("Processing terminated!!  Category invalid: {0}".format(categoryName))
        badData = True    

      rtnArray.append(list((categoryName,df.loc[row,totName])))
  
  if badData:
    exit(993)
  return rtnArray


# Get categories classisifed as 'living expenses', the spreadsheet should have a column
# identifier of 'Category'
# -------------------------------------------------------------------------------------
def getLivingExpenseCategories(theFile):  
  categoryRemap = remapSql.getCategoryRemap()
  if os.path.exists(theFile) == False:
    print("Spreadsheet: {0} does not exist, exiting".format(theFile))
    exit(99)
  
  rtnArray = []
  df = read_ods(theFile,"Sheet1")
  for row in range(len(df.index)):
    theCategory = df.loc[row,"Category"]
    theFlag     = df.loc[row,"Living Expense"]
    for char2Change in chars2Change.keys():
      theCategory = theCategory.replace(char2Change,chars2Change[char2Change])
    if theCategory in categoryRemap:
      print("Category: {0} remapped to: {1}".format(theCategory,categoryRemap[theCategory]))
      theCategory = categoryRemap[theCategory]
      
    rtnArray.append([theCategory,theFlag])
  return rtnArray

# Get categories classisifed as 'living expenses', the spreadsheet should have a column
# identifier of 'Category'
# -------------------------------------------------------------------------------------
def getMiscSheetData(theFile):  
  if os.path.exists(theFile) == False:
    print("Spreadsheet: {0} does not exist, exiting".format(theFile))
    exit(99)
  
  rtnArray = []
  df = read_ods(theFile,"Sheet1")
  for row in range(len(df.index)):    
    if myUtil.isNull(df.loc[row,"taxYear"]) == False:        
      taxYear  = myUtil.formatSqlVar(df.loc[row,"taxYear"],"I",False)  # args: field, datatype (Int/Float/Char), isNullable
      amount   = myUtil.formatSqlVar(df.loc[row,"amount"],"F",False)
      notesRef = myUtil.formatSqlVar(df.loc[row,"Notes/ref"],"C",False) 
      dictItem = { "taxYear" : taxYear, \
                   "category" : df.loc[row,"category"], \
                   "description" : df.loc[row,"description"], \
                   "amount" : amount, \
                   "notesRef" : notesRef }    
      rtnArray.append(dictItem)
    
  return rtnArray


# Get summary data, we're passed in the dictionary of category remapping
# ----------------------------------------------------------------------
def getSheetDetail():
  # Returns an array where each row in the array is another array containing category and total
  global validCategories

  rtnArray = []  
  if os.path.exists(programDictionary["spreadsheetName"]) == False:
    print("Spreadsheet: {0} does not exist, exiting")
    exit(99)

  categoryRemap = remapSql.getCategoryRemap()
  if len(validCategories) == 0: # Have valid categories?  if not get em
    validCategories = catSql.getCategoryDict()
    if 1 == 0:
      print("Valid categories:")
      for aCat in validCategories.keys():
        print(":{0}:".format(aCat))

  df = read_ods(programDictionary["spreadsheetName"], programDictionary["sheetName"])

  # We'll validate the columns
  dfColumnList = list(df.columns)
  if DEBUGIT:
    for theCol in dfColumnList:
      print(theCol)
  badColumns    = False
  badCategories = {}
  theColumnKeys = sheetColumnDictionary.keys()
  
  rowIdx = 1 # Header is at 1
  for row in range(len(df.index)):
    rowIdx = rowIdx + 1
    theRecord  = {}
    skipRecord = False
    for colKey in theColumnKeys:
      colName = sheetColumnDictionary[colKey]["xcelName"]
      
      tableColName = sheetColumnDictionary[colKey]["tabColName"]
      tableColType = sheetColumnDictionary[colKey]["tabColType"]
      isNullable   = sheetColumnDictionary[colKey]["nullable"]
      isRequired   = sheetColumnDictionary[colKey]["required"]

      isCategoryColumn = False
      if colKey == "categoryColName":
        isCategoryColumn = True

      if DEBUGIT:
        print("Getting value for row: {0} column: {1}".format(row,colName))

      if isRequired and myUtil.isNull(df.loc[row,colName]):
        skipRecord = True
      elif not colName in dfColumnList:
        print("*** Column name not in spreadsheet {0}".format(colName))
        badColumns = True
      else:
        # Get value and ensure correct format
        theValue = myUtil.formatSqlVar(df.loc[row,colName],tableColType,isNullable)
        if isCategoryColumn:
          # Fix bad characters :)
          for char2Change in chars2Change.keys():
            theValue = theValue.replace(char2Change,chars2Change[char2Change])
          if theValue in categoryRemap:
            theValue = categoryRemap[theValue]
          if theValue not in validCategories:
            if theValue not in badCategories:
              print("Processing terminated!!  Category invalid:{0}: row{1}".format(theValue, rowIdx))
              badCategories[theValue] = 1
            else:
              badCategories[theValue] = badCategories[theValue] + 1
      
        theRecord[tableColName] = theValue
      
    if skipRecord == False:
      rtnArray.append(theRecord)
    else:
      print("*** Record skipped at row: {0}".format(rowIdx))
    
    if DEBUGIT:
      print("Added Record: {0}".format(str(theRecord)))
    
    if badColumns:
      print("\nHas bad columns, terminating!!")
      exit(997)

  if len(badCategories) > 0:
    exit(992)

  return rtnArray

# Display help - on parms
# -----------------------
def help():
  print("\n\nYou can override the following args by passing in the key and value pair(s)")
  print("as arguments when you invoke the program.  Here's the current key/values:")
  for theKey in programDictionary:
    print("  key: {0}     value: {1}".format(theKey,programDictionary[theKey]))

# Process the program arguments, they are in the form key value key2 value2 ...
# -----------------------------------------------------------------------------
def procParms(listOfParms):
  numParms = len(listOfParms) // 2
  for idx in range(numParms):
    theKey   = listOfParms[idx*2]
    theValue = listOfParms[idx*2+1]
    print("Mapped: {0} to: {1}".format(theKey,theValue))
    if theKey in programDictionary:
      programDictionary[theKey] = theValue
      if DEBUGIT:
        print("Mapped: {0} to: {1}".format(theKey,theValue))
    else:
      if DEBUGIT:
        print("Unknown key: {0}, was ignored".format(theKey))

# Just for testing, output data
# -----------------------------
def testDetail(numRecords2Print=99999): 
  detailData = getSheetDetail()
  for row in range(min(len(detailData),numRecords2Print)):
    print("Detail record: {0}".format(str(detailData[row])))
  return

# Just for testing, output data
# -----------------------------
def testSummary(): 
  print(1)
  summaryData = getCategorySummaryData()  
  print(200)
  for row in range(len(summaryData)):
    catName      = summaryData[row][0]
    runningTotal = summaryData[row][1]
    print("cat: {0} total: {1}".format(catName,runningTotal))
  return

# -------------------------------------------------------------------------------------------
if __name__ == "__main__":
  if len(sys.argv) < 2:
    help()
    argList = []
  else:
    argList = sys.argv[1:]
 
  procParms(argList)  # Process program arguments
  
  # Test that the summary data is good
  if 1 == 0:
    testSummary()
  
  # Test that the detail is good
  if 1 == 1:
    testDetail(5)

  if 1 == 0:
    print(str(getLivingExpenseCategories(programDictionary["spreadsheetName"])))

  # See the category listings
  if 1 == 0:
     aList = catSql.getCategoryList()
     print(str(aList))