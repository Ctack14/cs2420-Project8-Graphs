import math
import heapq
from collections import deque


class Graph:
    def __init__(self):
        self._vertices = set()   #Set for faster lookup!!
        self._adj = {}  # Adjacency list representation of the graph

    def add_vertex(self, label):
        if not isinstance(label, (str, int, float)):
            raise ValueError("Vertex must be a string or integer")      #Value error required by tests
        label = str(label)
        if label in self._vertices:
            raise ValueError(f"Vertex '{label}' already exists")
        if not label.strip():
            raise ValueError("Vertex label cannot be empty")

        self._vertices.add(label)
        self._adj[label] = {}
        return self

    def add_edge(self, src, dest, w):
        src, dest = str(src), str(dest)
        if src not in self._vertices or dest not in self._vertices:
            raise ValueError("Both vertices must exist in the graph")
        if not isinstance(w, (int, float)):
            raise ValueError("Weight must be a number")       #Value error required by tests
        self._adj[src][dest] = w
        return self

    def get_weight(self, src, dest):
        src, dest = str(src), str(dest)
        if src not in self._vertices or dest not in self._vertices:
            raise ValueError("Both vertices must exist in the graph")
        return self._adj[src].get(dest, math.inf)

    def dfs(self, starting_vertex):
        if starting_vertex not in self._vertices:
            raise ValueError("Starting vertex must exist in the graph")
        visited = set()
        def _dfs(v):
            visited.add(v)
            yield v
            for neighbor in sorted(self._adj[v]):
                if neighbor not in visited:
                    yield from _dfs(neighbor)
        return _dfs(starting_vertex)

    def bfs(self, starting_vertex):
        if starting_vertex not in self._vertices:
            raise ValueError("Starting vertex must exist in the graph")
        visited = {starting_vertex}
        queue = deque([starting_vertex])
        while queue:
            v = queue.popleft()
            yield v
            for neighbor in sorted(self._adj[v]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    def dsp(self, src, dest):
        if src not in self._vertices or dest not in self._vertices:
            raise ValueError("Both vertices must exist in the graph")
        dist = {v: math.inf for v in self._vertices}
        prev = {v: None for v in self._vertices}
        dist[src] = 0
        pq = [(0, src)]
        while pq:
            d, v = heapq.heappop(pq)
            if d > dist[v]:
                continue
            if v == dest:
                break
            for neighbor, weight in self._adj[v].items():
                new_dist = d + weight
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = v
                    heapq.heappush(pq, (new_dist, neighbor))
        if dist[dest] == math.inf:
            return math.inf, []

        path = []
        curr = dest
        while curr is not None:
            path.append(curr)
            curr = prev[curr]
        path.reverse()
        return dist[dest], path

    def dsp_all(self, src):
        if src not in self._vertices:
            raise ValueError("Source vertex must exist in the graph")
        dist = {v: math.inf for v in self._vertices}
        prev = {v: None for v in self._vertices}
        dist[src] = 0
        pq = [(0, src)]
        while pq:
            d, v = heapq.heappop(pq)
            if d > dist[v]:
                continue
            for neighbor, weight in self._adj[v].items():
                new_dist = d + weight
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = v
                    heapq.heappush(pq, (new_dist, neighbor))
        paths = {}
        for v in self._vertices:
            if dist[v] == math.inf:
                paths[v] = []
            else:
                path = []
                curr = v
                while curr is not None:
                    path.append(curr)
                    curr = prev[curr]
                path.reverse()
                paths[v] = path
        return paths

    def __str__(self):
        lines = ["digraph G {"]
        for src in sorted(self._adj):
            for dest in sorted(self._adj[src]):
                w = self._adj[src][dest]
                lines.append(f'   {src} -> {dest} [label="{w}",weight="{w}"];')
        lines.append("}")
        return "\n".join(lines)

    def test_gsp(self, src, dest):
        dist, path = self.dsp(src, dest)
        if dist != math.inf:
            print(f"Shortest path from {src} to {dest}: length = {dist}, path = {path}")
            print(f"({int(dist)}, {path})")
        else:
            print(f"Vertex {dest} is not accessible from vertex {src}.")
            print(f"({dist}, {path})")



def main():
    G = Graph()
    for v in ["A", "B", "C", "D", "E", "F"]:
        G.add_vertex(v)
    edges = [
        ("A", "B", 2.0), ("A", "F", 9.0), ("B", "F", 6.0), ("B", "D", 15.0),
        ("C", "D", 1.0), ("B", "C", 8.0), ("E", "C", 7.0), ("F", "B", 6.0),
        ("F", "E", 3.0), ("E", "D", 3.0)
    ]
    for src, dest, w in edges:
        G.add_edge(src, dest, w)

    print(G)

    print("Starting BFS with Vertex A")
    for v in G.bfs("A"):
        print (v, end="")
    print()

    print("Starting DFS with Vertex A")
    for v in G.dfs("A"):
        print (v, end="")
    print()

    G.test_gsp("A", "F")

    G.test_gsp("D", "A")

    all_paths = G.dsp_all("A")
    print("Shortest paths from A to all vertices:")
    for dest in sorted(all_paths):
        print("{" + f"{dest}: {all_paths[dest]}" + "}")

if __name__ == "__main__":
    main()
