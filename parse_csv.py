
import csv
import math
import numpy as np
from collections import defaultdict
import pandas as pd
#import matplotlib.pyplot as plt
from connect_sql import addColumnsSQL, addDataSQL, changeColumnType, retrieveDataSQL, returnColumns

#Extract data from the csv file
def extractData(filename):
    players = {}

    with open(filename, "r") as csvFile:
        df = pd.read_csv(csvFile)
        players['name'] = df.Player
        players['season'] = df.Year
        players['age'] = df.Age
        players['team'] = df.Tm
        players['games_played'] = df.G
        players['games_started'] = df.GS
        players['min_played'] = df.MP
        players['3PT_rate'] = df.ThreePAr  # 3PT/FGA
        players['FT_rate'] = df.FTr  # FT/FGA
        players['total_RB_perc'] = df.TRBperc
        players['assist_perc'] = df.ASTperc
        players['steal_perc'] = df.STLperc
        players['block_perc'] = df.BLKperc
        players['turnover_perc'] = df.TOVperc
        players['FG'] = df.FG
        players['FG_attempts'] = df.FGA
        players['FG_perc'] = df.FGperc
        players['2PT'] = df.TwoP
        players['2PT_attempts'] = df.TwoPA
        players['2PT_perc'] = df.TwoPperc
        players['3PT'] = df.ThreeP
        players['3PT_attempts'] = df.ThreePA
        players['3PT_perc'] = df.ThreePperc
        players['FT'] = df.FT
        players['FT_attempts'] = df.FTA
        players['FT_perc'] = df.FTperc
        players['Off_rebounds'] = df.ORB
        players['Def_rebounds'] = df.DRB
        players['all_rebounds'] = df.TRB
        players['assists'] = df.AST
        players['steals'] = df.STL
        players['blocks'] = df.BLK
        players['turnovers'] = df.TOV
        players['fouls'] = df.PF
        players['points'] = df.PTS


    return players

#Create a dictionary that uses the player name as the key
def createPlayerDictionary(players):

    playerStats = defaultdict()
    playerArr    = []

    row = 0

    for name in players['name']:
        if name not in playerStats:
            playerStats[name] = []

        newStats = []
        newStats.append(players['name'][row])               #0
        newStats.append(players['season'][row])             #1
        newStats.append(players['age'][row])                #2
        newStats.append(players['team'][row])               #3
        newStats.append(players['games_played'][row])       #4
        newStats.append(players['games_started'][row])      #5
        newStats.append(players['min_played'][row])         #6
        newStats.append(players['3PT_rate'][row])           #7
        newStats.append(players['FT_rate'][row])            #8
        newStats.append(players['total_RB_perc'][row])         #9
        newStats.append(players['assist_perc'][row])           #10
        newStats.append(players['steal_perc'][row])            #11
        newStats.append(players['block_perc'][row])            #12
        newStats.append(players['turnover_perc'][row])         #13
        newStats.append(players['FG'][row])                 #14
        newStats.append(players['FG_attempts'][row])        #15
        newStats.append(players['FG_perc'][row])               #16
        newStats.append(players['2PT'][row])                #17
        newStats.append(players['2PT_attempts'][row])       #18
        newStats.append(players['2PT_perc'][row])              #19
        newStats.append(players['3PT'][row])                #20
        newStats.append(players['3PT_attempts'][row])       #21
        newStats.append(players['3PT_perc'][row])              #22
        newStats.append(players['FT'][row])                 #23
        newStats.append(players['FT_attempts'][row])        #24
        newStats.append(players['FT_perc'][row])               #25
        newStats.append(players['Off_rebounds'][row])       #26
        newStats.append(players['Def_rebounds'][row])       #27
        newStats.append(players['all_rebounds'][row])       #28
        newStats.append(players['assists'][row])            #29
        newStats.append(players['steals'][row])             #30
        newStats.append(players['blocks'][row])             #31
        newStats.append(players['turnovers'][row])          #32
        newStats.append(players['fouls'][row])              #33
        newStats.append(players['points'][row])             #34
        playerStats[name].append(newStats)
        playerArr.append(newStats)
        row += 1

    return playerStats, playerArr

#make sure there are non NaN - don't want to remove incomplete entries because some analysis might only need columsn that are present
#might not need this
def prepareDataSQL(playerData):

    arrangedData = createPlayerDictionary(playerData)

    playerArr = arrangedData[1]

    for elem in playerArr:
        for i in range(len(elem)):
            if isinstance(elem[i], float):
                if math.isnan(elem[i]):
                    elem[i] = -99.0


    return playerArr

#graph practice
def scoring_graph(player_stats):

    total_points = []
    season = []
    fg_attempts = []

    for year in player_stats:
        season.append(year[1]-1.0)
        total_points.append(year[34])
        fg_attempts.append(year[24])

    return season, total_points, fg_attempts

def main():

    filename = 'nba-players-stats/Seasons_Stats.csv'
    #playerData = extractData(filename)

    '''columns = []
    for elem in playerData.keys():
        columns.append(elem)'''
    #addColumnsSQL(columns)
    data = {}

    #playerData = prepareDataSQL(playerData)

    columns     = ["name", "season"]
    comparisons = ["LIKE", "="]
    values      = ["Le%", "2017"]
    table       = "playerStats"

    #retrieveDataSQL(columns, comparisons, values, table)

    '''for elem in columns:
        if elem != "name" and elem != "team":
            changeColumnType(elem, "FLOAT(7,3)")'''



    returnColumns(["turnovers"], "playerStats")
    #addDataSQL(columns, playerData)


    '''print(player_dic["LeBron James"][0])'''


    '''LBJ = scoring_graph(player_dic['LeBron James'])
    KD  = scoring_graph(player_dic['Kevin Durant'])
    JH  = scoring_graph(player_dic['James Harden'])


    start_season = min(min(LBJ[0]), min(KD[0]), min(JH[0]))
    end_season   = max(max(LBJ[0]), max(KD[0]), max(JH[0]))

    seasons = np.arange(start_season, end_season)

    plt.plot(LBJ[0], LBJ[1])
    plt.plot(LBJ[0], LBJ[2])

    plt.plot(KD[0], KD[1])
    plt.plot(KD[0], KD[2])

    plt.plot(JH[0], JH[1])
    plt.plot(JH[0], JH[2])

    plt.legend(['LeBron Points', 'LeBron FG Attempts', 'Durant Points', 'Durant FG Attempts', 'Harden Points', 'Harden FG Attempts'])

    plt.xticks(np.arange(start_season, end_season + 1, 1.0))

    plt.show()'''

    return

if __name__ == '__main__':
    main()