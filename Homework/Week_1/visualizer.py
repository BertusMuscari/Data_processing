#!/usr/bin/env python
# Name: Machiel Cligge
# Student number: 10772006
"""
This script visualizes data obtained from a .csv file
"""

import csv
import matplotlib.pyplot as plt
from statistics import mean

# Global constants for the input file, first and last year
INPUT_CSV = "movies.csv"
START_YEAR = 2008
END_YEAR = 2018

# Global dictionary for the data
data_dict = {str(key): [] for key in range(START_YEAR, END_YEAR)}

# Open csv file as dictionary
with open(INPUT_CSV, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    # Add all ratings from movies to each year
    for movie in reader:
        data_dict[movie['Year']].append(float((movie['Rating'])))

    # Take mean from ratings
    for key in data_dict:
        data_dict[key] = mean(data_dict[key])


if __name__ == "__main__":
    print(data_dict)
