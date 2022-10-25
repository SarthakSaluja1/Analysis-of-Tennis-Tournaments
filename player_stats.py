import structure_tournaments as st
import tournament_stats as stats

def get_players(lst) :
    '''
    Assumes a list object where each list
    within represents tennis matches,
    returns a set of all players who participated during the given matches
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
    Assumes a dictionary of players and the aggregated score
    on a metric of given player. Returns ordered list by rank
    '''

    output = {}
    sorted_list = sorted(dct.items(), key=lambda x: x[1], reverse = True)

    return sorted_list

def get_wins_rank(lst) :
    '''
    Assumes a list object where each list
    within represents tennis matches and set of players in given list,
    returns a dictionary indicating each person and their rank based on wins
    during the given period
    '''
    players = get_players(lst)
    output = {players : 0 for players in players}#Initialize a dictionary with all players
    output_dct = {}

    for match in lst :
        winner = match[12]
        output[winner] += 1

    output_list = get_rank(output)


    return output_list

def get_weighted_rank(lst, rounds) :
    '''
    Assumes a grouped by tournament list where each list within represents
    a tennis match and a dictionary of its rounds. Returns the dictionary of player and
    their rank by score weighted by round.
    '''

    players = get_players(lst)
    output = {players : 0 for players in players}
    grouped = st.grouping(lst)
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
    Assumes a list where each list within represents
    a tennis match. Returns the dictionary of player and
    their WbW rank for the given period
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

        new_output_rank = get_rank(new_output)
        #Sort this dictionary and 'rank' it then compare. Should work


        if old_output_rank == new_output_rank :
            break

        old_output = new_output
        old_output_rank = new_output_rank

    return new_output_rank
