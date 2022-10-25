from itertools import groupby

def get_winner(lst) :
    '''
    Assumes a list object where each list
    within represents tennis matches, modifies
    the list in place indicating the winner of match
    '''
    for row in lst :
        player_1 = row[4]
        player_2 = row[5]
        set_1 = row[8]
        set_2 = row[9]
        set_3 = row[10]

        if row[11] == 'Completed' : #For completed matches
            i = 0
            set_1 = set_1.split('-')
            set_1 = [int(i) for i in set_1]

            set_2 = set_2.split('-')
            set_2 = [int(i) for i in set_2]

            if set_1[0] > set_1[1] :
                i += 1
            if set_2[0] > set_2[1] :
                i += 1

                #Match going to third set
            if set_3 != '' :
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


def grouping_tournaments(lst) :
    '''
    Assumes a list object where each list
    within represents tennis matches, assumes that
    the list is sorted and same tournaments appear together.
    Returns a grouped list of tournaments and their matches
    '''
    grouped_lst = []
    for k, g in groupby(lst,  lambda x: (x[0], x[1])) :
       grouped_lst.append(list(g))    # Store group iterator as a list
    return grouped_lst
