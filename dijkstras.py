#!/usr/bin/env python3

"""dijkstras.py at https://github.com/wilsonmar/python-samples/blob/main/dijkstras.py

"v009 + globals, display_tree :dijkstras.py"
STATUS: Working

This program has a time complexity of O(E*log(V)).
Illustrated within python-graphs-1.pptx at https://7451111251303.gumroad.com/l/rsvia

This program compares different alogorithms to calculate the 
shortest distance to each node using the Dijkstra algorithm
used by map apps, computer network routing, etc.
    * https://www.youtube.com/watch?v=WJFWb9Z5uHY

Dijkstra is called "greedy" since it makes the locally optimal by,
at each stage, choosing the node (aka vertex) with the smallest 
weight or distance (along an edge) to the next node/vertex,
without taking additional analysis effort to identify
a shorter total/global path.

On a table (matrix) to calculate the total cost of each path,
https://www.youtube.com/watch?v=db_-e07jkjo
draws a square around the least costly distance to the next node
in a matrix.

The shortest path picked starting at the end.

The A* (A-star) algorithm at https://www.pythonpool.com/a-star-algorithm-python/
adds an additional dimension of a heuristic variable to estimate for each node
a distance to the global target "as the crow flies"`.

Highest rated videos:
* https://www.youtube.com/watch?v=pVfj6mxhdMw by Computer Science Lessons [DataSet 1]
    # https://www.youtube.com/watch?v=OrJ004Wid4o
    # https://neetcode.io/problems/dijkstra
    # https://www.youtube.com/watch?v=_B5cx-WD5EA&t=29s

Generalization of this is Graph handling in Python:
* https://www.udemy.com/course/data-structures-and-algorithms-in-python-gb/learn/lecture/39778648#overview


"""
# no imports

# Define Global:
SHOW_GRAPH = True
SHOW_NODES = False

# Code here do not insert graph data, just read.

def dijkstra1(current, nodes, distances):
    # From Pratik Kinage at https://www.pythonpool.com/dijkstras-algorithm-python/
    print(f"*** dijkstra1() From Pratik Kinage:")
    # and https://www.youtube.com/playlist?list=PL5-M_tYf311Y8R3h81RiZFYnWrBv2kfj6
    # This outputs just the total distance to each node from A. As in:
        # {'A': 0, 'B': 2, 'C': 4, 'D': 6, 'E': 9, 'F': 10}
    # This does not output the optimal path (such as A C D E).

    # Code here uses Python lambda functions.
    # All the nodes which have not been visited yet:
    unvisited = {node: None for node in nodes}
    # Store the shortest distance from one node to another:
    visited = {}
    # Store the predecessors of the nodes:
    currentDistance = 0
    unvisited[current] = currentDistance
    # Running the loop while all the nodes have been visited:
    while True:
        # iterating through all the unvisited node:
        for neighbour, distance in distances[current].items():
            # Iterating through the connected nodes of current_node (for
            # example, a is connected with b and c having values 10 and 3
            # respectively) and the weight of the edges:
            if neighbour not in unvisited: continue
            newDistance = currentDistance + distance
            if unvisited[neighbour] is None or unvisited[neighbour] > newDistance:
                unvisited[neighbour] = newDistance
        # Till now the shortest distance between the source node and target node
        # has been found. Set the current node as the target node:
        visited[current] = currentDistance
        del unvisited[current]
        if not unvisited: break
        candidates = [node for node in unvisited.items() if node[1]]
        print(sorted(candidates, key = lambda x: x[1]))
        current, currentDistance = sorted(candidates, key = lambda x: x[1])[0]
    return visited

def dijkstra2(graph,start,goal):
    # From Ian Sullivan at https://pastebin.com/3Q9rqGHA
    # described at https://www.youtube.com/watch?v=OrJ004Wid4o
    print(f"*** dijkstra2() From Ian Sullivan:")
    shortest_distance = {}
    predecessor = {}
    unseenNodes = graph
    infinity = 9999999
    path = []
    for node in unseenNodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0

    while unseenNodes:
        minNode = None
        for node in unseenNodes:
            if minNode is None:
                minNode = node
            elif shortest_distance[node] < shortest_distance[minNode]:
                minNode = node

        for childNode, weight in graph[minNode].items():
            if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                shortest_distance[childNode] = weight + shortest_distance[minNode]
                predecessor[childNode] = minNode
        unseenNodes.pop(minNode)

    currentNode = goal
    while currentNode != start:
        try:
            path.insert(0,currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print('*** Path not reachable')
            break
    path.insert(0,start)
    if shortest_distance[goal] != infinity:
        print('*** Shortest distance is ' + str(shortest_distance[goal]), end=" ")
        print('along path ' + str(path))

    # TODO: Print intermediate stage nodes with distances.
    return


def display_tree(dictionary, indent=""):
    """Display dictionary graph with indents.
    """
    # TODO: Ensure that only one edge is specified. No multigraphs allowed.
    for key, value in dictionary.items():
        print(f"{indent}Key: {key}")
        if isinstance(value, dict):
            display_tree(value, indent + "  ")
        else:
            print(f"{indent}  Value: {value}")


if __name__ == "__main__":

    # TODO: Define these outside the program from a file?

    start = 'A'  # Starting node. Applies to all datasets.
    goal = "E"

    # The graph is an "Adjacency List" with values to each edge.
    # Values in graphs can be decimal (not just integers).
    # Vertices can be two-way (non-directed graphs (aka digraph)
    # [DataSet 1] explained by https://www.youtube.com/watch?v=pVfj6mxhdMw
    nodes = ('A', 'B', 'C', 'D', 'E')
    graph = { # between nodes, from
        'A': {'B': 6, 'D': 1},
        'B': {'A': 6, 'C': 5, 'E':2},
        'C': {'B': 5, 'E': 5},
        'D': {'A': 1, 'E': 1},
        'E': {'D': 1, 'B': 2, 'C': 5}}
    # The graph can be displayed as an adjancy matrix or incidence matrix.
    if SHOW_GRAPH == True:
        display_tree(graph, indent="")

    goal = "F"
    nodes = ('A', 'B', 'C', 'D', 'E', 'F')
    graph = { # between nodes, from
        'A': {'B': 3, 'C': 6, 'D': 4},
        'B': {'A': 3, 'C': 2, 'E': 3},
        'C': {'A': 6, 'B': 2, 'E': 3, 'F': 3},
        'D': {'A': 4, 'F': 6},
        'E': {'B': 3, 'C': 3, 'F': 1},
        'F': {'C': 3, 'D': 6, 'E': 1}}
    if SHOW_GRAPH == True:
        display_tree(graph, indent="")

    if SHOW_NODES == True:
        print(dijkstra1(start, nodes, graph))
        # {'A': 0, 'D': 1, 'E': 2, 'B': 4, 'C': 7}
    print(dijkstra2(graph,start,goal))
        # *** dijkstra2() From Ian Sullivan:
        # Shortest distance is 2 along path ['A', 'D', 'E']

    print(" ")

    # [DataSet 2] explained by https://www.youtube.com/watch?v=OrJ004Wid4o
    nodes = ('A', 'B', 'C', 'D', 'E', 'F')
#    graph = { # between nodes, from
#        'A': {'B': 5, 'C': 2},
#        'B': {'C': 2, 'D': 3},
#        'C': {'B': 3, 'D': 7},
#        'D': {'E': 7},
#        'E': {'D': 9}}
    graph = { # between nodes
        'A': {'B': 2, 'C': 4},
        'B': {'A': 2, 'C': 3, 'D': 8},
        'C': {'A': 4, 'B': 3, 'E': 5, 'D': 2},
        'D': {'B': 8, 'C': 2, 'E': 11 , 'F': 22},
        'E': {'C': 5, 'D': 11, 'F': 1},
        'F': {'D': 22, 'E': 1}}
        # CAUTION: Values in distances cannot be negative.
    if SHOW_GRAPH == True:
        display_tree(graph, indent="--")
    if SHOW_NODES == True:
        print(dijkstra1(start, nodes, graph))
        # Numeric distances between nodes can be hours time or miles:
        # [('B', 2), ('C', 4)]
        # [('C', 4), ('D', 10)]
        # [('D', 6), ('E', 9)]
        # [('E', 9)]
        # return visited: A C E F = 10
        # {'A': 0, 'B': 2, 'C': 4, 'D': 6, 'E': 9, 'F': 10}
    print(dijkstra2(graph,start,goal))
        # Shortest distance is 10
        # And the path is ['A', 'C', 'E', 'F']
        # None

    # TODO: Illustrate visually in a GUI?


# def dijkstra3(graph, start): # by https://www.youtube.com/watch?v=_B5cx-WD5EA
    # Code requested from glassbyte.io@gmail.com
#    graph = { # between nodes, from
#        'A': {'B': 3, 'C': 6, 'D': 4},
#        'B': {'A': 3, 'C': 2, 'E': 3},
#        'C': {'A': 6, 'B': 2, 'E': 3, 'F': 3},
#        'D': {'A': 4, 'F': 6},
#        'E': {'B': 3, 'C': 3, 'F': 1}
#        'F': {'C': 3, 'D': 6, 'E': 1}}

