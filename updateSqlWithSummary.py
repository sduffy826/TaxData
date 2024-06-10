import sys
# from decimal import *
from datetime import datetime

import mySqlSummaryTable as summSql
import mySqlCategory as catSql
import pandas as pd

"""
def dumpAllSummary():
  theListOfDict = summSql.getAllSummaryRecords()
  for aRow in theListOfDict:
    print("Got row: {0}".format(str(aRow)))
    # theNum = float(aRow["runningTotal"])
    # print("theNum: {0} type: {1}".format(theNum, type(theNum) ) )  
    print("runningTotal: {0} type: {1}".format(aRow["runningTotal"], type(aRow["runningTotal"]) ) )

def dumpSummaryForYear(theYear):
  theListOfDict = summSql.getSummaryRecordsForYear(theYear)
  for aRow in theListOfDict:
    print("Got row: {0}".format(str(aRow)))
  return

def updateSummaryDataFromSpreadsheet(theYear):
  # Get the data from the spreadsheet
  theList = getData.getCategorySummaryData()
  if len(theList) > 0:
    summSql.deleteSummaryRecordsForYear(theYear)
    for aRow in theList:
      print("Category {0} Amount {1}".format(aRow[0],aRow[1]))
      summSql.insertSummaryRecord(theYear,aRow[0],aRow[1])  # Category and amount

"""

if __name__ == "__main__":
  # Show the dictionary with all the years that we have defined in the dictionary, if we
  # need to store additional values just modify the table (tax_summary) and update the 
  # array at the top of mySqlSummaryTable.py... that's all that's required
  if 1 == 0:
    print(summSql.getDictOfYearValues())

  # Get the valid years as a list instead of a dictionary
  if 1 == 0:
    print(summSql.getListOfValuesFromDict(summSql.getDictOfYearValues()))

  # Show the sql statement that we'll build
  if 1 == 0:
    print(summSql.getSqlStatement())

  # Get all summary records in the table
  if 1 == 0:
    summaryRecordsList = summSql.getAllSummaryRecords()
    for aRecord in summaryRecordsList:
      print(str(aRecord))

  # Get all summary records and write them to taxSummaryYYYYMMDD_HHMMSS.csv
  if 1 == 1:
    summaryRecordsList = summSql.getAllSummaryRecords()
    catDictList        = catSql.getCategoryDict()
    print(catDictList)
    for catKey in catDictList.keys(): # Add values for keys not in row
        print("catKey:{0}:".format(catKey))
        print("record:{0}".format(str(catDictList[catKey])))
    
    # Update each summary record to include the flags from catDictList
    for aRow in summaryRecordsList:
      theCategory = aRow["category"]
      for catKey in catDictList[theCategory].keys(): # Add values for keys not in row
        print("catKey:{0}:".format(catKey))
        if catKey not in aRow:
          aRow[catKey] = catDictList[theCategory][catKey]

    df = pd.DataFrame(summaryRecordsList) # Create dataframe
    outputFile = "~/taxes/taxSummary" + datetime.today().strftime('%Y%m%d_%H%M%S') + ".csv"
    df.to_csv(outputFile)
    print("Data written to: {0}".format(outputFile))

  # Delete all the summary records on file
  if 1 == 0:
    summSql.deleteAllSummaryRecords()

  # This builds the summary records based on the data in the detail table, it will delete/add
  # any records found... if you renamed categories then you probably want to uncomment
  # block above to delete all the summary data on file.
  if 1 == 0:
    summaryRecordsFromDetail = summSql.getSummaryFromDetailTable()
    
    for aRecord in summaryRecordsFromDetail:
      if 1 == 1: # Debugging
        print(str(aRecord))
      summSql.insertSummaryRecord(aRecord)
