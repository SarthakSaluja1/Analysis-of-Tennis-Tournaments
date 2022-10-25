import csv
from datetime import datetime
import os

def get_data(files) :
    '''
    To convert rows in data frame into lists and store them all in one list
    Assumes a list of '.csv' file
    Returns a list with each element list representing a row of the given files
    '''
    final_list = []
    errors = []
    for file in files :
        file = '../assignment-final-data/' + file
        with open(file, 'r') as df :
            next(df)
            df_reader = csv.reader(df)
            for matches in df_reader :
                matches[1] = datetime.strptime(matches[1], "%Y-%m-%d").date()
                matches[2] = datetime.strptime(matches[2], "%Y-%m-%d").date()
                matches[3] = int(matches[3])
                if matches[6] != '' :
                    matches[6] = int(float(matches[6]))
                if matches[7] != ''  :
                    matches[7] = int(float(matches[7]))

                start_date = matches[1]
                end_date = matches[2]
                condition = ((end_date.day == 31 and end_date.month == 12) or
                             (start_date.day == 1 and start_date.day == 1) and
                             (start_date.year != 2007 and
                              start_date.year != 2017)) #To avoid ASB Classics in 2007 and 2017
                if condition :
                    errors.append(matches)
                    continue

                final_list.append(matches)

    return [final_list, errors]
