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


def graph_distances(tableName, columnNames):

    shotStats = returnColumns(tableName, columnNames)

    shotTally = {}

    for elem in shotStats:

        if elem[0] not in shotTally:
            shotTally[elem[0]] = [0,0]

        if elem[1] == "made":
            shotTally[elem[0]][0] += 1

        shotTally[elem[0]][1] += 1


    shotPercentages = [[],[]]
    shotCount       = [[], []]
    expectedValue   = [[], []]


    for elem in sorted(shotTally.keys()):

        if shotTally[elem][1] > 100:

            perc = 100*(shotTally[elem][0]/shotTally[elem][1])
            count = shotTally[elem][0] + shotTally[elem][1]
            value = shotTally[elem][0]/shotTally[elem][1]

            shotPercentages[0].append(elem)
            shotPercentages[1].append(perc)

            shotCount[0].append(elem)
            shotCount[1].append(count)

            if elem > 23.7:
                value *= 3
            else:
                value *= 2

            expectedValue[0].append(elem)
            expectedValue[1].append(value)


    #Graphs the change in made shot percentage over shot distance
    plt.plot(shotPercentages[0], shotPercentages[1])
    plt.xlabel('Shot Distance in Feet')
    plt.ylabel('Percentage of Shots Made')
    plt.xticks(np.arange(0, 30, 1))
    plt.show()

    #Graphs the number of shots take over shot distance
    plt.plot(shotCount[0], shotCount[1])
    plt.xlabel('Shot Distance in Feet')
    plt.ylabel('Number of Shots Taken')
    plt.xticks(np.arange(0, 30, 1))
    plt.show()

    #Graphs the expected value of a certain shot over shot distance
    plt.plot(expectedValue[0], expectedValue[1])
    plt.xlabel('Shot Distance in Feet')
    plt.ylabel('Expected Value of Shot')
    plt.xticks(np.arange(0, 30, 1))
    plt.show()

    return


def main():

    tableName = "nbaShotStats"
    columnName = ["SHOT_DIST", "SHOT_RESULT"]

    graph_distances(tableName, columnName)

    return

if __name__ == "__main__":
    main()