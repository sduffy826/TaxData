import mySqlRoutines as spdSql

# Delete record by key taxYear and description
def deleteMisc(taxYear, description):
  spdSql.init()
  sqlStmt = """delete from corti.tax_misc where taxYear=%s and description=%s"""
  spdSql.cursor.execute(sqlStmt,(taxYear, description))
  spdSql.connection.commit()
  if spdSql.DEBUGIT:
    print("mySqlCategory-deleteMisc")
  return spdSql.cursor.rowcount

# Return boolean representing if on file 
def isOnFileMisc(taxYear, description):
  return (getMiscCategoryForYearDescription(taxYear, description) is not None)

# Get the category for a given 'misc' record, search by taxYear and description
# Note: there could be more than one record for taxYear/description, but there
# shouldn't be, so only one value is returned
def getMiscCategoryForYearDescription(taxYear, description):    
  spdSql.init()
  sqlStmt = """select category from corti.tax_misc where taxYear=%s and description=%s"""
  spdSql.cursor.execute(sqlStmt,(taxYear, description))
  theValue = spdSql.cursor.fetchall() # Done just in case more than one record exists
  spdSql.connection.commit()
  if spdSql.DEBUGIT:
    print("mySqlCategory-getMiscCategoryForYearDescription is:{0}".format(theValue))
 
  if len(theValue) > 0:
    return theValue[0]["category"] 
  else:
    return None

# Get the category for a given 'misc' record, search by taxYear and description
def getMiscIdForYearDescription(taxYear, description):
  spdSql.init()
  sqlStmt = """select id from corti.tax_misc where taxYear=%s and description=%s"""
  spdSql.cursor.execute(sqlStmt,(taxYear, description))
  theValue = spdSql.cursor.fetchall()  # Just in case more than 1, we only return 1 though
  spdSql.connection.commit()
  if spdSql.DEBUGIT:
    print("mySqlCategory-getMiscIdForYearDescription is:{0}".format(theValue))
 
  if len(theValue) == 0:
    return None
  else:
    return theValue[0]["id"]

# Get all the records on file, return as a dictionary
def getAllMiscDict():
  spdSql.init()
  sqlStmt = """select id, taxYear, category, description, notesRef, amount from corti.tax_misc order by category, description, taxYear"""
  spdSql.cursor.execute(sqlStmt)
  listOfValues = spdSql.cursor.fetchall()
  spdSql.connection.commit()
  if spdSql.DEBUGIT:
    print("mySqlCategory-getAllMiscDict")
  return listOfValues

# Get all records, return as a list
def getAllMiscList():
  dictList = getAllMiscDict()
  if spdSql.DEBUGIT:
    print("mySqlCategory-getAllMiscList")
  rtnArray = []
  for aRow in dictList:
    if spdSql.DEBUGIT:
      print(str(aRow))
    rtnArray.append([ aRow["id"], aRow["taxYear"], aRow["category"], aRow["description"], aRow["notesRef"], aRow["amount"] ])
  return rtnArray

# Insert record into the table, code should not call this, should call updateMisc instead, that will
# update or insert as necessary
def insertMisc(taxYear, category, description, notesRef, amount):  
  spdSql.init()

  sqlStmt = """insert into corti.tax_misc (taxYear, category, description, notesRef, amount) values(%s, %s, %s, %s, %s)"""
  if spdSql.DEBUGIT:
    print("mySqlCategory-insertMisc: {0}".format(sqlStmt))
  
  if spdSql.doUpdate:       
    spdSql.cursor.execute(sqlStmt,(taxYear, category, description, notesRef, amount))
    spdSql.connection.commit()    
  return

# Update the misc record, this function will either update the existing record
# or insert a new record (if it didn't exist)
def updateMisc(taxYear, category, description, notesRef, amount):  
  recordId = getMiscIdForYearDescription(taxYear, description)
  if recordId is not None:
    spdSql.init()
    sqlStmt = """update corti.tax_misc set category=%s, notesRef=%s, amount=%s where id=%s"""
    if spdSql.DEBUGIT:
      print("mySqlCategory-updateMisc: {0}".format(sqlStmt))

    if spdSql.doUpdate:
      spdSql.cursor.execute(sqlStmt,(category, notesRef, amount, recordId))
      spdSql.connection.commit()    
    else:
      pass
  else:
    insertMisc(taxYear, category, description, notesRef, amount)  
  return
