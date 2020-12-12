import mysql.connector
from mysql.connector import Error
import mySqlConnectionVars as cv 

connectionState = 0
connection      = None
cursor          = None
doUpdate        = True
DEBUGIT         = False

def getServerInfo():
  if connectionState == 1:
    return connection.get_server_info()
  else:
    return None

def setUpdateMode(theMode):
  global doUpdate
  doUpdate = theMode

def cleanup():
  global connectionState, connection, cursor
  if connectionState == 1:
    if (connection.is_connected()):
      connection.close()
    cursor = None
    connectionState = 0

  
# Routine to get connection, cursor, it will terminate the program if it fails by default
def init(failOnError = True):
  global connection, cursor, connectionState
  if DEBUGIT:
    print("In mySqlRoutines.init(), connectionState: {0}".format(connectionState))
    print("host:{0}, database:{1}, userid:{2}, passwork:{3}".format(cv.host, cv.database, cv.user, cv.password))
  try:
    if connectionState != 1:
      connectionState = -1  # Default to failure state
      connection = mysql.connector.connect(host=cv.host, database=cv.database, user=cv.user, password=cv.password)
      if connection.is_connected():
        cursor          = connection.cursor(dictionary=True)  # Want dictionary values
        connectionState = 1  # Connected
  except Error as e:
    print("Error encountered: ",e)
  finally:
    if connectionState != 1:
      if failOnError:
        print("Failure on init, terminating program")
        exit(999)