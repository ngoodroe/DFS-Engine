# Reb+As
import random
points = []
reb = []
ass = []
loop = 'y'
target=1

while True:
    target = input('\nWhat is the target number (press n to close) \t')
    if target == 'n':
        break
    target = float(target)
    #while len(points)!=5:
    #    points = [int(x)
    #             for x in input('write five numbers points \t').split()]
    while len(reb)!=5:
        reb = [int(x)
                 for x in input('write five numbers rebounds \t').split()]
    while len(ass)!=5:
        ass = [int(x)
                 for x in input('write five numbers assists \t').split()]


    over=0
    under=0
    for x in range(1000):
        #score = random.choice(points)+random.choice(reb)+random.choice(ass)

        score = random.choice(reb)+random.choice(ass)
        if score> target:
                over+=1
        elif score< target:
                under+=1

    uratio = under/1000
    oratio = over/1000

    print(f'He hits the under {uratio} percent of the time \n and the over {oratio} percent of the time')
    points = []
    reb = []
    ass = []

'''
import requests as re
from bs4 import BeautifulSoup

url = ''
r = re.get(url)
busu = BeautifulSoup(r.text,'html.parser')


last5 = busu.find_all('table')[0]

for x in last5.find_all('tr')[1:]:
	print(int(x.find_all('td')[17].text)) #Total Rebounds
	print(int(x.find_all('td')[18].text)) #Assists

'''


