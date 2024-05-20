#! FanDuel 3pt Comp

import pandas as pd
import os
import matplotlib.pyplot as plt
from tabulate import tabulate
from pprint import pprint
import time

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

positions = ['PG','SG','SF','PF','C']

logging.debug('New dataframe')

#Edit which csv
fd = pd.read_csv('FanDuel-NBA-2019-02-04-32557-players-list.csv')
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


df = pd.concat([fd,p],axis=1, sort = True)
df['TP'] = df['3P']
df['TPP'] = df['3P%']

df = df.query('Team in @teams')
df = df[df['Injury Indicator'] != 'O' ]
df = df[df['TP'] > 0 ]

##df = df[df.index != 'Eric Gordon']
##df = df[df.index != 'Goran Dragic']


df1 = df[df.Tier == 'T1']
df2 = df[df.Tier == 'T2']
df3 = df[df.Tier == 'T3']

## Creating the three point normalized (tpn) dataframes

tpn1 = df1[['G','GS','MP','TP','3PA','TPP']]
#tpn1 = (tpn1 - tpn1.min())/(tpn1.max() - tpn1.min() )

tpn2 = df2[['G','GS','MP','TP','3PA','TPP']]
#tpn2 = (tpn2 - tpn2.min())/(tpn2.max() - tpn2.min() )

tpn3 = df3[['G','GS','MP','TP','3PA','TPP']]
#tpn3 = (tpn3 - tpn3.min())/(tpn3.max() - tpn3.min() )



#tpn1 = tpn1[(tpn1['MP'] > .25) & (tpn1['TP'] >.25)]
#tpn1['Score'] = tpn1['3PA']+(2*tpn1.TP)
tpn1 = tpn1.sort_values('3PA', ascending = False)

#tpn2 = tpn2[(tpn2['MP'] > .25) & (tpn2['TP'] >.25)]
#tpn2['Score'] = tpn2['3PA']+(2*tpn2.TP)
tpn2 = tpn2.sort_values('3PA', ascending = False)

#tpn3 = tpn3[(tpn3['MP'] > .25) & (tpn3['TP'] >.25)]
#tpn3['Score'] = tpn3['3PA']+(tpn3.TP*2)
tpn3 = tpn3.sort_values('3PA', ascending = False)

final = [[tpn1.index[0],tpn2.index[0],tpn3.index[0]]]

print('\n'*3)
print(tabulate(final, headers = ['Player1','Player2','Player3 (2x)']))
print('\n'*3)

# df = pd.read_csv('NBAp.csv')
# df['Name'] = df.Player.str[:-10]
# df = df.set_index('Name')
# df = df.drop(columns = ['Rk'])

# c = df.columns.values




