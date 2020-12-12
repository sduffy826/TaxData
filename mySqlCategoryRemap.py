import mySqlRoutines as spdSql

def deleteCategoryRemap(category):
  spdSql.init()
  sqlStmt = """delete from corti.tax_category_remap where category=%s"""
  spdSql.cursor.execute(sqlStmt,(category, ))
  spdSql.connection.commit()
  if spdSql.DEBUGIT:
    print("mySqlDetailTable-deleteCategoryRemap")

def getCategoryRemap():
  spdSql.init()
  sqlStmt = """select category, remappedCategory from corti.tax_category_remap order by category"""
  spdSql.cursor.execute(sqlStmt)
  listOfValues = spdSql.cursor.fetchall()
  spdSql.connection.commit()
  if spdSql.DEBUGIT:
    print("mySqlDetailTable-getCategoryRemap")
  rtnDict = {}
  for aRow in listOfValues:
    if spdSql.DEBUGIT:
      print("Old: {0} New: {1}".format(aRow["category"],aRow["remappedCategory"]))
    rtnDict[aRow["category"]] = aRow["remappedCategory"]
  return rtnDict

# Insert record into the table
def insertRemappedRecord(category, remappedCategory):  
  spdSql.init()

  sqlStmt = """insert into corti.tax_category_remap (category, remappedCategory) values(%s, %s)"""
  if spdSql.DEBUGIT:
    print("mySqlDetailTable-insertRemappedRecord: {0}".format(sqlStmt))

  if spdSql.doUpdate:
    spdSql.cursor.execute(sqlStmt,(category, remappedCategory))
    spdSql.connection.commit()    
  return
