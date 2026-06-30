from collections import deque
from heapq import heappush, heappop
from solver import move, is_goal, DIRS


def bfs(start, walls, goals):
    queue = deque([start])
    visited = set()
    expanded = 0

    while queue:
        state = queue.popleft()

        if state in visited:
            continue

        visited.add(state)
        expanded += 1

        if is_goal(state, goals):
            return state.path, expanded

        for d in DIRS:
            nxt = move(state, d, walls)
            if nxt and nxt not in visited:
                queue.append(nxt)

    return None, expanded


def dls(state, walls, goals, depth_limit, visited, expanded):
    if is_goal(state, goals):
        return state.path, expanded, True

    if depth_limit == 0:
        return None, expanded, False

    visited.add(state)
    expanded += 1

    for d in DIRS:
        nxt = move(state, d, walls)
        if nxt and nxt not in visited:
            result, expanded, found = dls(
                nxt, walls, goals, depth_limit - 1, visited.copy(), expanded
            )
            if found:
                return result, expanded, True

    return None, expanded, False


def ids(start, walls, goals, max_depth=60):
    total_expanded = 0

    for depth in range(max_depth + 1):
        result, expanded, found = dls(start, walls, goals, depth, set(), 0)
        total_expanded += expanded
        if found:
            return result, total_expanded

    return None, total_expanded


def ucs(start, walls, goals):
    pq = []
    counter = 0
    heappush(pq, (0, counter, start))
    visited = set()
    expanded = 0

    while pq:
        cost, _, state = heappop(pq)

        if state in visited:
            continue

        visited.add(state)
        expanded += 1

        if is_goal(state, goals):
            return state.path, expanded

        for d in DIRS:
            nxt = move(state, d, walls)
            if nxt and nxt not in visited:
                counter += 1
                heappush(pq, (len(nxt.path), counter, nxt))

    return None, expanded


def heuristic(boxes, goals):
    total = 0
    for bx, by in boxes:
        total += min(abs(bx - gx) + abs(by - gy) for gx, gy in goals)
    return total


def astar(start, walls, goals):
    pq = []
    counter = 0
    heappush(pq, (heuristic(start.boxes, goals), counter, start))
    visited = set()
    expanded = 0

    while pq:
        _, _, state = heappop(pq)

        if state in visited:
            continue

        visited.add(state)
        expanded += 1

        if is_goal(state, goals):
            return state.path, expanded

        for d in DIRS:
            nxt = move(state, d, walls)
            if nxt and nxt not in visited:
                counter += 1
                g = len(nxt.path)
                h = heuristic(nxt.boxes, goals)
                heappush(pq, (g + h, counter, nxt))

    return None, expanded
