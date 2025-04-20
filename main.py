import math
import heapq
from collections import deque



class Graph:
    def __init__(self):
        self._vertices = set()   #Set for faster lookup!!
        self._adj = {}  # Adjacency list representation of the graph

    def add_vertex(self, vertex):
        if not isinstance(vertex, str):
            raise TypeError("Vertex must be a string")
        if vertex in self._vertices:
            raise ValueError(f"Vertex '{vertex}' already exists")
        self._vertices.add(vertex)
        self._adj[vertex] = {}
        return self

