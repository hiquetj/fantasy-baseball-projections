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

def totalWriter():
    with open('output.csv', 'w') as csvfile:
        reader =csv.writer(csvfile)
        reader.writerow(('Player', 'FP'))
        for value,item in playersTotal.items():
            reader.writerow((value,item))

def detailBatterWriter():
    with open('output_detail_batter.csv', 'w') as csvfile:
        reader =csv.writer(csvfile)
        reader.writerow(('Player', 'BB', 'R', 'SO', 'RBI', 'SB', 'TB', 'Total', 'OBP'))
        for value,item in players.items():
            if 'SB' in item:
                reader.writerow((value,item['BB'],item['R'],item['SO'],item['RBI'],item['SB'],item['TB'],item['total'],item['OBP']))

def detailPitcherWriter():
    with open('output_detail_pitcher.csv', 'w') as csvfile:
        reader =csv.writer(csvfile)
        reader.writerow(('Player', 'IP', 'H', 'ER', 'BB', 'W', 'L', 'SV', 'HLD', 'SO', 'Total'))
        for value,item in players.items():
            if 'HLD' in item:
                reader.writerow((value,item['IP'],item['H'],item['ER'],item['BB'],item['W'],item['L'],item['SV'],item['HLD'],item['SO'],item['total']))


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
            if 'OBP' in mapping:
                scores['OBP'] = float(lines[mapping['OBP']])
            if 'SB' in mapping:
                scores['SB'] = getRawValue(lines[mapping['SB']])*getRawValue(scoring['SB'])
            scores['R'] = getRawValue(lines[mapping['R']]*getRawValue(scoring['R']))
            scores['TB'] = getRawValue(lines[mapping['1B']])*getRawValue(scoring['TB']) + (getRawValue(lines[mapping['2B']])*2)*getRawValue(scoring['TB']) + (getRawValue(lines[mapping['3B']])*3)*getRawValue(scoring['TB']) + (getRawValue(lines[mapping['HR']])*4)*getRawValue(scoring['TB'])
            scores['RBI'] = getRawValue(lines[mapping['RBI']])*getRawValue(scoring['RBI'])
            scores['BB'] = getRawValue(lines[mapping['BB']])*getRawValue(scoring['BB'])
            scores['SO'] = getRawValue(lines[mapping['SO']])*getRawValue(scoring['SO'])
        if position == 'pitcher':
            for scoreType in scoring:
                if scoreType in mapping:
                    scores[scoreType] = getRawValue(lines[mapping[scoreType]])*getRawValue(scoring[scoreType])
        addPlayerScores(lines[mapping['Player']], scores)

def addPlayerScores(player, scores):
    if player.strip() in players.keys():
        for score in scores:
            if score != 'OBP':
                if score in players[player.strip()].keys():
                    players[player.strip()][score] = int(((int(players[player.strip()][score]) + int(scores[score])) / 2))
                else:
                    players[player.strip()][score] = int(scores[score])
            else:
                if 'OBP' in players[player.strip()]:
                    players[player.strip()][score] = float((float(players[player.strip()][score]) + float(scores[score])) / 2)
                else:
                    players[player.strip()][score] = float(scores[score])
    else:
        players[player.strip()] = {}
        playersName.append(player.strip())
        for score in scores:
            if score != 'OBP':
                players[player.strip()][score] = int(scores[score])
            else:
                players[player.strip()][score] = float(scores[score])


def getPlayerTotal():
    for player in players:
        players[player]['total'] = 0
        playersTotal[player] = 0
        for score in players[player]:
            if score != 'total':
                playersTotal[player] += int(players[player][score])
                players[player]['total'] += int(players[player][score])



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
    if position == 'pitcher':
        cbsPitchers = {
            'Full': 0,
            'Player': 1,
            'Position': 2,
            'Team': 3,
            'W': 4,
            'L': 5,
            'ERA': 6,
            'GP': 7,
            'GS': 8,
            'IP': 9,
            'H': 10,
            'BB': 11,
            'SO': 12,
            'SV': 13,
            'HLD': 14,
            'ER': 15
        }
        iterate(file, cbsPitchers, position)
        


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
    if position == 'pitcher':
        fangraphsPitchers = {
            '#': 0,
            'Player': 1,
            'Team': 2,
            'W': 3,
            'L': 4,
            'ERA': 5,
            'G': 6,
            'GS': 7,
            'SV': 8,
            'HLD': 9,
            'IP': 10,
            'H': 11,
            'ER': 12,
            'BB': 13,
            'SO': 14
        }
        iterate(file, fangraphsPitchers, position)

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
    if position == 'pitcher':
        razzballPitchers = {
            'Player': 0,
            'Team': 1,
            'POS': 2,
            'R/L': 3,
            'G': 4,
            'GS': 5,
            'IP': 6,
            'W': 7,
            'L': 8,
            'SV': 9,
            'HLD': 10,
            'ERA': 11,
            'SO': 12,
            'BB': 13,
            'H': 14,
            'ER': 15,
            'LD%': 16
        }
        iterate(file, razzballPitchers, position)

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
    if position == 'pitcher':
        fantasyprosPitchers = {
            'Player': 0,
            'Team': 1,
            'Positions': 2,
            'IP': 3,
            'SO': 4,
            'W': 5,
            'SV': 6,
            'ERA': 7,
            'ER': 8,
            'H': 9,
            'BB': 10,
            'HR': 11,
            'G': 12,
            'GS': 13,
            'L': 14,
            'CG': 15
        }
        iterate(file, fantasyprosPitchers, position)



main()
getPlayerTotal()
totalWriter()
detailBatterWriter()
detailPitcherWriter()
print('DONE!')