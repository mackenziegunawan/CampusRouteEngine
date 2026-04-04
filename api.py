# api.py
from fastapi import FastAPI, HTTPException, Query
from route_service import route_by_name

app = FastAPI(title="GT Pathfinder API", version="0.1.0")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/route")
def route(frm: str = Query(..., alias="from"), to: str = Query(..., alias="to")):
    try:
        return route_by_name(frm, to)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    """
    This gives the shortest walking route between two locations.

    Parameters:
    - from: source location (alias or lat/lon)
    - to: destination location

    Returns:
    - distance (meters)
    - estimated time
    - route polyline (list of [lat, lon] points)
    """
