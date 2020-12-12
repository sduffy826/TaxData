import mySqlRoutines as spdSql
import mySqlCategory as catSql
import decimal

yearsOfData = [2016, 2017, 2018, 2019, 2020]

def deleteSummaryRecord(category):
  spdSql.init()
  if spdSql.DEBUGIT:
    print("mySqlSummaryTable-deleteSummaryRecord category: {0}".format(category))
  
  sqlStmt = """delete from corti.tax_summary where category=%s"""
  spdSql.cursor.execute(sqlStmt,(category, ))
  spdSql.connection.commit()
  return

def deleteAllSummaryRecords():
  spdSql.init()
  if spdSql.DEBUGIT:
    print("mySqlSummaryTable-deleteAllSummaryRecords")
  
  sqlStmt = """delete from corti.tax_summary"""
  spdSql.cursor.execute(sqlStmt)
  spdSql.connection.commit()
  return 

# Return a dictionary that has a key for eacy year, and value is 0
def getDictOfYearValues():
  tempDict = {}
  for aYear in yearsOfData:
    tempDict[aYear] = 0.0
  return tempDict

# Take the dictionary of year values and return them as a list
def getListOfValuesFromDict(dictOfValues):
  if spdSql.DEBUGIT:
    print("getListOfValuesFromDict:{0}".format(str(dictOfValues)))
  tempList = []
  for aYear in yearsOfData:
    tempList.append(float(dictOfValues[aYear]))
    # tempList.append(decimal.Decimal(dictOfValues[aYear]))
    # tempList.append(dictOfValues[aYear])
  return tempList

# Return a string that represents the insert statement, useing this we're not hardcoded
# for the years
def getSqlStatement():
  theString = "insert into corti.tax_summary (category"
  valString = "(%s"
  for aYear in yearsOfData:
     theString = theString + ", `" + str(aYear) + "`"
     valString = valString + ", %s"
  theString = theString + ") values" + valString + ")"
  return theString

def getAllSummaryRecords():
  spdSql.init()
  sqlStmt = """select * from corti.tax_summary order by category"""
  spdSql.cursor.execute(sqlStmt)
  dictOfValues = spdSql.cursor.fetchall()
  spdSql.connection.commit()
  if spdSql.DEBUGIT:
    print("mySqlSummaryTable.py-getSummaryRecord")
    for aRow in dictOfValues:
      print(str(aRow))      
  return dictOfValues

def getSummaryRecord(category):
  spdSql.init()
  sqlStmt = """select * from corti.tax_summary where category=%s"""
  spdSql.cursor.execute(sqlStmt,(category, ))
  dictOfValues = spdSql.cursor.fetchall()
  spdSql.connection.commit()
  if spdSql.DEBUGIT:
    print("mySqlSummaryTable-getSummaryRecord")
    for aRow in dictOfValues:
      print(str(aRow))
  return dictOfValues

def getSummaryFromDetailTable():
  spdSql.init()
  sqlStmt = """select category, taxYear, sum(amount) as yearTot \
               from corti.tax_detail \
               group by category, taxYear \
               order by 1,2"""
  spdSql.cursor.execute(sqlStmt)
  dictOfValues = spdSql.cursor.fetchall()
  spdSql.connection.commit()
  if spdSql.DEBUGIT:
    print("mySqlSummaryTable-getSummaryFromDetailTable")
    for aRow in dictOfValues:
      print(str(aRow))

  dictOfValues.append({"category" : "ZZZZ", "taxYear" : 9999, "yearTot" : 5.4}) # For end of list processing
  RtnArray = []
  lastCategory = "zstart"
  recordToLoad = []
  dictOfYearValues = {}  # Just for initialization
  for aRecord in dictOfValues:
    if aRecord["category"] != lastCategory:
      if lastCategory != "zstart": # If not the first record append it
        recordToLoad = recordToLoad + getListOfValuesFromDict(dictOfYearValues)
        if spdSql.DEBUGIT:       
          print("recordToLoad:{0}".format(str(recordToLoad)))
        
        RtnArray.append(recordToLoad.copy()) # Need copy since clearing below changes record

      # Prep data areas for the new record       
      lastCategory = aRecord["category"]
      recordToLoad.clear() 
      recordToLoad.append(lastCategory)
      dictOfYearValues.clear()
      dictOfYearValues = getDictOfYearValues()  # Get initized dictionary to use
    
    # Put summed value into the dictionary
    theYear = aRecord["taxYear"]
    dictOfYearValues[theYear] = aRecord["yearTot"]
    if spdSql.DEBUGIT:
      print("theYear:{0}: yearToT:{1}: dict:{2}".format(theYear,aRecord["yearTot"],str(dictOfYearValues)))

  if spdSql.DEBUGIT:
    print("===============================================")
    for index in range(len(RtnArray)):
      print(str(RtnArray[index]))

  return RtnArray

# Insert the record passed in, it should be a list where first column is the category
# followed by values for each year in the table
def insertSummaryRecord(listRecord):
  spdSql.init()

  sqlStmt     = getSqlStatement()
  theCategory = listRecord[0]
  if spdSql.DEBUGIT:
    print("mySqlSummaryTable-insertSummaryRecord: {0}".format(sqlStmt))

  if spdSql.doUpdate:
    deleteSummaryRecord(theCategory)
    tupleOfValues = tuple(listRecord)
    spdSql.cursor.execute(sqlStmt,tupleOfValues)
    spdSql.connection.commit()    
  return

# Update record, since the insert does a delete and add call it
def updateSummaryRecord(listRecord):
  insertSummaryRecord(listRecord)
  return
