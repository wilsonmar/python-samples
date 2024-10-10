#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dijkstras.py at https://github.com/wilsonmar/python-samples/blob/main/dijkstras.py

gas "v005 + rename from dijkstra.py :dijkstras.py"

This program uses different alogorithms to calculate the 
shortest distance to each node using the Dijkstra algorithm, 

Dijkstra is called "greedy" since it makes the locally optimal 
choice at each stage with the hope of finding a global optimum.
By contrast, the A* (A-star) heuristic algorithm at https://www.pythonpool.com/a-star-algorithm-python/
references from each node an additional dimension of distance to the global target.

Alternative: https://www.youtube.com/watch?v=IG1QioWSXRI
"""

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
            print('Path not reachable')
            break
    path.insert(0,start)
    if shortest_distance[goal] != infinity:
        print('Shortest distance is ' + str(shortest_distance[goal]), end=" ")
        print('along path ' + str(path))

    # TODO: Print intermediate stage nodes with distances.
    return

if __name__ == "__main__":

    # TODO: Define these outside the program from a file?
    start = 'A'  # Starting node.
    goal = "F"
    nodes = ('A', 'B', 'C', 'D', 'E', 'F')
#    graph = { # between nodes, from
#        'A': {'B': 5, 'C': 2},
#        'B': {'C': 2, 'D': 3},
#        'C': {'B': 3, 'D': 7},
#        'D': {'E': 7},
#        'E': {'D': 9}}

    graph = { # between nodes, from https://www.youtube.com/watch?v=OrJ004Wid4o
        'A': {'B': 2, 'C': 4},
        'B': {'A': 2, 'C': 3, 'D': 8},
        'C': {'A': 4, 'B': 3, 'E': 5, 'D': 2},
        'D': {'B': 8, 'C': 2, 'E': 11 , 'F': 22},
        'E': {'C': 5, 'D': 11, 'F': 1},
        'F': {'D': 22, 'E': 1}}
        # CAUTION: Values in distances cannot be negative.
    print(dijkstra1(start, nodes, graph))
        # Numeric distances between nodes can be hours time or miles:
        # [('B', 2), ('C', 4)]
        # [('C', 4), ('D', 10)]
        # [('D', 6), ('E', 9)]
        # [('E', 9)]
        # return visited: A C E F = 10
        # {'A': 0, 'B': 2, 'C': 4, 'D': 6, 'E': 9, 'F': 10}

    # graph = {'a':{'b':10,'c':3},'b':{'c':1,'d':2},'c':{'b':4,'d':8,'e':2},'d':{'e':7},'e':{'d':9}}
    # goal = "E"
    print(dijkstra2(graph,start,goal))
        # Shortest distance is 10
        # And the path is ['A', 'C', 'E', 'F']
        # None
    # TODO: Illustrate visually in a GUI?
    # https://www.youtube.com/watch?v=OrJ004Wid4o
    # https://neetcode.io/problems/dijkstra
    # https://www.youtube.com/watch?v=_B5cx-WD5EA&t=29s