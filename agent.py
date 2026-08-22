# agent.py
from collections import deque
import heapq

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

class SearchAgent:
    def __init__(self):
        self.actions = ['Up', 'Down', 'Left', 'Right']
        
        # Search plan
        self.plan = []

        # Active search algorithm
        self.active_algo = 'BFS'

    def get_neighbors(self, state, grid_size, walls):
        """
        Return all valid neighboring states.

        state: (x, y)
        """
        x, y = state
        width, height = grid_size

        neighbors = []

        moves = {
            'Up': (0, 1),
            'Down': (0, -1),
            'Left': (-1, 0),
            'Right': (1, 0)
        }

        for action, (dx, dy) in moves.items():
            nx = x + dx
            ny = y + dy

            # Check grid boundaries
            if 0 <= nx < width and 0 <= ny < height:
                # Check walls
                if (nx, ny) not in walls:
                    neighbors.append(((nx, ny), action))

        return neighbors

#BFS
def bfs_search(self, start, goal, grid_size, walls):
        """
        Breadth-First Search using a FIFO queue.
        """

        queue = deque()
        queue.append((start, []))

        reached = {start}

        while queue:
            state, path = queue.popleft()

            if state == goal:
                return path

            for next_state, action in self.get_neighbors(
                    state, grid_size, walls):

                if next_state not in reached:
                    reached.add(next_state)

                    new_path = path + [action]
                    queue.append((next_state, new_path))
                    
        return None

#DFS
def dfs_search(self, start, goal, grid_size, walls):
        """
        Depth-First Search using a LIFO stack.
        """

        stack = []
        stack.append((start, []))

        reached = {start}

        while stack:
            state, path = stack.pop()

            if state == goal:
                return path

            for next_state, action in self.get_neighbors(
                    state, grid_size, walls):

                if next_state not in reached:
                    reached.add(next_state)

                    new_path = path + [action]
                    stack.append((next_state, new_path))
                    
            return None

#UCS
 def ucs_search(self, start, goal, grid_size, walls):
        """
        Uniform-Cost Search using a priority queue.
        Priority is the total path cost g(n).
        """

        priority_queue = []

        # (cost, state, path)
        heapq.heappush(priority_queue, (0, start, []))

        reached = {start: 0}

        while priority_queue:
            cost, state, path = heapq.heappop(priority_queue)

            if state == goal:
                return path

            # Ignore outdated queue entries
            if cost > reached[state]:
                continue

            for next_state, action in self.get_neighbors(
                    state, grid_size, walls):

                step_cost = 1
                new_cost = cost + step_cost

                if (next_state not in reached or
                        new_cost < reached[next_state]):

                    reached[next_state] = new_cost

                    new_path = path + [action]

                    heapq.heappush(
                        priority_queue,
                        (new_cost, next_state, new_path)
                    )

        return None

#method to find the closest food
def find_closest_food(self, start, food_positions):
    if not food_positions:
        return None

    return min(
        food_positions,
        key=lambda food:
            abs(food[0] - start[0]) +
            abs(food[1] - start[1])
    )

def sense_and_act(self, percept):

    # If there is no existing plan, create a new one
    if not self.plan:

        start = percept['agent_pos']
        all_food = percept['all_food']
        grid_size = percept['grid_size']
        walls = set(tuple(wall) for wall in percept['walls'])

        # If there is no food left
        if not all_food:
            return 'Stay'

        # Find the closest food pellet
        goal = self.find_closest_food(start, all_food)

        # Execute the selected search algorithm
        if self.active_algo == 'BFS':
            self.plan = self.bfs_search(
                start,
                goal,
                grid_size,
                walls
            )

        elif self.active_algo == 'DFS':
            self.plan = self.dfs_search(
                start,
                goal,
                grid_size,
                walls
            )

        elif self.active_algo == 'UCS':
            self.plan = self.ucs_search(
                start,
                goal,
                grid_size,
                walls
            )

        # Search could not find a path
        if self.plan is None:
            self.plan = []
            return 'Right'

    # Execute the first action in the plan
    return self.plan.pop(0)
