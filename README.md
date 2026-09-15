# Campus Route Engine

A pedestrian routing system for the Georgia Tech campus built with Python, OpenStreetMap data, graph algorithms, and FastAPI.

The project provides two ways to explore shortest-path routing: a custom Dijkstra implementation through the command-line interface and an API-backed routing service over Georgia Tech's real OpenStreetMap pedestrian network.

## Features

- Builds a pedestrian graph of the Georgia Tech campus from **OpenStreetMap**
- Computes shortest walking routes using weighted graph edges
- Includes a **custom implementation of Dijkstra's algorithm**
- Resolves common campus building aliases to geographic coordinates
- Accepts raw latitude/longitude coordinates as routing endpoints
- Estimates route distance and walking time
- Returns route geometry as latitude/longitude points
- Exposes routing functionality through a **FastAPI REST API**
- Caches the OpenStreetMap graph locally to reduce startup time

## Architecture

```text
                         Campus Route Engine
                                  |
                 +----------------+----------------+
                 |                                 |
              CLI Route                         REST API
                 |                                 |
        Custom Dijkstra                    FastAPI /route
                 |                                 |
        Small JSON Graph                    Routing Service
                                                   |
                                      Alias / Coordinate Resolver
                                                   |
                                        Nearest-Node Search
                                          (Haversine)
                                                   |
                                      NetworkX Shortest Path
                                                   |
                                      OpenStreetMap Walk Graph
```

The project contains two routing paths:

1. **CLI routing** uses the custom `Graph` class and Dijkstra implementation in `dijkstra.py`.
2. **API routing** uses an OSMnx/NetworkX pedestrian graph representing the Georgia Tech campus.


## Algorithms & Mathematics

### Shortest-Path Routing

The routing problem is modeled as a weighted graph

$$
G = (V, E)
$$

where each vertex $\(v \in V\)$ represents a point in the pedestrian network and each edge $\(e \in E\)$ represents a walkable connection. Edge weights correspond to physical distance in meters.

The custom routing implementation uses **Dijkstra's algorithm**. For an edge from $\(u\)$ to $\(v\)$ with weight $\(w(u,v)\)$, the relaxation step is:

$$
d(v) = \min\left(d(v),\ d(u) + w(u,v)\right)
$$

where $\(d(v)\)$ is the shortest currently known distance from the source to vertex \(v\).

A binary min-heap is used as the priority queue, giving a time complexity of approximately

$$
O((|V| + |E|)\log |V|)
$$

for the adjacency-list representation.

### Geographic Distance

Before a route can be calculated, an arbitrary latitude/longitude location must be mapped to the nearest node in the pedestrian graph.

Because the graph is stored in geographic coordinates, the engine computes great-circle distance using the **Haversine formula**:

$$
a =
\sin^2\left(\frac{\Delta\phi}{2}\right)
+
\cos(\phi_1)\cos(\phi_2)
\sin^2\left(\frac{\Delta\lambda}{2}\right)
$$

$$
d =
2R\arcsin(\sqrt{a})
$$

where:

- \(\phi_1,\phi_2\) are the two latitudes in radians
- \(\Delta\phi\) is the difference in latitude
- \(\Delta\lambda\) is the difference in longitude
- \(R = 6{,}371{,}000\text{ m}\) is the Earth's approximate mean radius

The engine evaluates this distance against graph nodes and selects

$$
v^* = \arg\min_{v \in V} d(p,v)
$$

where \(p\) is the requested geographic position.

### Walking-Time Estimation

After computing the route distance, estimated walking time is calculated using

$$
t = \frac{d}{v}
$$

with an assumed walking speed of

$$
v = 1.3\text{ m/s}.
$$

The API converts the resulting time from seconds to minutes.

## Custom Dijkstra Implementation

`dijkstra.py` implements Dijkstra's shortest-path algorithm using an adjacency-list graph representation and Python's `heapq` priority queue.

For each node, the algorithm maintains:

- the current shortest known distance from the source
- the previous node on the shortest path
- a priority queue of candidate nodes
- a visited set to avoid reprocessing finalized nodes

When the destination is reached, the predecessor map is traversed backward to reconstruct the route.

For a graph with `V` vertices and `E` edges, the heap-based implementation runs in approximately:

```text
O((V + E) log V)
```

## OpenStreetMap Routing

The API uses **OSMnx** to download Georgia Tech's pedestrian network:

```python
ox.graph_from_place(
    "Georgia Institute of Technology, Atlanta, GA",
    network_type="walk"
)
```

Intersections and other network points are represented as nodes, while walkable connections are represented as weighted edges whose `length` attribute stores distance in meters.

The graph is saved locally as:

```text
data/gt.graphml
```

Subsequent runs load the cached graph rather than downloading and rebuilding it.

## Location Resolution

Routes can be requested using either a campus alias or geographic coordinates.

For example:

```text
CULC
Klaus
33.7756,-84.3963
```

Aliases are stored in `aliases.json`.

Before routing, a location is converted to the nearest node in the pedestrian graph. The nearest node is found using the **Haversine distance**, which measures geographic distance between latitude/longitude coordinates.

This implementation performs the search directly in Python and does not require SciPy.

## REST API

The routing service is exposed through **FastAPI**.

Start the server with:

```bash
uvicorn api:app --reload
```

Check that the service is running:

```http
GET /health
```

Response:

```json
{
  "ok": true
}
```

### Request a Route

```http
GET /route?from=CULC&to=Klaus
```

Both `from` and `to` may be aliases defined in `aliases.json` or coordinates in `lat,lon` format.

A successful response contains:

```json
{
  "distance_m": 850.4,
  "eta_min": 10.9,
  "nodes": [],
  "polyline": [],
  "meta": {
    "algorithm": "networkx.shortest_path",
    "weight": "length"
  }
}
```

`distance_m` represents the route distance in meters, while `eta_min` estimates walking time using a walking speed of **1.3 meters per second**.

The `polyline` contains the latitude/longitude coordinates of the route and can be consumed by a mapping frontend.

## Command-Line Interface

The CLI demonstrates shortest-path routing using the project's custom Dijkstra implementation.

```bash
python cli.py CULC Klaus
```

A custom graph file can also be provided:

```bash
python cli.py CULC Klaus --graph data/gt_graph.json
```

Example output:

```text
Start: CULC
Goal: Klaus
Path: CULC -> ... -> Klaus
Total distance: ... m
```

## Project Structure

```text
campus-route-engine/
├── api.py              # FastAPI REST endpoints
├── route_service.py    # OSM routing and location resolution
├── dijkstra.py         # Custom Dijkstra implementation
├── graph_build.py      # OSMnx graph creation and caching
├── cli.py              # Command-line interface
├── aliases.json        # Campus location aliases
├── data/               # Cached and local graph data
└── README.md
```

## Technical Decisions

### Why OpenStreetMap?

OpenStreetMap provides real pedestrian network data, allowing routes to follow actual campus walkways rather than straight-line distances between buildings.

### Why Haversine Distance?

The graph remains in latitude/longitude coordinates rather than being projected into a planar coordinate system. Haversine distance therefore provides a simple way to locate the graph node geographically closest to an arbitrary coordinate.

### Why Cache the Graph?

Downloading and constructing the campus network on every startup would add unnecessary latency. The generated graph is therefore stored as GraphML and reused on subsequent runs.

## Future Improvements

- Replace the linear nearest-node scan with a spatial index
- Add **A\*** routing and compare its performance with Dijkstra's algorithm
- Support accessibility-aware routing
- Account for temporary walkway closures
- Add configurable walking speeds
- Build an interactive map frontend using the returned route geometry
- Add automated tests and routing benchmarks

## Tech Stack

**Python · FastAPI · NetworkX · OSMnx · OpenStreetMap · GraphML**
