'''
This file contains functions that help with cleaning and returning
list of tournaments in a way that can be used for final analysis
'''

from itertools import groupby
import tournament_stats as ts

def grouping(lst) :
    '''
    Groups a list by consecutive tournaments.
    Assumes a sorted list object where each list
    within represents tennis matches. Returns a grouped list of tournaments and their matches
    '''
    grouped_lst = []
    for k, g in groupby(lst,  lambda x: (x[0], x[1])) :
       grouped_lst.append(list(g))    # Store group iterator as a list
    return grouped_lst


def get_winner(lst) :
    '''
    Modifies list in place to add winner.
    Assumes a list object where each list
    within represents tennis matches, modifies in place.
    '''
    for row in lst :
        player_1 = row[4]
        player_2 = row[5]
        set_1 = row[8]
        set_2 = row[9]
        set_3 = row[10]
        if row[11] == 'Completed' : #For completed matches
            i = 0

            # Clean string containing scores in each set and store the results
            # in a list of list

            set_1 = set_1.split('-')
            set_1 = [int(i) for i in set_1]
            set_2 = set_2.split('-')
            set_2 = [int(i) for i in set_2]

            # A player wins a match if the number of sets they win is greater than
            # the number of sets won by the opponent

            if set_1[0] > set_1[1] :
                i += 1
            if set_2[0] > set_2[1] :
                i += 1

            if set_3 != '' : #Match going to third set
                set_3 = set_3.split('-')
                set_3 = [int(i) for i in set_3]
                if set_3[0] > set_3[1] :
                    i += 1
            if i >= 2 :
                row.append(player_1)
            else :
                row.append(player_2)

        else : #Matches that were not completed
            store = row[11].split(' Retired')
            if player_1 != store[0] :
                row.append(player_1)
            else :
                row.append(player_2)


def reconstruct_tournament(lst, round_robin) :
    '''
    Assumes a list of matches grouped by tournaments and list
    containing names of round robin tournaments.
    Modifies list in place to add the round for each match played.
    '''

    # Get the total matches, total participants and number of rounds of each tournament

    total_matches, total_participants, total_rounds = ts.tournament_stats(lst)

    for tournament in lst :
        count = [] #List containing the number of appearences by a player in the tournament
        sf_loser = [] #List containing players losing in semi finals to later calculate third place matches
        participants = set() #Set containing all participants in the tournament for calculating 'byes'
        name = tournament[0][0] # Name of the tournament
        date = str(tournament[0][1]) # Tournament start date
        year = str(tournament[0][1].year) # Tournament start year
        tourney = name + ' ' + date # To access dictionary
        name_y = name + ' ' + year # To check if row in round robin
        no_of_players = total_participants[tourney] # stores the number of players in tournament
        no_of_matches = total_matches[tourney] # stores the number of matches in tournament
        rounds = total_rounds[tourney] # stores the number of rounds in a tournament

        if name_y not in round_robin : #Different algorithm for RR tourneys

            for match in tournament : #iterate through all matches in the tournament
                i = 1
                player_1 = match[4] #Stores player1
                player_2 = match[5] #Stores player2

                if (player_1 in sf_loser) or (player_2 in sf_loser) : #Third place match can only happen after semifinals
                        match.append('Third Place')
                else :
                    if player_1 in count :
                        i += count.count(player_1)
                        if i < rounds - 2 :
                            match.append(i)
                        elif i == rounds - 2 :
                            match.append('Quarter Finals')
                        elif i == rounds - 1 :
                            match.append('Semi Finals')
                        elif i == rounds :
                            match.append('Finals')
                    elif player_2 in count : # To account for byes in R2
                        i += count.count(player_2)
                        match.append(i)
                    else :
                        match.append(i)
                if i == 1 : #Store the participants of R1
                    participants.add(player_1)
                    participants.add(player_2)
                if i == 2 : #Add the players that got a 'bye' in R1 to the winners list twice. Assumption is that players who got a bye in R1 will not go against each other in R2 as they are likely to be the top seeded ones.
                    if player_1 not in participants :
                        count.append(player_1)
                    if player_2 not in participants :
                        count.append(player_2)
                if i == rounds - 2 : #Store semi finals players for evaluating third place match
                    if player_1 != match[12] :
                        sf_loser.append(player_1)
                    else :
                        sf_loser.append(player_2)
                count.append(player_1)
                count.append(player_2)

        elif name_y in round_robin :
            for match in tournament :
                player_1 = match[4]
                player_2 = match[5]
                count.append(player_1)
                count.append(player_2)
                i = max(count.count(player_1), count.count(player_2)) #To account for alternatives, assumption being that two alternatives will never go against each other
                if name != 'WTA Elite Trophy' and name != 'Commonwealth Bank Tournament of Champions':
                    if i <= 3 :
                        match.append('Group Stage')
                    elif i == 4 :
                        match.append('Semi Finals')
                    elif i == 5 :
                        match.append('Finals')
                else :  #As WTA Elite Trophy and Commonwealth 2019 have 12 participants divided into 4 groups of 3 participants. This is legible as round robins were indicated separately
                    if i <= 2 :
                        match.append('Group Stage')
                    elif i == 3 :
                        match.append('Semi Finals')
                    elif i == 4 :
                        match.append('Finals')

def correct_error_list(lst) :
    '''
    Function that corrects the abnormal cases spanning across two years.
    '''
    new = {}
    for t in grouping(lst) :
        key = t[0][0]
        year = str(t[0][1])
        new.update({key + ' ' + year : []})
        for m in t :
            new[key + ' ' + year].append(m)

    for k in new :
        prev_tournament = k
        for v in new.values():
            if v[0][0] in prev_tournament and str(v[0][1].year - 1) in prev_tournament and v[0][1].day == 1 :
                for v in v :
                    new[prev_tournament].append(v)

    check = list(new.values())

    index_list = []
    for i in range(len(check)) :
        if check[i][0][1].day == 1 :
            index_list.append(i)


    final_list = [check[i] for i in range(len(check)) if i not in index_list]

    return final_list
