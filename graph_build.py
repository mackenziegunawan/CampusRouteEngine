<<<<<<< HEAD
# graph_build.py  — flat layout, no SciPy needed, keeps lat/lon
from pathlib import Path
from typing import Tuple
import osmnx as ox
import networkx as nx
import math

DATA_DIR = Path("data"); DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_PATH = DATA_DIR / "gt.graphml"

ox.settings.log_console = False
ox.settings.use_cache = True

PLACE = "Georgia Institute of Technology, Atlanta, GA"

def _add_edge_lengths(G: nx.MultiDiGraph) -> nx.MultiDiGraph:
    # OSMnx v1.x vs v2.x compatibility
    if hasattr(ox, "add_edge_lengths"):
        return ox.add_edge_lengths(G)
    else:
        return ox.distance.add_edge_lengths(G)

def load_graph() -> nx.MultiDiGraph:
    """
    Load the GT walking network in **lat/lon** (y=lat, x=lon).
    Do NOT project to meters; keeps nearest-node simple + no SciPy.
    """
    if CACHE_PATH.exists():
        G = ox.load_graphml(CACHE_PATH)
    else:
        G = ox.graph_from_place(PLACE, network_type="walk")
        G = _add_edge_lengths(G)  # edges get 'length' in meters
        # IMPORTANT: do NOT call ox.project_graph(G)!!!!
        ox.save_graphml(G, CACHE_PATH)
    return G


# helpers with no SciPy
def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dlmb/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def nearest_node(G: nx.MultiDiGraph, lat: float, lon: float) -> int:
    """Pure-Python nearest node by haversine (fast enough for campus graphs)."""
    best, best_d = None, float("inf")
    for nid, data in G.nodes(data=True):
        d = haversine_m(lat, lon, data["y"], data["x"])
        if d < best_d:
            best, best_d = nid, d
    return int(best)

def parse_latlon(value: str) -> Tuple[float, float]:
    a, b = value.split(",")
    return float(a.strip()), float(b.strip())
=======
# graph_build.py  — flat layout, no SciPy needed, keeps lat/lon
from pathlib import Path
from typing import Tuple
import osmnx as ox
import networkx as nx
import math

DATA_DIR = Path("data"); DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_PATH = DATA_DIR / "gt.graphml"

ox.settings.log_console = False
ox.settings.use_cache = True

PLACE = "Georgia Institute of Technology, Atlanta, GA"

def _add_edge_lengths(G: nx.MultiDiGraph) -> nx.MultiDiGraph:
    # OSMnx v1.x vs v2.x compatibility
    if hasattr(ox, "add_edge_lengths"):
        return ox.add_edge_lengths(G)
    else:
        return ox.distance.add_edge_lengths(G)

def load_graph() -> nx.MultiDiGraph:
    """
    Load the GT walking network in **lat/lon** (y=lat, x=lon).
    Do NOT project to meters; keeps nearest-node simple + no SciPy.
    """
    if CACHE_PATH.exists():
        G = ox.load_graphml(CACHE_PATH)
    else:
        G = ox.graph_from_place(PLACE, network_type="walk")
        G = _add_edge_lengths(G)  # edges get 'length' in meters
        # IMPORTANT: do NOT call ox.project_graph(G)!!!!
        ox.save_graphml(G, CACHE_PATH)
    return G


# helpers with no SciPy
def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dlmb/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def nearest_node(G: nx.MultiDiGraph, lat: float, lon: float) -> int:
    """Pure-Python nearest node by haversine (fast enough for campus graphs)."""
    best, best_d = None, float("inf")
    for nid, data in G.nodes(data=True):
        d = haversine_m(lat, lon, data["y"], data["x"])
        if d < best_d:
            best, best_d = nid, d
    return int(best)

def parse_latlon(value: str) -> Tuple[float, float]:
    a, b = value.split(",")
    return float(a.strip()), float(b.strip())
>>>>>>> ff90a719a89555165b91e33f65f0775c3e44c032
