#! FanDuel NBA Comp

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

#https://www.basketball-reference.com/leagues/NBA_2019_ratings.html
#https://www.basketball-reference.com/leagues/NBA_2019_per_game.html

logging.debug('Start of Program')

road = 'C:\\Users\\ngoodroe\\Desktop'
#road = r'/Users/goodroe/Dropbox/Python/Pandas'

#Teams according to FanDuel


percent = .8

teams = []

if os.getcwd() != road:
	os.chdir(road)
	logging.debug('File Path Fixed')

positions = ['PG','SG','SF','PF','C']

logging.debug('New dataframe')

fd = pd.read_csv('FanDuel-NBA-2019-03-15-33531-players-list.csv')
fd = fd.set_index('Nickname')
fd.index.names = ['Name']

teams = list(fd.Team)
teams = list(set(teams))

p = pd.read_csv('NBAp.csv')
loc = p.Player.str.find('\\')
p['temp'] = p.Player.str.split('\\')
p['Name'] = p['temp'].str[0]
p = p.drop(columns = ['temp'])
p = p.set_index('Name')
p = p.drop(columns = ['Rk'])

for each_fd in range(len(fd.index)):
	for each_p in range(len(p.index)):
		if fd.index[each_fd] == p.index[each_p]:
			continue
		elif fd.index[each_fd] in p.index[each_p]:
			logging.debug('Changed '+fd.index[each_fd]+' to '+p.index[each_p])
			fd = fd.rename(index = {fd.index[each_fd]:p.index[each_p]})
			continue
		elif p.index[each_p] in fd.index[each_fd]:
			logging.debug('Changed '+p.index[each_p]+' to '+fd.index[each_fd])
			p = p.rename(index = {p.index[each_p]:fd.index[each_fd]})


df = pd.concat([fd,p],axis=1
               #,sort = True
               )



df = df[df['Injury Indicator'] != 'O']

### MANUAL TAKEOUT
#df = df[df.index != 'Kawhi Leonard']
df = df[df.index != 'Justin Holiday']

###

pg = df[df.Position == 'PG']
pg = pg.query('Team in @teams')
pg_sal = pg[['Salary','FPPG','Position']]
pg = pg[['3P','AST','BLK','FG','FT','TRB','STL','TOV']]
#pg_n = pg
pg_n = (pg-pg.min())/(pg.max()-pg.min())

sg = df[df.Position == 'SG']
sg = sg.query('Team in @teams')
sg_sal = sg[['Salary','FPPG','Position']]
sg = sg[['3P','AST','BLK','FG','FT','TRB','STL','TOV']]
#sg_n = sg
sg_n = (sg-sg.min())/(sg.max()-sg.min())

sf = df[df.Position == 'SF']
sf = sf.query('Team in @teams')
sf_sal = sf[['Salary','FPPG','Position']]
sf = sf[['3P','AST','BLK','FG','FT','TRB','STL','TOV']]
#sf_n = sf
sf_n = (sf-sf.min())/(sf.max()-sf.min())

pf = df[df.Position == 'PF']
pf = pf.query('Team in @teams')
pf_sal = pf[['Salary','FPPG','Position']]
pf = pf[['3P','AST','BLK','FG','FT','TRB','STL','TOV']]
#pf_n = pf
pf_n = (pf-pf.min())/(pf.max()-pf.min())

c  = df[df.Position == 'C' ]
c = c.query('Team in @teams')
c_sal = c[['Salary','FPPG','Position']]
c  = c[['3P','AST','BLK','FG','FT','TRB','STL','TOV']]
#c_n = c
c_n = (c-c.min())/(c.max()-c.min())


'''
3p shot 	=	1		'3P'
assist		=	1.5		'AST'
block		=	3		'BLK'
fieldgoal	=	2		'FG'
freethrow	=	1		'FT'
rebound		=	1.2		'TRB'
steal		=	3		'STL'
turnover	=	-1		'TOV'


# header = ['PG,','Points','SG','Points','SF','Points','PF','Points','C','Points']

norm_dfs = [pg_n, sg_n, sf_n, pf_n, c_n]
for each in norm_dfs:
	each['AST'] = each['AST'] * 1.5
	each['BLK'] = each['BLK'] * 3
	each['FG' ] = each['FG' ] * 2
	each['TRB'] = each['TRB'] * 1.2
	each['STL'] = each['STL'] * 3
	each['TOV'] = each['TOV'] * -1
	each['Score'] = each[['3P','AST','BLK','FG','FT','TRB','STL','TOV']].sum(axis=1)
	each = each.sort_values('Score', ascending = False)


Pos      3Pointers    Assists    Blocks    FieldGoal    FreeThrow    Rebounds    Steals    Turnovers
-----  -----------  ---------  --------  -----------  -----------  ----------  --------  -----------
PG         5.64148    26.46     3.32905      36.2546      8.04167     15.5838  11.4247      -6.73522
SG         7.12208    15.1501   4.92536      39.3801      8.0544      19.6312  11.6312      -5.89443
SF         6.01991    11.7736   5.96758      35.7771      7.25658     25.1558  13.4891      -5.43966
PF         4.88173    11.2167   8.89669      33.8848      6.8192      29.1677  10.6989      -5.56571
C          1.45881    10.0923  12.1403       30.9866      8.42177     34.8358   7.50161     -5.43725
'''

pg_n['3P']  = pg_n['3P' ] * 4.99
pg_n['AST'] = pg_n['AST'] * 27.17
pg_n['BLK'] = pg_n['BLK'] * 3.80
pg_n['FG' ] = pg_n['FG' ] * 34.29
pg_n['FT' ] = pg_n['FT' ] * 6.97
pg_n['TRB'] = pg_n['TRB'] * 16.64
pg_n['STL'] = pg_n['STL'] * 13.27
pg_n['TOV'] = pg_n['TOV'] * -7.16
pg_n['Score'] = pg_n[['3P','AST','BLK','FG','FT','TRB','STL','TOV']].sum(axis=1)
pg_n = pg_n.sort_values('Score', ascending = False)

sg_n['3P' ] = sg_n['3P' ] * 7.67
sg_n['AST'] = sg_n['AST'] * 15.44
sg_n['BLK'] = sg_n['BLK'] * 5.05
sg_n['FG' ] = sg_n['FG' ] * 39.09
sg_n['FT' ] = sg_n['FT' ] * 7.01
sg_n['TRB'] = sg_n['TRB'] * 20.07
sg_n['STL'] = sg_n['STL'] * 11.63
sg_n['TOV'] = sg_n['TOV'] * -5.99
sg_n['Score'] = sg_n[['3P','AST','BLK','FG','FT','TRB','STL','TOV']].sum(axis=1)
sg_n = sg_n.sort_values('Score', ascending = False)

sf_n['3P' ] = sf_n['3P' ] * 6.30
sf_n['AST'] = sf_n['AST'] * 11.34
sf_n['BLK'] = sf_n['BLK'] * 5.96
sf_n['FG' ] = sf_n['FG' ] * 36.00
sf_n['FT' ] = sf_n['FT' ] * 6.95
sf_n['TRB'] = sf_n['TRB'] * 25.77
sf_n['STL'] = sf_n['STL'] * 13.09
sf_n['TOV'] = sf_n['TOV'] * -5.44
sf_n['Score'] = sf_n[['3P','AST','BLK','FG','FT','TRB','STL','TOV']].sum(axis=1)
sf_n = sf_n.sort_values('Score', ascending = False)


pf_n['3P' ] = pf_n['3P' ] * 5.20
pf_n['AST'] = pf_n['AST'] * 10.90
pf_n['BLK'] = pf_n['BLK'] * 8.20
pf_n['FG' ] = pf_n['FG' ] * 34.37
pf_n['FT' ] = pf_n['FT' ] * 7.09
pf_n['TRB'] = pf_n['TRB'] * 30.73
pf_n['STL'] = pf_n['STL'] * 9.09
pf_n['TOV'] = pf_n['TOV'] * -5.61
pf_n['Score'] = pf_n[['3P','AST','BLK','FG','FT','TRB','STL','TOV']].sum(axis=1)
pf_n = pf_n.sort_values('Score', ascending = False)

'C          1.45881    10.0923  12.1403       30.9866      8.42177     34.8358   7.50161     -5.43725'
c_n['3P' ] = c_n['3P' ] * 1.74
c_n['AST'] = c_n['AST'] * 9.87
c_n['BLK'] = c_n['BLK'] * 12.73
c_n['FG' ] = c_n['FG' ] * 32.03
c_n['FT' ] = c_n['FT' ] * 7.09
c_n['TRB'] = c_n['TRB'] * 34.11
c_n['STL'] = c_n['STL'] * 7.70
c_n['TOV'] = c_n['TOV'] * -5.29
c_n['Score'] = c_n[['3P','AST','BLK','FG','FT','TRB','STL','TOV']].sum(axis=1)
c_n = c_n.sort_values('Score', ascending = False)

logging.debug('Almost Done!')

pg_ns = pd.concat([pg_n,pg_sal],axis=1)#, sort=False)
sg_ns = pd.concat([sg_n,sg_sal],axis=1)#, sort=False)
sf_ns = pd.concat([sf_n,sf_sal],axis=1)#, sort=False)
pf_ns = pd.concat([pf_n,pf_sal],axis=1)#, sort=False)
c_ns  = pd.concat([c_n,c_sal]  ,axis=1)#, sort=False)

player_df = pd.concat([pg_ns,sg_ns,sf_ns,pf_ns,c_ns], axis=0)#, sort=False)

logging.debug('Stop for secondary df')

players = []
for total in range(len(player_df)):
	players.append([player_df.iloc[total]['Position'],
					player_df.index[total],
					player_df.iloc[total].Score,
					player_df.iloc[total].Salary,
					player_df.iloc[total].FPPG])

playernum = [str(i) for i in range(len(player_df.index))]
pgplayers = {str(i): 1 if (player_df.iloc[i]['Position'] == 'PG') else 0 for i in range(len(player_df.index))}
sgplayers = {str(i): 1 if (player_df.iloc[i]['Position'] == 'SG') else 0 for i in range(len(player_df.index))}
sfplayers = {str(i): 1 if (player_df.iloc[i]['Position'] == 'SF') else 0 for i in range(len(player_df.index))}
pfplayers = {str(i): 1 if (player_df.iloc[i]['Position'] == 'PF') else 0 for i in range(len(player_df.index))}
cplayers  = {str(i): 1 if (player_df.iloc[i]['Position'] == 'C' ) else 0 for i in range(len(player_df.index))}
cost = {str(i): player_df.iloc[i]['Salary'] for i in range(len(player_df.index))}
pts  = {str(i): player_df.iloc[i]['Score']  for i in range(len(player_df.index))}


model = LpProblem('Fantasy Basketball', LpMaximize)

player_var = LpVariable.dicts('Players',playernum,0,1,LpBinary)

model += lpSum([pts[i]*player_var[i] for i in playernum]),'TotalScore'

model += lpSum([cost[i]*player_var[i] for i in playernum]) <= 60000
model += lpSum([pgplayers[i]*player_var[i] for i in playernum]) <= 2
model += lpSum([sgplayers[i]*player_var[i] for i in playernum]) <= 2
model += lpSum([sfplayers[i]*player_var[i] for i in playernum]) <= 2
model += lpSum([pfplayers[i]*player_var[i] for i in playernum]) <= 2
model += lpSum( [cplayers[i]*player_var[i] for i in playernum]) <= 1

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
titles = ['Pos','Name','Score','Price','FPPG']

print(tabulate(lineup,headers = titles))

'''

pg_ns = pg_ns[pg_ns.Score > pg_ns.Score.quantile(percent)]
sg_ns = sg_ns[sg_ns.Score > sg_ns.Score.quantile(percent)]
sf_ns = sf_ns[sf_ns.Score > sf_ns.Score.quantile(percent)]
pf_ns = pf_ns[pf_ns.Score > pf_ns.Score.quantile(percent)]
c_ns  = c_ns[c_ns.Score   >  c_ns.Score.quantile(percent)]


pgplayers = []
sgplayers = []
sfplayers = []
pfplayers = []
cplayers  = []



#0 = Position, 1 = Name, 2 = Score, 3 = Salary

for total in range(len(pg_ns)):
	pgplayers.append(['PG',pg_ns.index[total],
                          pg_ns.iloc[total].Score,pg_ns.iloc[total].Salary,
                          pg_ns.iloc[total].FPPG])

for total in range(len(sg_ns)):
	sgplayers.append(['SG',sg_ns.index[total],
                          sg_ns.iloc[total].Score,sg_ns.iloc[total].Salary,
                          sg_ns.iloc[total].FPPG])

for total in range(len(sf_ns)):
	sfplayers.append(['SF',sf_ns.index[total],
                          sf_ns.iloc[total].Score,sf_ns.iloc[total].Salary,
                          sf_ns.iloc[total].FPPG])

for total in range(len(pf_ns)):
	pfplayers.append(['PF',pf_ns.index[total],
                          pf_ns.iloc[total].Score,pf_ns.iloc[total].Salary,
                          pf_ns.iloc[total].FPPG])

for total in range(len(c_ns)):
	cplayers.append(['C',c_ns.index[total],c_ns.iloc[total].Score,
                         c_ns.iloc[total].Salary,c_ns.iloc[total].FPPG])


'''
