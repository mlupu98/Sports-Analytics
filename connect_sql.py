import mysql.connector
import pandas as pd

def connect():
    mydb = mysql.connector.connect(
        host         = "localhost",
        user         = "root",
        passwd       = "mcsr7531",
        ssl_disabled = "True",
        database     = "nbaStats"
    )

    return mydb



#Creates a database and takes in the db name as a parameter
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



#create a table and initialize the first column - can't create table without any columns
def createTable(tableName, firstCol, firstColType):

    mydb = connect()

    mycursor = mydb.cursor()

    sqlFormula = "CREATE TABLE " + tableName + " (" + firstCol + " " + firstColType + ")"

    mycursor.execute(sqlFormula)



#adds columns to table
def addColumnsSQL(tableName, columnNames, columnTypes):

    mydb = connect()

    mycursor = mydb.cursor()

    #Create a table with givemn columns and column sizes in given databse
    for i in range(len(columnNames)):
        mycursor.execute("ALTER TABLE " + tableName + " ADD " + columnNames[i] + " " + columnTypes[i] + " NOT NULL")

    return



#change the data type of a specific column
def changeColumnType(name, type):

    mydb = connect()

    mycursor = mydb.cursor()

    mycursor.execute("ALTER TABLE playerStats MODIFY COLUMN " + name + " " + type)

    return



#Insert values into the table
def addDataSQL(tableName, columnNames, playerData):

    mydb = connect()

    mycursor = mydb.cursor()

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

    sqlFormula = "INSERT INTO " + tableName + " " + columns + " VALUES " + values

    mycursor.executemany(sqlFormula, playerData)

    mydb.commit()

    return



#columnArr contains the columns name, comparisonTerms is either LIKE or = and valueArr is the specific value to be looking for
#NOTE: remember that if you use like to add % where other characters are expected in the valueArr
def retrieveDataSQL(tableName, columnArr, comparisonTerms, valueArr):

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



#return specified columns from given table
def returnColumns(tableName, columns):

    mydb = connect()
    mycursor = mydb.cursor()

    sqlFormula = "SELECT " + columns[0]
    #Return the columns with these specific names
    for i in range(1, len(columns)):
        add =  ", " + columns[i]
        sqlFormula += add


    sqlFormula += " FROM " + tableName

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



#delete an element from a specified table
def deleteElemSQL(tableName, columnArr, comparisonTerms, valueArr):

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

    mycursor.execute(sqlFormula)
    
    mydb.commit()

    return



#remove a colum from specified table
def dropColumns(tableName, columns):

    mydb = connect()
    mycursor = mydb.cursor()

    sqlFormula = "ALTER TABLE " + tableName

    first = ""
    for elem in columns:
        add = first + " DROP " + elem
        sqlFormula += add
        first = ","

    mycursor.execute(sqlFormula)



#delete a specified table
def deleteTableSQL(tableName):

    mydb = connect()

    mycursor = mydb.cursor()

    #Removes a table from the databse. IF EXISTS is a failsafe so that you dont get an error if the table does not exist
    dropTable = "DROP TABLE IF EXISTS " + tableName
    
    mycursor.execute(dropTable)
    
    mydb.commit

    return



if __name__ == '__addColumnsSQL__':
    addColumnsSQL()
