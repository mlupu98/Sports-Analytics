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
from sklearn import linear_model, preprocessing
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
from connect_sql import returnColumns, retrieveDataSQL, get_column_names

#uses panda to read csv file
def read_data_csv(filename, columns):

    #read file into dataframe
    data = pd.read_csv(filename, sep=",")

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
def train_model(correctedData, predict, filename):

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

        model = KNeighborsClassifier(n_neighbors = 11)

        model.fit(x_train, y_train)

        accuracy = model.score(x_test, y_test)


        #check accuracy and replace results if this run has better results
        if accuracy > highestAccuracy:

            with open(filename, "wb") as f:
                pickle.dump(model, f)

    print("Accuracy: \n", accuracy)

    return x_test, y_test, filename



#print regression results
def print_results(x_test, y_test, filename):


    pickle_in = open(filename, "rb")
    linear = pickle.load(pickle_in)


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

    i = 0

    print("HERE")

    for elem in data.columns:
        data.drop(data.index[data[elem] == "-99.0"], inplace=True)
        print("HERE2")
        print(len(data[elem]))
        if i == len(data.columns)-1:
            for i in range(len(data[elem])):
                if data[elem][i] == "SG" or data[elem][i] == "PG":
                    data[elem][i] = "G"
                elif data[elem][i] == "PF" or data[elem][i] == "C":
                    data[elem][i] = "BIG"



        i += 1

    return data

def main():

    #allCols = get_column_names("nbaPlayerStats")
    columns = np.asarray(["assists", "turnovers", "blocks", "steals", "all_rebounds", "3PT_attempts", "pos"])

    predict = "pos"
    #data = read_data_csv("Tennis-Major-Tournaments-Match-Statistics/AusOpen-women-2013.csv", columns)

    cols = get_column_names("nbaPlayerStats")

    data = read_data_sql("nbaPlayerStats", ['name', 'season'], ['LIKE', 'LIKE'], ['%', '201%'])

    df = create_df(cols, data, columns)

    cleanData = remove_nan(df)

    filename = "knn_pickle"

    x_test, y_test, pickleName = train_model(cleanData, predict, filename)

    print_results(x_test, y_test, pickleName)



    return

if __name__ == '__main__':
    main()