from itertools import combinations


def held_karp(graph):
    n = len(graph)

    vertices = [k for k in range(1, n)]

    # Set costs starting from initial vertex
    subproblems = {((vertex,), vertex): (graph[0][vertex], 0) for vertex in vertices}

    # Set costs of all other subproblems
    for size in range(2, n):
        for subset in combinations(vertices, size):

            list_subset = list(subset)

            # Find the lowest cost related to this subproblem
            for vertex in subset:
                remaining_vertices = list_subset[:]
                remaining_vertices.remove(vertex)
                res = []
                for remaining_vertex in remaining_vertices:
                    res.append((subproblems[(tuple(remaining_vertices), remaining_vertex)][0]
                                + graph[remaining_vertex][vertex], remaining_vertex))
                subproblems[(tuple(list_subset), vertex)] = min(res)

    # Find the length of an optimal path
    res = []
    for k in range(1, n):
        res.append((subproblems[(tuple(vertices), k)][0] + graph[k][0], k))
    cost, parent = min(res)

    # Backtrack to find optimal TSP path
    path = [1]
    vertices_list = vertices[:]
    while len(vertices_list) != 0:
        path.append(parent + 1)
        parent = subproblems[(tuple(vertices_list), parent)][1]
        vertices_list.remove(path[-1] - 1)
    path.append(1)

    return cost, path[::-1]
