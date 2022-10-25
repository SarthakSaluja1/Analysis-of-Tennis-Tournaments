'''
This file contains functions that are used to calculate some crucial
statistics of a tournament
'''

import math
import structure_tournaments as st

def tournament_stats(lst) :
    '''
    Function to estimate some tournament stats for all tournaments given.
    Assumes a list of matches grouped by tournaments.
    Returns dictionary indicating total participants, total rounds and total matches played
    '''

    total_participants = {}
    total_rounds = {}
    total_matches = {}
    tournament = []
    for g in lst :
        participants = set()
        name = g[0][0]
        date = str(g[0][1])
        tourney = name + ' ' + date
        total_participants.update({tourney : 0})
        total_rounds.update({tourney : 0})
        total_matches.update({tourney : 1})
        tournament.append([tourney, 0])
        total_matches[tourney] = len(g)
        for match in g :
            if match[4] not in participants :
                tournament[-1][1] += 1
                participants.add(match[4])
            if match[5] not in participants :
                tournament[-1][1] += 1
                participants.add(match[5])
        total_participants[tourney] = tournament[-1][1]
        total_rounds[tourney] = math.ceil(math.log(total_participants[tourney], 2)) #Total rounds for a normal tennis tournament

    return (total_matches, total_participants, total_rounds)

def get_players(lst) :
    '''
    Function to retrieve all players based on matches provided.
    Assumes a list of matches,
    returns a set of all players who participated during the given matches.
    '''
    players = set()
    for match in lst :
        player_1 = match[4]
        player_2 = match[5]
        if player_1 not in players :
            players.add(player_1)
        if player_2 not in players :
            players.add(player_2)
    return players

def get_rank(dct) :
    '''
    Function to retrieve the order of all players based on ranking.
    Assumes a dictionary of players and the aggregated score
    on a metric of given player. Returns ordered list by rank
    '''
    sorted_list = sorted(dct.items(), key=lambda x: x[1], reverse = True)
    return sorted_list

def get_wins_rank(lst) :
    '''
    Function to estimate the number of wins of a player.
    Assumes a list of matches,
    returns a ordered list indicating each person and their wins during the given period
    '''
    players = get_players(lst)
    output = {players : 0 for players in players}#Initialize a dictionary with all players
    for match in lst :
        winner = match[12]
        output[winner] += 1

    output_list = get_rank(output)
    return output_list

def get_weighted_rank(grouped_lst, rounds) :
    '''
    Function to estimate the round weighed rank of a player.
    Assumes a list of matches grouped by tournament and dictionary indicating tournament and number of rounds played.
    Returns a sorted list of player and their score weighed by round.
    '''
    grouped = grouped_lst
    players = set()
    for t in grouped :
        for m in t :
            players.add(m[4])
            players.add(m[5])

    output = {players : 0 for players in players}
    n_rounds = rounds
    for tournament in grouped :
        name = tournament[0][0]
        date = str(tournament[0][1])
        tourney = name + ' ' + date
        rounds = n_rounds[tourney]
        for match in tournament :
            player_1 = match[4]
            player_2 = match[5]
            match_round = match[13]
            winner = match[12]
            if player_1 == winner :
                loser = player_2
            else :
                loser = player_1
            if match_round == 'Finals' :
                r = rounds
            elif match_round == 'Third Place' :
                r = rounds
            elif match_round == 'Semi Finals' :
                r = rounds - 1
            elif match_round == 'Quarter Finals' :
                r = rounds - 2
            elif match_round == 'Group Stage' :
                r = 1
            else :
                r = match_round
            output[winner] += r
            output[loser] -= 1/r
    output_list = get_rank(output)
    return output_list

def get_WbW_rank(lst) :
    '''
    Function to estimate the Winner beat Winner rank of a player.
    Assumes a list of matches ,
    Returns a sorted list of players and their WbW score.
    '''
    players = get_players(lst)
    count_players = len(players)
    initial = 1/count_players
    lost_to = {players : [] for players in players}
    for match in lst :
        player1 = match[4]
        player2 = match[5]
        winner = match[12]
        if player1 == winner :
            loser = player2
        else :
            loser = player1
        lost_to[loser].append(winner)
    old_output = {players : initial for players in players} #initialize
    old_output_rank = get_rank(old_output)
    old_output_list = [k for k, v in old_output_rank] #Use a list of ordered players to test convergence to avoid comparing decimal.decimals

    while True :
        new_output = {players : 0 for players in old_output}
        new_output_rank = {}
        for key in old_output :
            beat = lost_to[key]
            loss = len(beat)
            if loss == 0 :
                new_output[key] += 2 * old_output[key]
            else :
                temp = old_output[key]/loss
                new_output[key] += old_output[key] - temp
                for players in beat :
                    new_output[players] += temp
            new_output[key] = 0.85*new_output[key] + (0.15/count_players) #rescale
        new_output_rank = get_rank(new_output) #sort dictionary
        new_output_list = [k for k, v in new_output_rank] #Extract list of sorted names
        if old_output_list == new_output_list : #convergence criteria
            break
        old_output = new_output
        old_output_rank = new_output_rank
        old_output_list = new_output_list

    return new_output_rank
