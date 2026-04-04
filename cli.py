import argparse
import json
from dijkstra import Graph

def load_graph(path: str) -> Graph:
    with open(path, "r") as f:
        data = json.load(f)
    return Graph(nodes=data["nodes"], edges=data["edges"], undirected=True)

def main():
    parser = argparse.ArgumentParser(description="Shortest path on a tiny GT campus graph (Dijkstra).")
    parser.add_argument("start", help="Start node (e.g., CULC)")
    parser.add_argument("goal", help="Goal node (e.g., Klaus)")
    parser.add_argument("--graph", default="data/gt_graph.json", help="Path to graph JSON")
    args = parser.parse_args()

    g = load_graph(args.graph)
    distance, path = g.dijkstra(args.start, args.goal)

    print(f"Start: {args.start}\nGoal: {args.goal}")
    print("Path:", " -> ".join(path))
    print(f"Total distance: {distance:.1f} m")

if __name__ == "__main__":
    main()
