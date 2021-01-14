import sys

import mySqlDetailTable as detailSql
import mySqlCategory as catSql
import getSpreadsheetData as getData

import pandas as pd 
from datetime import datetime

if __name__ == "__main__":
  # Insert the categories that are in the detail table
  if 1 == 0:  
    listOfCatFromDetail = detailSql.getDistinctCategories()
    for aCat in listOfCatFromDetail:
      catSql.insertCategory(aCat, "Y", "A", " ")  # Default everything to Y/A/blank
    listOfCats = catSql.getCategoryList()
    for rowOfData in listOfCats:
      print(str(rowOfData))

  # Insert a new category into table
  if 1 == 1:  
    # Format: category, isExpense, reportCode (A-Accountant, P-Personal), livingExpense (Y-es S-eany...)
    # Idea is livingExpense is things that are required to live
    list2Ins = [ ["Mortgage", "Y", "A", "Y"], 
                 ["529 Fund", "Y", "A", " "], 
                 ["Dog", "Y", "P", "Y"], 
                 ["Florida House", "Y", "A", " "] ]
    # Override var 01/11/2021 for new elelments 
    list2Ins = [ ["Deposit - Unemployment", "N", "P", " "],
                 ["Deposit - UPS", "N", "P", " "] ]

    for aRow in list2Ins:
      theCat = aRow[0]
      isExpense = aRow[1]
      reportCode = aRow[2]
      livingExp  = aRow[3]
      catSql.insertCategory(theCat, isExpense, reportCode, livingExp)

  
  # Insert one item
  if 1 == 0:  
    # Format: category, isExpense, reportCode (A-Accountant, P-Personal), livingExpense (Y-es S-eany or blank)
    catSql.insertCategory("Vacation", "Y", "A","N")
  

  # Delete a category by name
  if 1 == 0:
    catSql.deleteCategory("category2Delete")

  # Show all the categories, output of each record {id, category, isExpense, reportCode}
  if 1 == 0:
    listOfCats = catSql.getCategoryList()
    for rowOfData in listOfCats:
      print(str(rowOfData))      

  # Get all the categories and write them to ~/taxes/categoriesOnFileYYYYMMDD_HHMMSS.csv
  if 1 == 0:
    dictListOfCats = catSql.getCategoryDictList()
    df = pd.DataFrame(dictListOfCats)
    outputFile = "~/taxes/categoriesOnFile" + datetime.today().strftime('%Y%m%d_%H%M%S') + ".csv"
    df.to_csv(outputFile)
    print("Data written to {0}".format(outputFile))


  # Get dictionary of categories, keys are the categories, the value for each is the category record (as dict object)
  if 1 == 1:
    listOfCategories = catSql.getCategoryDict()
    for catKey in listOfCategories:
      print("Category {0} data: {1}".format(catKey, str(listOfCategories[catKey])))

  # Get the living expenses from the spreadsheet and update the table
  if 1 == 0:
    theFile = "/home/dev/taxes/livingExpenseCategories.ods"
    livingExpenseList = getData.getLivingExpenseCategories(theFile)

    for aRow in livingExpenseList:
      # print("cat: {0} flag: {1}".format(aRow[0],aRow[1]))
      catSql.updateLivingExpenseForCategory(aRow[0],aRow[1])
