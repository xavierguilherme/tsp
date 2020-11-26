from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.sparse import csr_matrix
from itertools import combinations
from munkres import Munkres
from numpy import triu, inf, array

N_VERTICES = None


def christofides(adjacency_matrix):
    global N_VERTICES
    N_VERTICES = len(adjacency_matrix)

    # Create a minimum spanning tree
    mst = minimum_spanning_tree(csr_matrix(triu(adjacency_matrix)))

    # Create a graph representation using python dictionary
    graph = generate_graph(adjacency_matrix, mst)

    # Get odd degree vertices
    odd_vertices = odd_degree_vertices(graph)

    # Generate a combination between all odd degree vertices
    odd_vert_combinations = [set(i) for i in combinations(set(odd_vertices), len(odd_vertices) // 2)]
    odd_vert_subgraph = odd_vertices_subgraph(adjacency_matrix, odd_vert_combinations, odd_vertices)

    # Use Munkres algorithm to find a minimum_weight perfect matching
    munkres(adjacency_matrix, graph, odd_vert_subgraph)

    # Form an Eulerian circuit
    path = eulerian_circuit(graph)

    # Convert to a Hamiltonian circuit (shortcutting)
    shortcut_path = hamiltonian_circuit(path)

    # Get total cost of Hamiltonian circuit
    cost = path_cost(adjacency_matrix, shortcut_path)

    return cost, shortcut_path


def generate_graph(adjacency_matrix, mst):
    graph = {}

    for v1, v2 in list(zip(*mst.nonzero())):

        if v1.item() not in graph:
            graph[v1.item()] = {}
        if v2.item() not in graph:
            graph[v2.item()] = {}

        graph[v1.item()][v2.item()] = adjacency_matrix[v1.item()][v2.item()]
        graph[v2.item()][v1.item()] = adjacency_matrix[v1.item()][v2.item()]

    return graph


def odd_degree_vertices(mst):
    odd_vertices = [vertex for vertex, neighbors in mst.items() if len(neighbors) % 2 == 1]

    return sorted(odd_vertices)


def odd_vertices_subgraph(adjacency_matrix, odd_vert_combinations, odd_vertices):
    subgraphs = []
    vertex_sets = []
    for vertex_set1 in odd_vert_combinations:
        vertex_set1 = list(sorted(vertex_set1))
        vertex_set2 = []
        for vertex in odd_vertices:
            if vertex not in vertex_set1:
                vertex_set2.append(vertex)
        matrix = [[inf for _ in enumerate(vertex_set2)] for _ in enumerate(vertex_set1)]

        for i in range(len(vertex_set1)):
            for j in range(len(vertex_set2)):
                matrix[i][j] = adjacency_matrix[vertex_set1[i]][vertex_set2[j]]

        subgraphs.append(matrix)

        vertex_sets.append([vertex_set1, vertex_set2])

    return [subgraphs, vertex_sets]


def munkres(adjacency_matrix, graph, odd_vert_subgraph):
    m = Munkres()
    minimum = inf

    for index, bip_graph in enumerate(odd_vert_subgraph[0]):
        munkres_indexes = m.compute(bip_graph)

        cost = 0
        for idx in munkres_indexes:
            cost += bip_graph[idx[0]][idx[1]]

        if cost < minimum:
            minimum = cost
            min_index = index
            min_munkres_indexes = munkres_indexes

    munkres_indexes = [[]] * len(min_munkres_indexes)

    for index, vertex_set in enumerate(min_munkres_indexes):
        munkres_indexes[index].append(odd_vert_subgraph[1][min_index][0][vertex_set[0]])
        munkres_indexes[index].append(odd_vert_subgraph[1][min_index][1][vertex_set[1]])

    for match in munkres_indexes:
        graph[match[0]][match[1]] = adjacency_matrix[match[0]][match[1]]
        graph[match[1]][match[0]] = adjacency_matrix[match[0]][match[1]]


def eulerian_circuit(graph):
    start_vertex = list(graph[0])[0]
    path = [list(graph[start_vertex])[0]]

    while len(graph) > 0:

        for index, vertex in enumerate(path):
            if vertex in graph and len(graph[vertex]) > 0:
                break

        while vertex in graph:
            next_vertex = list(graph[vertex])[0]

            del graph[vertex][next_vertex]
            del graph[next_vertex][vertex]

            if len(graph[vertex]) == 0:
                del graph[vertex]
            if len(graph[next_vertex]) == 0:
                del graph[next_vertex]

            index += 1
            path.insert(index, next_vertex)
            vertex = next_vertex

    return path


def hamiltonian_circuit(path):
    shortcut_path = []
    for vertex in path:
        if vertex not in shortcut_path:
            shortcut_path.append(vertex)

    shortcut_path = list(array(shortcut_path) + 1)
    shortcut_path.append(1)

    return shortcut_path


def path_cost(adjacency_matrix, path):
    weight = 0
    for i in range(len(path) - 1):
        weight += adjacency_matrix[path[i]-1, path[i + 1]-1]

    return weight
