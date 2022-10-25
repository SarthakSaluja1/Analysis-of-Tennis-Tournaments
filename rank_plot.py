'''
This file contains functions that help in plotting the ranks in last 52 weeks 
'''


import structure_tournaments as st
import tournament_stats as ts

def sublist(lst, date) :
    '''
    Function to retrieve matches played in the last 52 weeks
    Assumes a list of matches, and a datetime object
    Returns a list of matches played in the last 52 weeks.
    '''

    output = [rows for rows in lst if ((rows[2] - date).days/7 < 0) and ((rows[2] - date).days/7 >= -52)]
    return output


def plot_WTA_vs_WbW(lst) :
    '''
    Assumes a list of matches.
    Returns a list that shows
    progression of WTA and WbW ranking of all  players in given period
    '''
    WTA = []
    WbW = []
    grouped_list = st.grouping(lst)
    for g in grouped_list :
        start_date = g[0][1]
        if start_date.year != 2007 :
            new_list = sublist(lst, start_date) #Will return a list of tournament matches, where the tournament end date was 52 weeks before the start date of this tournament.
            rank = ts.get_WbW_rank(new_list) #Gets rank based on results from 52 weeks before start of tournament
            #Note - This algorithm will take into consideration the start date of each grouped touurnament. For example,
            #ASB Classic 2008-01-01 was grouped with ASB Classic 2007-12-31 as per our algorithm. This is likely to produce
            #the most legible results as tournaments are grouped according to their 'true' start dates. Moreover. a new list is
            #returned for every new _tournament_ and not _match_ thus making sure that the ranking used is based on results completed
            #before the tournament began.
            rank_dct = {} #Store the ranking as a dictionary to avoid nested looping later
            prev= rank[0][1]
            i = 1
            for k, v in rank :
                rank_dct.update({k : 0})
                if v <= prev :
                    rank_dct[k] += i
                    i+=1
                    prev = v

            players = set()
            for matches in g :
                player_1 = matches[4]
                player_2 = matches[5]

                if player_1 not in players and player_1 in rank_dct.keys(): #Makes sure that a player's rank is only added once
                    if matches[6] != '' :
                        WTA.append(matches[6])
                        WbW.append(rank_dct[player_1])
                        players.add(player_1)
                if player_2 not in players and player_2 in rank_dct.keys():
                    if matches[7] != '' :
                        WTA.append(matches[7])
                        WbW.append(rank_dct[player_2])
                        players.add(player_2)

    return (WTA, WbW)
