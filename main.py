from numpy import loadtxt
from time import time
import data_processing
from held_karp import held_karp
from christofides import christofides

# Split each value with a comma and fix tsp4_7013 duplicated matrix error
# data_processing.run()

problems = ['1_253', '2_1248', '3_1194', '4_7013_fixed', '5_27603']

for problem in problems:
    adjacency_matrix = loadtxt(f'data/tsp{problem}.txt', dtype='int', delimiter=',')
    print(f'tsp{problem}')
    start = time()
    cost, path = christofides(adjacency_matrix)
    exec_time = time() - start
    print(f'Christofides (Approximation Algorithm)'
          f'\n\tPath: {path}'
          f'\n\tCost: {cost}'
          f'\n\tExecution time: {"{:.5f}".format(exec_time)} seconds')
    start = time()
    cost, path = held_karp(adjacency_matrix)
    exec_time = time() - start
    print(f'Held-Karp (Exact Algorithm)'
          f'\n\tPath: {path}'
          f'\n\tCost: {cost}'
          f'\n\tExecution time: {"{:.5f}".format(exec_time)} seconds')





