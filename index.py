import sys
import os
import csv

battersScoring = {
    'R': 1,
    'TB': 1,
    'RBI': 1,
    'BB': 1,
    'SO': -1,
    'SB': 1,
}

pitchersScoring = {
    'IP': 3,
    'H': -1,
    'ER': -2,
    'BB': -1,
    'SO': 1,
    'W': 5,
    'L': -5,
    'SV': 5,
    'HLD': 3
}

players = {}
playersName = []
playersTotal = {}

def main():
  year = sys.argv[1]
  print('Finding projections for year: ' + year)
  dir_list = os.listdir(year)
  print(dir_list)
  for dir in dir_list:
    file = year + '/' + dir
    print('Reading file: ' + file)
    with open(file, mode='r') as csvfile:
        csvFile = csv.reader(csvfile)
        next(csvFile)
        if file.find('CBS') >= 0:
            if file.find('Batters') >=0:
                cbs(csvFile, 'batter')
            else:
                cbs(csvFile, 'pitcher')  
        elif file.find('Fangraphs') >= 0:
            if file.find('Batters') >=0:
                fangraphs(csvFile, 'batter')
            else:
                fangraphs(csvFile, 'pitcher')
        elif file.find('FantasyPros') >= 0:
            if file.find('Batters') >=0:
                fantasypros(csvFile, 'batter')
            else:
                fantasypros(csvFile, 'pitcher')
        elif file.find('Razzball') >= 0:
            if file.find('Batters') >=0:
                razzball(csvFile, 'batter')
            else:
                razzball(csvFile, 'pitcher')

def writer():
    with open('output.csv', 'w') as csvfile:
        reader =csv.writer(csvfile)
        reader.writerow(('Player', 'FP'))
        for value,item in playersTotal.items():
            reader.writerow((value,item))

def getRawValue(value):
    return int(round(float(value)))

def iterate(file, mapping, position):
    scoring = {}
    if position == 'batter':
        scoring = battersScoring
    else:
        scoring = pitchersScoring
    
    for lines in file:
        scores = {}
        if position == 'batter':
            if 'SB' in mapping:
                scores['SB'] = getRawValue(lines[mapping['SB']])*getRawValue(scoring['SB'])
            scores['R'] = getRawValue(lines[mapping['R']]*getRawValue(scoring['R']))
            scores['TB'] = getRawValue(lines[mapping['1B']])*getRawValue(scoring['TB']) + (getRawValue(lines[mapping['2B']])*2)*getRawValue(scoring['TB']) + (getRawValue(lines[mapping['3B']])*3)*getRawValue(scoring['TB']) + (getRawValue(lines[mapping['HR']])*4)*getRawValue(scoring['TB'])
            scores['RBI'] = getRawValue(lines[mapping['RBI']])*getRawValue(scoring['RBI'])
            scores['BB'] = getRawValue(lines[mapping['BB']])*getRawValue(scoring['BB'])
            scores['SO'] = getRawValue(lines[mapping['SO']])*getRawValue(scoring['SO'])
        addPlayerScores(lines[mapping['Player']], scores)

def addPlayerScores(player, scores):
    if player.strip() in players.keys():
        if player.strip() == 'Lane Thomas':
            print(players[player.strip()])
            print(scores)
        for score in scores:
            if score in players[player.strip()].keys():
                players[player.strip()][score] = int(((int(players[player.strip()][score]) + int(scores[score])) / 2))
            else:
                players[player.strip()][score] = int(scores[score])
    else:
        players[player.strip()] = {}
        playersName.append(player.strip())
        for score in scores:
            players[player.strip()][score] = int(scores[score])

def getPlayerTotal():
    for player in players:
        playersTotal[player] = 0
        for score in players[player]:
            playersTotal[player] += int(players[player][score])



def cbs(file, position):
    print('Reading CBS: ' + position)
    if position == 'batter':
        cbsBatters = {
            'Full': 0,
            'Player': 1,
            'Position': 2,
            'Team': 3,
            'GP': 4,
            'R': 5,
            '1B': 6,
            '2B': 7,
            '3B': 8,
            'HR': 9,
            'RBI': 10,
            'OBP': 11,
            'BB': 12,
            'SO': 13,
            'TB': 14,
            'SB': 15
        }
        iterate(file, cbsBatters, position)
        


def fangraphs(file, position):
    print('Reading Fangraphs: ' + position)
    if position == 'batter':
        fangraphsBatters = {
            '#': 0,
            'Player': 1,
            'Team': 2,
            'G': 3,
            '1B': 4,
            '2B': 5,
            '3B': 6,
            'HR': 7,
            'R': 8,
            'RBI': 9,
            'BB': 10,
            'SO': 11
        }
        iterate(file, fangraphsBatters, position)

def razzball(file, position):
    print('Reading Razzball: ' + position)
    if position == 'batter':
        razzballBatters = {
            'Player': 0,
            'Team': 1,
            'Bats': 2,
            'ESPN': 3,
            'YAHOO': 4,
            'G': 5,
            'R': 6,
            'HR': 7,
            'RBI': 8,
            'SB': 9,
            '1B': 10,
            '2B': 11,
            '3B': 12,
            'TB': 13,
            'SO': 14,
            'BB': 15,
            'OBP': 16
        }
        iterate(file, razzballBatters, position)

def fantasypros(file, position):
    print('Reading Fantasypros: ' + position)
    if position == 'batter':
        fantasyprosBatters = {
            'Player': 0,
            'Team': 1,
            'Positions': 2,
            'R': 3,
            'HR': 4,
            'RBI': 5,
            'SB': 6,
            'OBP': 7,
            'H': 8,
            '1B': 9,
            '2B': 10,
            '3B': 11,
            'BB': 12,
            'SO': 13
        }
        iterate(file, fantasyprosBatters, position)



main()
getPlayerTotal()
writer()
print(playersTotal)