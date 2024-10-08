#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dijkstra.py
at https://github.com/bomonike/python-samples/
calculates the optimal path from A to E (5 nodes) as
illustrated at: https://www.pythonpool.com/dijkstras-algorithm-python/
Distances between nodes can be hours time or miles.
Here Python lambda functions are used.
NOTE: The Dijkstra algorithm takes more time than the 
      A* heuristic algorithm.
"""

def dijkstra(current, nodes, distances):
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

if __name__ == "__main__":

    # TODO: Define these outside the program from a file?
    current = 'A'  # Starting node.
    nodes = ('A', 'B', 'C', 'D', 'E')
    distances = {  # between nodes:
        'A': {'B': 5, 'C': 2},
        'B': {'C': 2, 'D': 3},
        'C': {'B': 3, 'D': 7},
        'D': {'E': 7},
        'E': {'D': 9}}
    print(dijkstra(current, nodes, distances))
        # [('C', 2), ('B', 5)]
        # [('B', 5), ('D', 9)]
        # [('D', 8)]
        # [('E', 15)]
        # return visited:
        # {'A': 0, 'C': 2, 'B': 5, 'D': 8, 'E': 15}
    # TODO: Illustrate visually in a GUI?