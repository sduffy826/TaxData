import mySqlRoutines as spdSql

def deleteCategory(category):
  spdSql.init()
  sqlStmt = """delete from corti.tax_category where category=%s"""
  spdSql.cursor.execute(sqlStmt,(category, ))
  spdSql.connection.commit()
  if spdSql.DEBUGIT:
    print("mySqlCategory-deleteCategory")

def getCategoryDictList():
  spdSql.init()
  sqlStmt = """select id, category, isExpense, reportCode, livingExpense from corti.tax_category order by category"""
  spdSql.cursor.execute(sqlStmt)
  listOfValues = spdSql.cursor.fetchall()
  spdSql.connection.commit()
  if spdSql.DEBUGIT:
    print("mySqlCategory-getCategoryDictList")
  return listOfValues

def getCategoryList():
  dictList = getCategoryDictList()
  if spdSql.DEBUGIT:
    print("mySqlCategory-getCategoryList")
  rtnArray = []
  for aRow in dictList:
    if spdSql.DEBUGIT:
      print(str(aRow))
    rtnArray.append([ aRow["id"], aRow["category"], aRow["isExpense"], aRow["reportCode"], aRow["livingExpense"] ])
  return rtnArray

# Get dictionary of categories, the key is the category, the value is a dictionary representing it's record
def getCategoryDict():
  rtnDict = {}
  listOfCats = getCategoryDictList()
  for aRow in listOfCats:
    if spdSql.DEBUGIT:
      print(str(aRow))
    rtnDict[aRow["category"]] = aRow.copy()
  return rtnDict


# Insert record into the table
def insertCategory(category, isExpense, reportCode, livingExpense):  
  spdSql.init()

  sqlStmt = """insert into corti.tax_category (category, isExpense, reportCode, livingExpense) values(%s, %s, %s, %s)"""
  if spdSql.DEBUGIT:
    print("mySqlCategory-insertCategory: {0}".format(sqlStmt))

  if spdSql.doUpdate:
    spdSql.cursor.execute(sqlStmt,(category, isExpense, reportCode, livingExpense))
    spdSql.connection.commit()    
  return

# Update livingExpense column for specific category
def updateLivingExpenseForCategory(category, livingExpense):  
  spdSql.init()

  sqlStmt = """update corti.tax_category set livingExpense=%s where category=%s"""
  if spdSql.DEBUGIT:
    print("mySqlCategory-updateLivingExpenseForCategory: {0}".format(sqlStmt))

  if spdSql.doUpdate:
    spdSql.cursor.execute(sqlStmt,(livingExpense, category))
    spdSql.connection.commit()    
  return
