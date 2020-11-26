import os
import re
from numpy import loadtxt

DIR = 'data/'


def run():

    for filename in os.listdir(DIR):
        with open(f'{DIR}{filename}', 'r') as file:
            lines = file.readlines()

        lines = [re.sub('\s+', ',', line.strip()) for line in lines]

        with open(f'{DIR}{filename}', 'w') as file:
            file.writelines(line + '\n' for line in lines)

    # Fix tsp4_7013 file error, matrix is duplicated
    adjacency_matrix = loadtxt(f'{DIR}tsp4_7013.txt', dtype='int', delimiter=',')
    adjacency_matrix_fixed = adjacency_matrix[:22, :22]
    lines = [re.sub('\s+', ',', " ".join(map(str, line))) for line in adjacency_matrix_fixed]
    with open(f'{DIR}tsp4_7013_fixed.txt', 'w+') as file:
        file.writelines(line + '\n' for line in lines)