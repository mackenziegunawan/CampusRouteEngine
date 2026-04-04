<<<<<<< HEAD
# route_service.py — no SciPy, uses aliases.json, robust name handling
from __future__ import annotations
from pathlib import Path
from typing import Dict, Tuple
import json, math
import networkx as nx

from graph_build import load_graph

ROOT = Path(__file__).resolve().parent
ALIASES_PATH = ROOT / "aliases.json"
WALK_M_PER_S = 1.3

G: nx.MultiDiGraph = load_graph() 


# helpers (no SciPy required)
def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dlmb/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def _nearest_node(lat: float, lon: float) -> int:
    best, best_d = None, float("inf")
    for nid, data in G.nodes(data=True):
        d = _haversine_m(lat, lon, data["y"], data["x"])# y=latitude, x=longitude
        if d < best_d:
            best, best_d = nid, d
    return int(best)

def _parse_latlon(s: str) -> Tuple[float, float]:
    a, b = s.split(",")
    return float(a.strip()), float(b.strip())

def _load_aliases() -> Dict[str, Tuple[float, float]]:
    """Reload aliases.json each request; normalize keys (lowercase, spaces)."""
    try:
        with open(ALIASES_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        norm = {}
        for k, v in raw.items():
            k_norm = k.strip().lower().replace("_", " ")
            norm[k_norm] = tuple(v)
        return norm
    except Exception:
        return {}

def _resolve_to_node(s: str) -> int:
    s = s.strip()

    # 1) coordinates form: "lat,lon"
    if "," in s:
        lat, lon = _parse_latlon(s)
        return _nearest_node(lat, lon)
    
    # 2) alias form (case/underscore insensitive)
    aliases = _load_aliases()
    key = s.lower().replace("_", " ")
    if key in aliases:
        lat, lon = aliases[key]
        return _nearest_node(lat, lon)
    
    # helpful error
    examples = ", ".join(list(k.title() for k in aliases.keys())[:8])
    raise ValueError(f"Unknown place '{s}'. Add to aliases.json or use 'lat,lon'. Known: {examples}")


# -------- public API --------
def route_by_name(frm: str, to: str) -> Dict:
    src = _resolve_to_node(frm)
    dst = _resolve_to_node(to)

    nodes = nx.shortest_path(G, src, dst, weight="length")

    dist = 0.0
    for u, v in zip(nodes[:-1], nodes[1:]):
        edata = G.get_edge_data(u, v)
        edge = edata[min(edata.keys())]
        dist += float(edge.get("length", 0.0))
        
    polyline = [[G.nodes[n]["y"], G.nodes[n]["x"]] for n in nodes]

    return {
        "distance_m": round(dist, 1),
        "eta_min": round(dist / WALK_M_PER_S / 60.0, 1),
        "nodes": nodes,
        "polyline": polyline,
        "meta": {"algorithm": "networkx.shortest_path", "weight": "length"},
    }
=======
# route_service.py — no SciPy, uses aliases.json, robust name handling
from __future__ import annotations
from pathlib import Path
from typing import Dict, Tuple
import json, math
import networkx as nx

from graph_build import load_graph

ROOT = Path(__file__).resolve().parent
ALIASES_PATH = ROOT / "aliases.json"
WALK_M_PER_S = 1.3

G: nx.MultiDiGraph = load_graph() 


# helpers (no SciPy required)
def _haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dlmb/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def _nearest_node(lat: float, lon: float) -> int:
    best, best_d = None, float("inf")
    for nid, data in G.nodes(data=True):
        d = _haversine_m(lat, lon, data["y"], data["x"])# y=latitude, x=longitude
        if d < best_d:
            best, best_d = nid, d
    return int(best)

def _parse_latlon(s: str) -> Tuple[float, float]:
    a, b = s.split(",")
    return float(a.strip()), float(b.strip())

def _load_aliases() -> Dict[str, Tuple[float, float]]:
    """Reload aliases.json each request; normalize keys (lowercase, spaces)."""
    try:
        with open(ALIASES_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        norm = {}
        for k, v in raw.items():
            k_norm = k.strip().lower().replace("_", " ")
            norm[k_norm] = tuple(v)
        return norm
    except Exception:
        return {}

def _resolve_to_node(s: str) -> int:
    s = s.strip()

    # 1) coordinates form: "lat,lon"
    if "," in s:
        lat, lon = _parse_latlon(s)
        return _nearest_node(lat, lon)
    
    # 2) alias form (case/underscore insensitive)
    aliases = _load_aliases()
    key = s.lower().replace("_", " ")
    if key in aliases:
        lat, lon = aliases[key]
        return _nearest_node(lat, lon)
    
    # helpful error
    examples = ", ".join(list(k.title() for k in aliases.keys())[:8])
    raise ValueError(f"Unknown place '{s}'. Add to aliases.json or use 'lat,lon'. Known: {examples}")


# -------- public API --------
def route_by_name(frm: str, to: str) -> Dict:
    src = _resolve_to_node(frm)
    dst = _resolve_to_node(to)

    nodes = nx.shortest_path(G, src, dst, weight="length")

    dist = 0.0
    for u, v in zip(nodes[:-1], nodes[1:]):
        edata = G.get_edge_data(u, v)
        edge = edata[min(edata.keys())]
        dist += float(edge.get("length", 0.0))
        
    polyline = [[G.nodes[n]["y"], G.nodes[n]["x"]] for n in nodes]

    return {
        "distance_m": round(dist, 1),
        "eta_min": round(dist / WALK_M_PER_S / 60.0, 1),
        "nodes": nodes,
        "polyline": polyline,
        "meta": {"algorithm": "networkx.shortest_path", "weight": "length"},
    }
>>>>>>> ff90a719a89555165b91e33f65f0775c3e44c032
