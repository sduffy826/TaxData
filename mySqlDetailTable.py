import mySqlRoutines as spdSql
import mySqlCategory as catSql

DEBUGIT = False

validCategories = []

def deleteDetailRecordById(id):
  spdSql.init()
  if spdSql.DEBUGIT:
    print("mySqlDetailTable-deleteDetailRecordById id: {0}".format(id))
  
  sqlStmt = """delete from corti.tax_detail where id=%s"""
  if spdSql.doUpdate:
    spdSql.cursor.execute(sqlStmt,(id, ))
    spdSql.connection.commit()
  return


def deleteDetailRecordsForYear(taxYear):
  spdSql.init()
  if spdSql.DEBUGIT:
    print("mySqlDetailTable-deleteDetailRecordsForYear forYear: {0}".format(taxYear))

  sqlStmt = """delete from corti.tax_detail where taxYear=%s"""
  if spdSql.doUpdate:   
    spdSql.cursor.execute(sqlStmt,(taxYear, ))
    spdSql.connection.commit()
  return 

def deleteDetailRecordsForYearAndCategory(taxYear, category):
  spdSql.init()
  if spdSql.DEBUGIT:
    print("mySqlDetailTable-deleteDetailRecordsForYearAndCategory forYear: {0} category: {1}".format(taxYear, category))

  sqlStmt = """delete from corti.tax_detail where taxYear=%s and category=%s"""
  if spdSql.doUpdate:   
    spdSql.cursor.execute(sqlStmt,(taxYear, category))
    spdSql.connection.commit()
  return   

def getDetailRecordById(id):
  spdSql.init()
  sqlStmt = """select * from corti.tax_detail where id=%s"""
  spdSql.cursor.execute(sqlStmt,(id,))
  mapOfValues = spdSql.cursor.fetchone()
  spdSql.connection.commit()
  if spdSql.DEBUGIT:
    print("mySqlDetailTable-getDetailRecordById")
    for aCol in mapOfValues:
      print(str(aCol))
  return mapOfValues

def getDetailRecordsForYearAndCategory(taxYear, category):
  spdSql.init()
  sqlStmt = """select * from corti.tax_detail where taxYear=%s and category=%s"""
  spdSql.cursor.execute(sqlStmt,(taxYear, category))
  dictOfValues = spdSql.cursor.fetchall()
  spdSql.connection.commit()
  if spdSql.DEBUGIT:
    print("mySqlDetailTable-getDetailRecordByYearAndCategory")
    for aRow in dictOfValues:
      print(str(aRow))
  return dictOfValues

def getDetailRecordsForYear(taxYear):
  spdSql.init()
  sqlStmt = """select * from corti.tax_detail where taxYear=%s order by sheetName, lineNumber, lineSubNumber"""
  spdSql.cursor.execute(sqlStmt,(taxYear,))
  dictOfValues = spdSql.cursor.fetchall()
  spdSql.connection.commit()
  if spdSql.DEBUGIT:
    print("mySqlDetailTable-getDetailRecordsForYear")
    for aRow in dictOfValues:
      print(str(aRow))
  return dictOfValues

# Convert list of dictionary (category) items just to have their value
def catToListHelper(listOfDict):
  rtnArray = []
  if DEBUGIT:
    print("In catToListHelper {0}".format(str(listOfDict)))
  for anItem in listOfDict:
    if DEBUGIT:
      print(anItem)
    rtnArray.append(anItem["category"])
  return rtnArray

def getDistinctCategories():
  spdSql.init()
  sqlStmt = """select distinct category from corti.tax_detail order by 1"""
  spdSql.cursor.execute(sqlStmt)
  listOfDictOfValues = spdSql.cursor.fetchall()
  spdSql.connection.commit()
  if spdSql.DEBUGIT:
    print("mySqlDetailTable-getDistinctCategories")
    for aRow in listOfDictOfValues:
      print(str(aRow))
  return catToListHelper(listOfDictOfValues)

def getDistinctCategoriesForYear(taxYear):
  spdSql.init()
  sqlStmt = """select distinct category from corti.tax_detail where taxYear=%s order by 1"""
  spdSql.cursor.execute(sqlStmt,(taxYear,))
  listOfDictOfValues = spdSql.cursor.fetchall()
  spdSql.connection.commit()
  if spdSql.DEBUGIT:
    print("mySqlDetailTable-getDistinctCategoriesForYear")
    for aRow in listOfDictOfValues:
      print(str(aRow))
  return catToListHelper(listOfDictOfValues)

# Insert record into the table
def insertDetailRecord(_taxYear, _sheetName, _itemDate, _description, _amount,
                       _category, _notesRef, _notesRefSub, _source, _lineNumber,
                       _lineSubNumber, _runningTotal, _frequency, _refOrCheckNum,
                       _memoOrIdentifier, _iagCode, _iagIdentifier, _break):  
  global validCategories                       
  spdSql.init()

  if len(validCategories) == 0: # Have valid categories?  if not get em
    validCategories = catSql.getCategoryDict()

  sqlStmt = """insert into corti.tax_detail (taxYear, sheetName, itemDate, description, amount, \
                                             category, notesRef, notesRefSub, source, lineNumber, \
                                             lineSubNumber, runningTotal, frequency, refOrCheckNum, \
                                            memoOrIdentifier, iagCode, iagIdentifier, break) \
                          values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
  if spdSql.DEBUGIT:
    print("mySqlDetailTable-insertDetailRecord: {0}".format(sqlStmt))

  if _category not in validCategories:
    print("Processing terminated!!  Category invalid: {0}".format(_category))
    exit(996)

  if spdSql.doUpdate:
    spdSql.cursor.execute(sqlStmt,(_taxYear, _sheetName, _itemDate, _description, _amount, \
                                  _category, _notesRef, _notesRefSub, _source, _lineNumber, \
                                  _lineSubNumber, _runningTotal, _frequency, _refOrCheckNum, \
                                  _memoOrIdentifier, _iagCode, _iagIdentifier, _break))
    spdSql.connection.commit()    
  return

# Update with args passed in
def updateDetailRecord(_id, _taxYear, _sheetName, _itemDate, _description, _amount,
                      _category, _notesRef, _notesRefSub, _source, _lineNumber,
                      _lineSubNumber, _runningTotal, _frequency, _refOrCheckNum,
                      _memoOrIdentifier, _iagCode, _iagIdentifier, _break):
  global validCategories
  spdSql.init()
  
  if len(validCategories) == 0: # Have valid categories?  if not get em
    validCategories = catSql.getCategoryDict()

  sqlStmt = """update corti.tax_detail set taxYear=%s, sheetName=%s, itemDate=%s, \
                description=%s, amount=%s, category=%s, notesRef=%s, notesRefSub=%s, \
                source=%s, lineNumber=%s, lineSubNumber=%s, runningTotal=%s, \
                frequency=%s, refOrCheckNum=%s, memoOrIdentifier=%s, iagCode=%s, \
                iagIdentifier=%s, break=%s where id=%s"""
  if spdSql.DEBUGIT:
    print("mySqlDetailTable.py-updateDetailRecord: {0}".format(sqlStmt))

  if _category not in validCategories:
    print("Processing terminated!!  Category invalid: {0}".format(_category))
    exit(995)

  if spdSql.doUpdate:
    spdSql.cursor.execute(sqlStmt,(_taxYear, _sheetName, _itemDate, _description, _amount,
                                   _category, _notesRef, _notesRefSub, _source, _lineNumber,
                                   _lineSubNumber, _runningTotal, _frequency, _refOrCheckNum,
                                   _memoOrIdentifier, _iagCode, _iagIdentifier, _break , _id))
    spdSql.connection.commit()

  return

# Update based on dictionary record passed in
def updateDetailRecordFromDict(dictRecord):
  updateDetailRecord(dictRecord["id"], dictRecord["taxYear"], dictRecord["sheetName"], dictRecord["itemDate"],
                     dictRecord["description"], dictRecord["amount"], dictRecord["category"],
                     dictRecord["notesRef"], dictRecord["notesRefSub"], dictRecord["source"],
                     dictRecord["lineNumber"], dictRecord["lineSubNumber"], dictRecord["runningTotal"],
                     dictRecord["frequency"], dictRecord["refOrCheckNum"], dictRecord["memoOrIdentifier"],
                     dictRecord["iagCode"], dictRecord["iagIdentifier"], dictRecord["break"])
  return