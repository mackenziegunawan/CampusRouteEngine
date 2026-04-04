from __future__ import annotations
from typing import Dict, List, Tuple, Optional
import heapq

class Graph:
    def __init__(self, nodes: Dict[str, dict], edges: List[Tuple[str, str, float]], undirected: bool = True):
        self.nodes = nodes
        self.adj: Dict[str, List[Tuple[str, float]]] = {k: [] for k in nodes.keys()}
        for u, v, w in edges:
            self.adj[u].append((v, float(w)))
            if undirected:
                self.adj[v].append((u, float(w)))

    def dijkstra(self, start: str, goal: str) -> Tuple[float, List[str]]:
        if start not in self.adj:
            raise KeyError(f"Unknown start node: {start}")
        if goal not in self.adj:
            raise KeyError(f"Unknown goal node: {goal}")

        dist: Dict[str, float] = {node: float('inf') for node in self.adj}
        prev: Dict[str, Optional[str]] = {node: None for node in self.adj}
        dist[start] = 0.0

        # (distance, node)
        pq: List[Tuple[float, str]] = [(0.0, start)]
        visited = set()

        while pq:
            d, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)
            if u == goal:
                break
            for v, w in self.adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(pq, (nd, v))

        if dist[goal] == float('inf'):
            raise ValueError(f"No path from {start} to {goal}")

        # reconstruct path
        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        return dist[goal], path
