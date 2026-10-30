"""Dijkstra shortest-path algorithm for a weighted, undirected road graph."""

import heapq


def dijkstra(start, goal, places, roads):
    """Return (minimum time, route, trace) using a binary min-heap.

    ``places`` is a mapping of location names to their metadata. ``roads`` is
    an iterable of (first location, second location, travel time) tuples.
    All edge weights must be non-negative.
    """
    graph = {name: [] for name in places}
    for first, second, minutes in roads:
        graph[first].append((second, minutes))
        graph[second].append((first, minutes))

    distances = {name: float("inf") for name in places}
    previous, visited = {}, set()
    distances[start] = 0
    queue, steps = [(0, start)], []

    while queue:
        distance, current = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        steps.append(f"Visit {current}: shortest known time is {distance} min.")
        if current == goal:
            break
        for neighbor, weight in graph[current]:
            candidate = distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                previous[neighbor] = current
                heapq.heappush(queue, (candidate, neighbor))
                steps.append(f"Update {neighbor}: {candidate} min via {current}.")

    if distances[goal] == float("inf"):
        return None, [], steps

    route = [goal]
    while route[-1] != start:
        route.append(previous[route[-1]])
    route.reverse()
    return distances[goal], route, steps
