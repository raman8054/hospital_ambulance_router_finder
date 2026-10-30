# Hospital Ambulance Route Finder — DAA Mini Project

A Python desktop application demonstrating Dijkstra's shortest path algorithm on a sample city road network. It includes six ambulance stations, seven hospitals, and ten road junctions.

## Run on Windows

Double-click **Start Ambulance Route Finder.bat**. The launcher checks for and installs CustomTkinter if needed, then opens the app. You can also install the dependency with `python -m pip install -r requirements.txt` and run `python ambulance_route_finder.py`.

The app uses CustomTkinter for its rounded dark dashboard and the built-in Tkinter Canvas for the map. Keep all three Python files in the same folder. The first launch may need internet access to install CustomTkinter. If Python is not installed, install Python 3 for Windows with Tcl/Tk support.

## Project files

- `ambulance_route_finder.py` — CustomTkinter dashboard, map, controls, and route display
- `dijkstra.py` — shortest-path algorithm and step-by-step trace
- `route_data.py` — locations and weighted road connections
- `requirements.txt` — CustomTkinter dependency

## How it works

Choose an ambulance station and destination hospital. The program finds the minimum estimated travel-time route, highlights it on the network, and lists the algorithm's progress.

- **Algorithm:** Dijkstra's shortest path with a min-heap (`heapq`)
- **Input graph:** Weighted, undirected roads with non-negative estimated travel times
- **Time complexity:** `O((V + E) log V)`
- **Space complexity:** `O(V + E)`
- **Travel times:** Demonstration data only; not live traffic or navigation guidance.
- **Map route colors:** Cyan route outline with a pink fastest-path highlight.
