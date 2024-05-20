#!NBA FanDuel 2.0
'''
This is the second incarnation of the python engine for predicting successful FanDuel match-ups

'''
import pandas as pd
import os
import matplotlib.pyplot as plt
from tabulate import tabulate
from pprint import pprint
import time
from pulp import *
import webbrowser

import logging
logging.basicConfig(level=logging.DEBUG,
			 format=' %(asctime)s - %(levelname)s- %(message)s')

logging.debug('Start of Program')

# road = 'C:\\Users\\ngoodroe\\Desktop'
#road = r'/Users/goodroe/Dropbox/Python/Pandas'


teamName = {
'Hawks' : 'ATL',
'Celtics' : 'BOS',
'Nets' : 'BKN',
'Hornets' : 'CHA',
'Bulls' : 'CHI',
'Cavaliers' : 'CLE',
'Mavericks' : 'DAL',
'Nuggets' : 'DEN',
'Pistons' : 'DET',
'Warriors' : 'GS',
'Rockets' : 'HOU',
'Pacers' : 'IND',
'Clippers' : 'LAC',
'Lakers' : 'LAL',
'Grizzlies' : 'MEM',
'Heat' : 'MIA',
'Bucks' : 'MIL',
'Timberwolves' : 'MIN',
'Pelicans' : 'NO',
'Knicks' : 'NY',
'Thunder' : 'OKC',
'Magic' : 'ORL',
'76ers' : 'PHI',
'Suns' : 'PHO',
'Blazers' : 'POR',
'Kings' : 'SAC',
'Spurs' : 'SA',
'Raptors' : 'TOT',
'Jazz' : 'UTA',
'Wizards' : 'WAS',
'GSW': 'GS','BRK':'BKN','NYK':'NY','NOP':'NO'}




'''
Sport Ref teams = ['ATL', 'BOS', 'BRK', 'CHI', 'CHO',
 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 
 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 
 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 
 'SAS', 'TOR', 'TOT', 'UTA', 'WAS']

FanDuel teams = ['ATL', 'BOS', 'BKN', 'CHI', 'CHO',
 'CLE', 'DAL', 'DEN', 'DET', 'GS', 'HOU', 'IND', 
 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NO', 
 'NY', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 
 'SAS', 'TOR', 'TOT', 'UTA', 'WAS']

 Differences:
 GSW -> GS
 BRK -> BKN
 NYK -> NY
 NOP -> NO


### Settle discrepancies between FD and
 SR team abbreviations   

Defer to FD

Split the string of team name and get the last one.
Map it to these

'''
#d = pd.read_csv('NBA_D.csv')


#d['newName'] = teamName[d['Team']]


fd = pd.read_csv('FanDuel-NBA-2021 ET-03 ET-28 ET-56192-players-list.csv')
##for each in range(len(fd.index)):
##        fd.loc[each,'Name'] = ''.join(fd.loc[each].Nickname.split('.'))

fd = fd.set_index('Nickname')
#fd.index.names = ['Name']

##p = pd.read_csv('NBAp.csv')
##loc = p.Player.str.find('\\')
##p['temp'] = p.Player.str.split('\\')
##p['Name2'] = p['temp'].str[0]
##p = p.drop(columns = ['temp'])
##for each in range(len(p.index)):
##        p.loc[each, 'Name'] = ''.join(p.loc[each].Name2.split('.'))
##
##p = p.set_index('Name')
##p = p.drop(columns = ['Rk'])


##for each_fd in range(len(fd.index)):
##	for each_p in range(len(p.index)):
##		if fd.index[each_fd] == p.index[each_p]:
##			continue
##		elif fd.index[each_fd] in p.index[each_p]:
##			logging.debug('Changed '+fd.index[each_fd]+' to '+p.index[each_p])
##			fd = fd.rename(index = {fd.index[each_fd]:p.index[each_p]})
##			continue
##		elif p.index[each_p] in fd.index[each_fd]:
##			logging.debug('Changed '+p.index[each_p]+' to '+fd.index[each_fd])
##			p = p.rename(index = {p.index[each_p]:fd.index[each_fd]})
##
#Fix names like J.J. into JJ
# ''.join(name.split('.'))


n = pd.read_csv('numfire.csv')
namelist = []
for x in range(len(n)):
	z = n.iloc[x]['name'].split(' ')[:2]
	namelist.append( z[0]+' '+z[1])

n['Nickname'] = namelist
n = n.set_index('Nickname')
fd = pd.concat([fd,n], axis=1, sort=True)

#df = pd.concat([fd,p],axis=1
               #, sort = True
                #)
df = fd


##teams = list(fd.Team)
##teams = list(set(teams))
##
##df = df.query('Team in @teams')
##
##d['temp'] = d.Team.str.split(' ')
##d['Name'] = d['temp'].str[-1]
##d['temp'] = d['Name'].str.split('*')
##d['Name'] = d['temp'].str[0]
##for x in range(len(d.index)):
##	d.loc[x,'Abrv'] = teamName[d.iloc[x].Name] #Change columns to their abreviations
##d = d.set_index('Abrv')
##	
##for x in df.index:
##	df.loc[x,'OppPts'] = d.loc[df.loc[x].Opponent].PTS
##
##
##df = df[df.MP > 1]
df['FPPG'] = df['FPPG']+1
df['proj']=df['proj'].fillna(0)
df['Score'] = (df['FPPG'] * df['Salary'] * df['proj'] * df['proj'])**(1/4)
#df['nScore'] = (df['Score']-df['Score'].min())/(df['Score'].max()-df['Score'].min())
#df['Score'] = df['proj']
#df['Score'] = 3* (20 ** df.nScore)



df = df.sort_values('Position', axis=0)

df = df[df['Injury Indicator'] != 'O']

##GTD = input('Do you want to exclude Game-Time-Desicion players?')
##if GTD == 'y':
#df = df[df['Injury Indicator'] != 'GTD']

        
df = df[df.Score.notnull()]
df = df[df.Id.notnull()]

### MANUAL TAKEOUT
#df = df[df.index != 'Anthony Davis']
#df = df[df.index != 'Derrick Rose']
player_df = df

# Get list of teams from both FD and TeamD and match them up

# Combine both player csv into one.
# Eliminate any nonplaying players (hurt or wrong team)
# Columns needed: MP, 3PA, and FPPG
# New column with opponent's 3pt% and pts allowed 

''' Calculate each player's score using
 geometric mean with the following qualities:
	*3pt = Opp 3p%, Minutes Played, and 3PA
	*Full Roster = MP, Opponent Points Allowed, and FPPG

 '''

# if threepoint == y:
# 	#CODE
# else:
# 	#CODE


# breakup the dataframe by position.

# Normalize Data

players = []
for total in range(len(player_df)):
	players.append([player_df.iloc[total]['Position'],
					player_df.index[total],
					player_df.iloc[total].Score,
					player_df.iloc[total].Salary,
					player_df.iloc[total].FPPG,
                                        player_df.iloc[total].proj])


# Linear Programming to find largest score for a team

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

model += lpSum([cost[i]*player_var[i] for i in playernum]) <=  60000
model += lpSum([pgplayers[i]*player_var[i] for i in playernum]) == 2
model += lpSum([sgplayers[i]*player_var[i] for i in playernum]) == 2
model += lpSum([sfplayers[i]*player_var[i] for i in playernum]) == 2
model += lpSum([pfplayers[i]*player_var[i] for i in playernum]) == 2
model += lpSum( [cplayers[i]*player_var[i] for i in playernum]) == 1
model += lpSum([player_var[i] for i in playernum]) == 9


status = model.solve()
LpStatus[model.status]

best = []
lineup = []
totalcost = 0
totalfant = 0
totalpoints = 0
totalproj = 0

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
	totalproj += each[5]
	

lineup.append(['Total','',totalpoints,totalcost,totalfant,totalproj])
titles = ['Pos','Name','Score','Price','FPPG','Projected']

print(tabulate(lineup,headers = titles))

# Print out the answers

#x = input('What is the last position you need?\n').upper()
#print('\n')
#print(df[(df.Pos == x)&(df.Salary ==3500)].Score.nlargest(6))

