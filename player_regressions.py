import csv
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import pickle
import tensorflow
import keras
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
from connect_sql import returnColumns, retrieveDataSQL, get_column_names

#uses panda to read csv file
def read_data_csv(filename, columns):

    #read file into dataframe
    data = pd.read_csv(filename, sep=",")

    #selectedData = data[["Result", "FSP.1", "ACE.1", "FSW.1", "BPC.1", "BPW.1", "NPA.1", "NPW.1", "TPW.1"]]
    #selectedData = data[["Result", "BPW.1", "FSW.1", "TPW.1"]]

    #choose columns of interest
    selectedData = data[columns]

    #number of data entries
    size = len(data[columns[0]])

    #drop all NaN
    correctedData = selectedData.dropna()

    return correctedData




def read_data_sql(tableName, columnArr, comparisonTerms, valueArr):

    data = retrieveDataSQL(tableName, columnArr, comparisonTerms, valueArr)

    return data



#predict is the variable that you want to predict
def train_model(correctedData, predict):

    #seperate prediction variable from the rest
    X = np.array(correctedData.drop([predict], 1))
    Y = np.array(correctedData[predict])

    print(X)
    print(Y)

    highestAccuracy = -1000

    #find the most accurate training model
    for i in range(20):

        #train the model on 90% of the data
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size = 0.1)

        #run linear regression
        linear = linear_model.LinearRegression()

        linear.fit(x_train, y_train)

        accuracy = linear.score(x_test, y_test)

        filename = "LBJ.pickle"


        #check accuracy and replace results if this run has better results
        if accuracy > highestAccuracy:

            with open(filename, "wb") as f:
                pickle.dump(linear, f)

    print("Accuracy: \n", accuracy)

    return x_test, y_test, filename



#print regression results
def print_results(x_test, y_test, filename):


    pickle_in = open(filename, "rb")
    linear = pickle.load(pickle_in)


    print("Coefficient: \n", linear.coef_)
    print("Intercept: \n", linear.intercept_)

    predictions = linear.predict(x_test)

    for x in range(len(predictions)):
        print(predictions[x], x_test[x], y_test[x])

    return



#graph results
def graph_results(correctedData, xplot, yplot):

    style.use("ggplot")
    plt.scatter(correctedData[xplot], correctedData[yplot])

    plt.xlabel(xplot)
    plt.ylabel(yplot)
    plt.show()

    return




def create_csv(filename, cols, data):

    with open(filename, 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(data)

def create_df(headings, data, cols):

    series = np.asarray(data)

    df = pd.DataFrame(series, columns = headings)

    return df[cols]



def remove_nan(data):

    for elem in data.columns:
        data.drop(data.index[data[elem] == "-99.0"], inplace=True)

    return data

def main():

    columns = ["blocks", "steals", "turnovers", "fouls"]

    predict = columns[-1]

    #data = read_data_csv("Tennis-Major-Tournaments-Match-Statistics/AusOpen-women-2013.csv", columns)

    cols = get_column_names("nbaPlayerStats")

    data = read_data_sql("nbaPlayerStats", ['name'], ['LIKE'], ['%'])

    df = create_df(cols, data, columns)

    cleanData = remove_nan(df)

    x_test, y_test, pickleName = train_model(cleanData, predict)

    print_results(x_test, y_test, pickleName)



    return

if __name__ == '__main__':
    main()