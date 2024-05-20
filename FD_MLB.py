#FD Baseball

import pandas as pd
import os
import matplotlib.pyplot as plt
from tabulate import tabulate
from pprint import pprint
import time
import statsmodels.api as sm
from pulp import *

import logging
logging.basicConfig(level=logging.DEBUG,
			 format=' %(asctime)s - %(levelname)s- %(message)s')
logging.debug('Start of Program')

#road = 'C:\\Users\\ngoodroe\\Downloads'
road = r'/Users/goodroe/Dropbox/Python/Pandas'
if os.getcwd() != road:
	os.chdir(road)
	logging.debug('File Path Fixed')

fd = pd.read_csv('FanDuel-MLB-2019-08-24-37912-players-list.csv')
fd = fd.set_index('Nickname')
df = pd.read_csv('MLBFD.csv')
df = df.set_index('Player')

x = pd.concat([df,fd],axis=1)


x = x[x['Injury Indicator'] != 'IL']
x = x[['Position','FPPG','Salary','Projection']]
x = x.dropna()
x = x.loc[:,~x.columns.duplicated()]


x['Score'] = (x['FPPG']*x['Salary']*x['Projection']**2)**(1/4)

#{'2B', 'OF', '3B', 'P', 'C', '1B', 'SS'}

players = []
players = []
for total in range(len(x)):
	players.append([x.iloc[total]['Position'],
					x.index[total],
					x.iloc[total].Score,
					x.iloc[total].Salary,
					x.iloc[total].Projection])

playernum = [str(i) for i in range(len(x.index))]
sbplayers = {str(i): 1 if (x.iloc[i]['Position'] == '2B') else 0 for i in range(len(x.index))}
ofplayers = {str(i): 1 if (x.iloc[i]['Position'] == 'OF') else 0 for i in range(len(x.index))}
tbplayers = {str(i): 1 if (x.iloc[i]['Position'] == '3B') else 0 for i in range(len(x.index))}
pplayers  = {str(i): 1 if (x.iloc[i]['Position'] == 'P')  else 0 for i in range(len(x.index))}
cplayers  = {str(i): 1 if (x.iloc[i]['Position'] == 'C')  else 0 for i in range(len(x.index))}
fbplayers = {str(i): 1 if (x.iloc[i]['Position'] == '1B') else 0 for i in range(len(x.index))}
ssplayers = {str(i): 1 if (x.iloc[i]['Position'] == 'SS') else 0 for i in range(len(x.index))}
cost = {str(i): x.iloc[i]['Salary'] for i in range(len(x.index))}
pts  = {str(i): x.iloc[i]['Score']  for i in range(len(x.index))}

model = LpProblem('Fantasy Baseball', LpMaximize)

player_var = LpVariable.dicts('Players',playernum,0,1,LpBinary)

model += lpSum([pts[i]*player_var[i] for i in playernum]),'TotalScore'

model += lpSum([cost[i]*player_var[i] for i in playernum]) <= 35000
model += lpSum([sbplayers[i]*player_var[i] for i in playernum]) <= 2
model += lpSum([sbplayers[i]*player_var[i] for i in playernum]) >= 1
model += lpSum([ofplayers[i]*player_var[i] for i in playernum]) <= 4
model += lpSum([ofplayers[i]*player_var[i] for i in playernum]) >= 3
model += lpSum([tbplayers[i]*player_var[i] for i in playernum]) <= 2
model += lpSum([tbplayers[i]*player_var[i] for i in playernum]) >= 1
model += lpSum([pplayers[i]*player_var[i] for i in playernum]) == 1
model += lpSum( [fbplayers[i]*player_var[i] for i in playernum]) <= 2
#model += lpSum( [fbplayers[i]*player_var[i] for i in playernum]) >= 1
model += lpSum( [ssplayers[i]*player_var[i] for i in playernum]) <= 2
model += lpSum( [ssplayers[i]*player_var[i] for i in playernum]) >= 1
model += lpSum( [cplayers[i]*player_var[i] for i in playernum]) <= 2
#model += lpSum( [cplayers[i]*player_var[i] for i in playernum]) >= 1
model += lpSum([player_var[i] for i in playernum]) <= 9

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
	totalpoints += each[2]
	totalcost += each[3]
	totalfant += each[4]

lineup.append(['Total','',totalpoints,totalcost,totalfant])
titles = ['Pos','Name','Score','Price','Projection']

print(tabulate(lineup,headers = titles))

