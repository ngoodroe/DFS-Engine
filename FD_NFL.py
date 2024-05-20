#! FanDuel NBA Comp

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

#https://www.basketball-reference.com/leagues/NBA_2019_ratings.html
#https://www.basketball-reference.com/leagues/NBA_2019_per_game.html

logging.debug('Start of Program')

# road = 'C:\\Users\\ngoodroe\\Desktop'
road = r'/Users/goodroe/Dropbox/Python/Pandas'

#Teams according to FanDuel


percent = .5

teams = []

if os.getcwd() != road:
	os.chdir(road)
	logging.debug('File Path Fixed')



logging.debug('New dataframe')

fd = pd.read_csv('FD_NFL_P.csv')
fd = fd.set_index('Nickname')
fd.index.names = ['Name']

teams = list(fd.Team)
teams = list(set(teams))

# p = pd.read_csv('NBAp.csv')
# loc = p.Player.str.find('\\')
# p['temp'] = p.Player.str.split('\\')
# p['Name'] = p['temp'].str[0]
# p = p.drop(columns = ['temp'])
# p = p.set_index('Name')
# p = p.drop(columns = ['Rk'])

# for each_fd in range(len(fd.index)):
# 	for each_p in range(len(p.index)):
# 		if fd.index[each_fd] == p.index[each_p]:
# 			continue
# 		elif fd.index[each_fd] in p.index[each_p]:
# 			logging.debug('Changed '+fd.index[each_fd]+' to '+p.index[each_p])
# 			fd = fd.rename(index = {fd.index[each_fd]:p.index[each_p]})
# 			continue
# 		elif p.index[each_p] in fd.index[each_fd]:
# 			logging.debug('Changed '+p.index[each_p]+' to '+fd.index[each_fd])
# 			p = p.rename(index = {p.index[each_p]:fd.index[each_fd]})


# df = pd.concat([fd,p],axis=1, sort = True)

df = fd

df = df[df['Injury Indicator'] != 'O']

### MANUAL TAKEOUT
# df = df[df.index != 'Kawhi Leonard']
# df = df[df.index != 'Rudy Gay']

###

players = []
for total in range(len(df)):
	players.append([df.iloc[total]['Position'],
					df.index[total],
					df.iloc[total].Salary,
					df.iloc[total].FPPG])

playernum = [str(i) for i in range(len(df.index))]
qbplayers = {str(i): 1 if (df.iloc[i]['Position'] == 'QB') else 0 for i in range(len(df.index))}
rbplayers = {str(i): 1 if (df.iloc[i]['Position'] == 'RB') else 0 for i in range(len(df.index))}
wrplayers = {str(i): 1 if (df.iloc[i]['Position'] == 'WB') else 0 for i in range(len(df.index))}
teplayers = {str(i): 1 if (df.iloc[i]['Position'] == 'TE') else 0 for i in range(len(df.index))}
defplayers = {str(i): 1 if (df.iloc[i]['Position'] == 'D') else 0 for i in range(len(df.index))}
cost = {str(i): df.iloc[i]['Salary'] for i in range(len(df.index))}
pts  = {str(i): df.iloc[i]['FPPG']  for i in range(len(df.index))}


model = LpProblem('Fantasy Football', LpMaximize)

player_var = LpVariable.dicts('Players',playernum,0,1,LpBinary)

model += lpSum([pts[i]*player_var[i] for i in playernum]),'TotalScore'


model += lpSum([cost[i]*player_var[i] for i in playernum]) <= 60000
model += lpSum([qbplayers[i]*player_var[i] for i in playernum]) == 1
model += lpSum([rbplayers[i]*player_var[i] for i in playernum]) <= 3
model += lpSum([wrplayers[i]*player_var[i] for i in playernum]) <= 4
model += lpSum([teplayers[i]*player_var[i] for i in playernum]) == 1
model += lpSum([defplayers[i]*player_var[i] for i in playernum]) == 1
model += lpSum([player_var[i] for i in playernum]) == 9

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
titles = ['Pos','Name','Price','FPPG']

print(tabulate(lineup,headers = titles))

# qbs = []
# rbs = []
# wrs = []
# tes = []
# flexs = []
# ds = []

# qb = df[df.Position == 'QB']
# rb = df[df.Position == 'RB']
# wr = df[df.Position == 'WR']
# te = df[df.Position == 'TE']
# flex = df[(df.Position == 'RB') | (df.Position == 'WR')]
# d = df[df.Position == 'D']


# for total in range(len(qb)):
# 	qbs.append(['QB',qb.index[total],qb.iloc[total].FPPG,
#                          qb.iloc[total].Salary])

# for total in range(len(rb)):
# 	rbs.append(['RB',rb.index[total],rb.iloc[total].FPPG,
#                          rb.iloc[total].Salary])
# for total in range(len(wr)):
# 	wrs.append(['WR',wr.index[total],wr.iloc[total].FPPG,
#                          wr.iloc[total].Salary])

# for total in range(len(te)):
# 	tes.append(['TE',te.index[total],te.iloc[total].FPPG,
#                          te.iloc[total].Salary])

# for total in range(len(flex)):
# 	flexs.append(['FLEX',flex.index[total],flex.iloc[total].FPPG,
#                          flex.iloc[total].Salary])
# for total in range(len(d)):
# 	ds.append(['DEF',d.index[total],d.iloc[total].FPPG,
#                          d.iloc[total].Salary])


# max_score = 0
# delta_score = 0
# fppg = 0
# total_price = 0
# new_score = 0
# best_lineup = []


# '''
# 1 QB
# 2 RB
# 3 WR?
# 1 TE
# 1 FLEX
# 1 DEF

# $60,000

# Matchup


# for a in range(len(qbs)):

# for b in range(len(rbs)-1):
# 	for c in range(b+1,len(rbs)):
# 		for d in range(len(wrs)-1):
# 			for e in range(d+1,len(wrs)):
# 				for g in range(len(flexs)):
# 					if (flexes[g] == rb[b] | flexes[g] == rb[c] | flexes[g] == wr[c]):
# 						continue
# 					for f in range(len(tes)):
# 						for h in range(len(ds)):







