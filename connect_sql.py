import mysql.connector
import pandas as pd

def connect():
    mydb = mysql.connector.connect(
        host         = "localhost",
        user         = "root",
        passwd       = "12345678",
        ssl_disabled = "True",
        database     = "nbaStats"
    )

    return mydb

def createDatabase(dbname):

    mydb = connect()
    mycursor = mydb.cursor()

    sqlFormula = "CREATE DATABASE " + dbname
    # create a database with given name
    mycursor.execute(sqlFormula)

    #show us the available databases
    result = mycursor.execute("SHOW DATABASES")

    retVal = False

    for elem in result:
        if elem == dbname:
            retVal = True

    return retVal


def addColumnsSQL(columnNames):

    mydb = connect()

    mycursor = mydb.cursor()

    #Create a table with givemn columns and column sizes in given databse
    columns = columnNames
    #["name", "age"]

    #mycursor.execute("CREATE TABLE playerStats (name VARCHAR (255))")

    for elem in columns[1:]:
        mycursor.execute("ALTER TABLE playerStats ADD " + elem + " FLOAT(4,2) NOT NULL")

    return

#change the data type of a specific column
def changeColumnType(name, type):

    mydb = connect()

    mycursor = mydb.cursor()

    mycursor.execute("ALTER TABLE playerStats MODIFY COLUMN " + name + " " + type)

    return

def addDataSQL(columnNames, playerData):

    mydb = connect()

    mycursor = mydb.cursor()

    #mydb.commit()

    #show us the available tables
    '''mycursor.execute("SHOW TABLES")'''

    #insert the following tuples !!!!IF YOU MAKE A CHANGE TO DB YOU NEED TO ADD mydb.commit()!!!!

    columns = "(" + columnNames[0]

    for elem in columnNames[1:]:
        add = ", " + elem
        columns += add

    columns += ")"

    values = "(%s"

    for elem in columnNames[1:]:
        values = values + ", " + "%s"

    values += ")"

    sqlFormula = "INSERT INTO playerStats " + columns + " VALUES " + values

    #sqlFormula = "INSERT INTO practicePlayers (name, season) VALUES (%s, %s)"=

    mycursor.executemany(sqlFormula, playerData)

    mydb.commit()

    '''for i in range(0, playerData[len(columnNames[0])]):
           for elem in columnNames:'''

    '''players = [("Lebron James", [2018, 2019]),
               ("James Harden", [2018, 2019]),
               ("Kevin Durant", [2020, 2021])]

    mycursor.executemany(sqlFormula, players)

    mydb.commit()'''

    return

#columnArr contains the columns name, comparisonTerms is either LIKE or = and valueArr is the specific value to be looking for
#NOTE: remember that if you use like to add % where other characters are expected in the valueArr
def retrieveDataSQL(columnArr, comparisonTerms, valueArr, tableName):

    sqlFormula = "SELECT * FROM " + tableName + " WHERE"

    multiple = False

    for i in range(len(columnArr)):
        if multiple:
            sqlFormula += " AND"
        addCondition = " " + columnArr[i] + " " + comparisonTerms[i] + " " + "'" + valueArr[i] + "'"
        sqlFormula += addCondition
        multiple = True

    mydb = connect()
    mycursor = mydb.cursor()

    mycursor.execute(sqlFormula)

    #fetchone can also be used to retrieve only on entry
    result = mycursor.fetchall()


    return result

#return specific columns from given table
def returnColumns(columns, table):

    mydb = connect()
    mycursor = mydb.cursor()

    sqlFormula = "SELECT " + columns[0]
    #Return the columns with these specific names
    for i in range(1, len(columns)):
        add =  ", " + columns[i]
        sqlFormula += add


    sqlFormula += " FROM " + table

    mycursor.execute(sqlFormula)
    
    myresult = mycursor.fetchall() #or fetchone

    #drops all NaN in a pd dataframe
    #myresult.dropna()

    return myresult


#update a elem in the table - not sure if currently necessary since I am taking in data directly from csv
def updateElem():

    #update the value of an entry with given parameters
    '''sql = "UPDATE practicePlayers SET season=%s WHERE name=%s"
    mycursor.execute(sql, (2019, "Kevin Durant"))'''

    #Limit to a specific number of returned values
    '''mycursor.execute("SELECT * FROM practicePlayers LIMIT 2 OFFSET 2") #OFFSET makes you start that many entries later
    
    myresult = mycursor.fetchall()
    
    for result in myresult:
        print(result)'''

    return

#mode is the criteria by which the elements should be ordered, i.e. DESC
def orderTable(column, mode, tableName):

    mydb = connect()
    mycursor = mydb.cursor()

    #Order items in a certain way: default is increasing, desc makes it decreasing(descending)
    order = "SELECT * from " + tableName +  " ORDER BY " + column + " " + mode
    
    mycursor.execute(order)
    
    myresult = mycursor.fetchall()
    
    return


def deleteElem(columnArr, comparisonTerms, valueArr, tableName):

    mydb = connect()
    mycursor = mydb.cursor()

    #DELETES all elements that match given parameters, need commmit because you are making change to table
    sqlFormula = "DELETE FROM " + tableName + " WHERE"

    multiple = False

    for i in range(len(columnArr)):
        if multiple:
            sqlFormula += " AND"
        addCondition = " " + columnArr[i] + " " + comparisonTerms[i] + " " + "'" + valueArr[i] + "'"
        sqlFormula += addCondition
        multiple = True

    mycursor.execute(deleteElem)
    
    mydb.commit()

    return

def dropColumn(columns, tableName):

    mydb = connect()
    mycursor = mydb.cursor()

    sqlFormula = "ALTER TABLE " + tableName

    first = ""
    for elem in columns:
        add = first + " DROP " + elem
        sqlFormula += add
        first = ","

    mycursor.execute(sqlFormula)

def deleteTable(tableName):

    mydb = connect()

    mycursor = mydb.cursor()

    #Removes a table from the databse. IF EXISTS is a failsafe so that you dont get an error if the table does not exist
    dropTable = "DROP TABLE IF EXISTS " + tableName
    
    mycursor.execute(dropTable)
    
    mydb.commit

    return

if __name__ == '__addColumnsSQL__':
    addColumnsSQL()
