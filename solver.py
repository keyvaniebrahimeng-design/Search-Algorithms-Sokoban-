from collections import deque
import heapq


MOVES = [
    (0,-1),
    (0,1),
    (-1,0),
    (1,0)
]


def move(player, boxes, move, walls):

    dx,dy = move
    new = (player[0]+dx, player[1]+dy)

    if new in walls:
        return None

    boxes = set(boxes)
    pushed = False

    if new in boxes:

        new_box = (new[0]+dx, new[1]+dy)

        if new_box in walls or new_box in boxes:
            return None

        boxes.remove(new)
        boxes.add(new_box)

        pushed = True

    new_state = (new, tuple(sorted(boxes)))

    return new_state, pushed


def goal(boxes, goals):
    return set(boxes) == goals




def solve_bfs(player, boxes, walls, goals):

    start = (player, tuple(sorted(boxes)))

    q = deque([(start, [])])

    visited = set()
    expanded = 0

    while q:

        (player,boxes), path = q.popleft()

        if goal(boxes,goals):
            return path, expanded

        if (player,boxes) in visited:
            continue

        visited.add((player,boxes))
        expanded += 1

        for m in MOVES:

            result = move(player, boxes, m, walls)

            if result:

                nxt, pushed = result

                q.append((nxt, path+[m]))

    return None, expanded



def solve_ucs(player, boxes, walls, goals):

    start = (player, tuple(sorted(boxes)))

    pq = []
    heapq.heappush(pq,(0,start,[]))

    best_cost = {}

    expanded = 0

    while pq:

        cost,(player,boxes),path = heapq.heappop(pq)

        state = (player,boxes)

        if state in best_cost and best_cost[state] <= cost:
            continue

        best_cost[state] = cost

        if goal(boxes,goals):
            return path, expanded

        expanded += 1

        for m in MOVES:

            result = move(player, boxes, m, walls)

            if result:

                nxt, pushed = result

                step_cost = 5 if pushed else 1

                heapq.heappush(
                    pq,
                    (
                        cost + step_cost,
                        nxt,
                        path+[m]
                    )
                )

    return None, expanded




def dfs(state, depth, walls, goals, visited, expanded):

    player,boxes = state

    if goal(boxes,goals):
        return [], expanded

    if depth == 0:
        return None, expanded

    visited.add(state)

    for m in MOVES:

        result = move(player, boxes, m, walls)

        if result:

            nxt, pushed = result

            if nxt not in visited:

                res, expanded = dfs(
                    nxt,
                    depth-1,
                    walls,
                    goals,
                    visited,
                    expanded+1
                )

                if res is not None:
                    return [m]+res, expanded

    return None, expanded


def solve_ids(player, boxes, walls, goals):

    start = (player, tuple(sorted(boxes)))

    depth = 1

    while True:

        visited = set()

        result, expanded = dfs(
            start,
            depth,
            walls,
            goals,
            visited,
            0
        )

        if result is not None:
            return result, expanded

        depth += 1







def reachable_positions(player, boxes, walls):

    blocked = set(boxes) | set(walls)

    q = deque([player])

    visited = {player}

    while q:

        x, y = q.popleft()

        for dx, dy in MOVES:

            nx, ny = x + dx, y + dy

            np = (nx, ny)

            if np in blocked:
                continue

            if np in visited:
                continue

            visited.add(np)

            q.append(np)

    return visited




def heuristic(boxes, goals):

    total = 0

    remaining_goals = set(goals)

    for box in boxes:

        best_goal = None
        best_dist = float('inf')

        for goal_pos in remaining_goals:

            dist = abs(box[0] - goal_pos[0]) + abs(box[1] - goal_pos[1])

            if dist < best_dist:
                best_dist = dist
                best_goal = goal_pos

        total += best_dist

        if best_goal:
            remaining_goals.remove(best_goal)

    return total



def is_deadlock(box, boxes, walls, goals):

    if box in goals:
        return False

    x, y = box

    up = (x, y - 1)
    down = (x, y + 1)
    left = (x - 1, y)
    right = (x + 1, y)

  

    if up in walls and left in walls:
        return True

    if up in walls and right in walls:
        return True

    if down in walls and left in walls:
        return True

    if down in walls and right in walls:
        return True

    

    if up in walls and left in boxes:
        return True

    if up in walls and right in boxes:
        return True

    if down in walls and left in boxes:
        return True

    if down in walls and right in boxes:
        return True

    if left in walls and up in boxes:
        return True

    if right in walls and up in boxes:
        return True

    if left in walls and down in boxes:
        return True

    if right in walls and down in boxes:
        return True

    return False


def has_deadlock(boxes, walls, goals):

    box_set = set(boxes)

    for b in box_set:

        if is_deadlock(b, box_set, walls, goals):
            return True

    return False




def solve_astar(player, boxes, walls, goals):

    start = (player, tuple(sorted(boxes)))

    pq = []

    start_h = heuristic(boxes, goals)

    heapq.heappush(
        pq,
        (
            start_h,
            0,
            start,
            []
        )
    )

    best_cost = {}

    expanded = 0

    while pq:

        f, g, (player, boxes), path = heapq.heappop(pq)

        state = (player, boxes)

        if state in best_cost and best_cost[state] <= g:
            continue

        best_cost[state] = g

      
        if goal(boxes, goals):
            return path, expanded

        expanded += 1

        for m in MOVES:

            result = move(player, boxes, m, walls)

            if not result:
                continue

            nxt, pushed = result

            new_player, new_boxes = nxt

           
            if has_deadlock(new_boxes, walls, goals):
                continue

            move_cost = 2 if pushed else 1

            new_g = g + move_cost

            h = heuristic(new_boxes, goals)

            new_f = new_g + h

            next_state = (
                new_player,
                tuple(sorted(new_boxes))
            )

            if next_state in best_cost and best_cost[next_state] <= new_g:
                continue

            heapq.heappush(
                pq,
                (
                    new_f,
                    new_g,
                    next_state,
                    path + [m]
                )
            )

    return None, expanded



