#! FanDuel Golf Comp

import pandas as pd
import os
import matplotlib.pyplot as plt
from tabulate import tabulate
from pprint import pprint
import time
from pulp import *

import logging
logging.basicConfig(level=logging.DEBUG,
			 format=' %(asctime)s - %(levelname)s- %(message)s')


logging.debug('Start of Program')

#road = 'C:\\Users\\ngoodroe\\Desktop'
road = r'/Users/goodroe/Dropbox/Python/Pandas'

#Teams according to FanDuel



if os.getcwd() != road:
	os.chdir(road)
	logging.debug('File Path Fixed')



logging.debug('New dataframe')

fd = pd.read_csv('FanDuel-PGA-2019-08-22-37788-players-list.csv')
fd = fd.set_index('Nickname')
fd.index.names = ['Name']

fd['Score'] = (fd.Salary * fd.FPPG)**(.5)
fd = fd[fd.Score.notnull()]


df = fd

#df = df[df['Injury Indicator'] != 'O']

### MANUAL TAKEOUT
# df = df[df.index != 'Kawhi Leonard']
#df = df[df.index != 'Billy Hurley']

###

players = []
for total in range(len(df)):
	players.append([df.iloc[total]['Position'],
					df.index[total],
					df.iloc[total].Salary,
					df.iloc[total].Score]) #FPPG to Score

playernum = [str(i) for i in range(len(df.index))]
cost = {str(i): df.iloc[i]['Salary'] for i in range(len(df.index))}
pts  = {str(i): df.iloc[i]['Score']  for i in range(len(df.index))} #FPPG to Score


model = LpProblem('Fantasy Golf', LpMaximize)

player_var = LpVariable.dicts('Player',playernum,0,1,LpBinary)

model += lpSum([pts[i]*player_var[i] for i in playernum]),'TotalScore'
model += lpSum([cost[i]*player_var[i] for i in playernum]) <= 60000
model += lpSum([player_var[i] for i in playernum]) == 6

status = model.solve()
LpStatus[model.status]

best = []
lineup = []
totalcost = 0
totalfant = 0
totalpoints = 0


for var in player_var:
	var_value = player_var[var].varValue
	if var_value == 1:
		best.append(var)

for each in best:
	lineup.append(players[int(each)])

for each in lineup:
	totalcost += each[2]
	totalfant += each[3]

lineup.append(['Total','',totalcost,totalfant])
titles = ['Pos','Name','Price','Score']

print(tabulate(lineup,headers = titles))




