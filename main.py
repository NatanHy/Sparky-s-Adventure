from math import inf

class Node:
    def __init__(self):
        # Four values representing different orientations
        self.values = [inf, inf, inf, inf]

    # Actual distance to the node
    def min(self):
        return min(self.values)

# n x n grid of Node
class Grid:
    def __init__(self, n):
        self.n = n

        # 2-d array, initialized with Node[inf, inf, inf, inf]
        self.arr = [
            [Node() for _ in range(n)] for _ in range(n)
        ]

    def get(self, index) -> Node:
        return self.arr[index[0]][index[1]]
    
    def get_value(self, index):
        return self.get(index).min()

    def set(self, index, node):
        self.arr[index[0]][index[1]] = node

    # Returns list of index values that are adjacent to index
    def get_adjacent(self, index):
        i, j = index

        res = []

        if i > 0:
            res.append((i - 1, j))
        if j > 0:
            res.append((i    , j - 1))
        if i < self.n - 1:
            res.append((i + 1, j))
        if j < self.n - 1:
            res.append((i    , j + 1))

        return [index for index in res if self.get(index) is not None]
    
    # Only used for printing
    def _max_value(self):
        res = 0

        for row in self.arr:
            for node in row: 
                if node is not None:
                    res = max(res, node.min())

        return res

    def print(self):
        str_len = len(str(self._max_value()))

        for row in self.arr:
            for node in row:
                if node is None:
                    # " " * str_len adds padding to align numbers
                    print("x", end=" " * str_len)
                else:
                    val = node.min()
                    print(val, end=" " * (str_len - len(str(val)) + 1))
            print("")

    # Used to set the node at the start to [0, 0, 0, 0]
    def set_start(self, index):
        i, j = index

        self.arr[i][j].values = [0, 0, 0, 0]

class Queue:
    def __init__(self):
        self.arr = []

    def queue(self, elm):
        self.arr.append(elm)

    def dequeue(self):
        return self.arr.pop(0)
    
    def len(self):
        return len(self.arr)

# Calculate weight at given index (1 at odd sums, 2 at even sums)
def get_weight(index):
    i, j = index

    return 2 - (i + j) % 2

# Calculate cost of turning from dir1 to dir2
def get_turn_cost(dir1, dir2):
    if dir1 == dir2:
        return 0
    if (dir1 + dir2) % 2 == 1:
        return 1
    return 2

# Calculate direction that travels from index1 to index2
def get_direction(index1, index2):
    d_i = index1[0] - index2[0]
    d_j = index1[1] - index2[1]

    if d_i == 1:
        return 0
    if d_i == -1:
        return 2
    if d_j == 1:
        return 3
    if d_j == -1:
        return 1

# Update values of Node at unvisited_index based on values of Node at visited_index
def update(grid : Grid, visited_index, unvisited_index):
    # Fetch nodes
    visited_node = grid.get(visited_index)
    unvisited_node = grid.get(unvisited_index)

    # Vertex weight based on even/odd index
    current_weight = get_weight(visited_index)
    weight = get_weight(unvisited_index)

    # Direction travelling from visited node to unvisited node
    direction = get_direction(visited_index, unvisited_index)

    # Iterate over node value pairs
    for i in range(4):
        # Cost of turning towards target node
        start_turn_cost = current_weight * get_turn_cost(i, direction)

        for j in range(4):
            elm1 = visited_node.values[i]
            elm2 = unvisited_node.values[j]

            # Cost of turning to correct orientation after getting to the node
            end_turn_cost = weight * get_turn_cost(direction, j)

            turn_weight = start_turn_cost + end_turn_cost

            # Update one value at unvisited node
            unvisited_node.values[j] = min(elm2, elm1 + weight + turn_weight)

def dijkstra(grid : Grid, start_index, target_index):
    queue = Queue()  # Queue of nodes to update

    grid.set_start(start_index) # Initialize start_index

    queue.queue(start_index)

    while True:
        index = queue.dequeue()

        # Update values around index
        for adj in grid.get_adjacent(index):
            update(grid, index, adj)

            queue.queue(adj)

        # If target_index is reached, the algorithm is finished
        if index == target_index:
            return
        
# Finds all possible minimum-length paths
def find_possible_paths(grid : Grid, start_index, target_index):
    possible_paths = []

    # Builds paths backwards from target_index
    path_builder = Queue()

    path_builder.queue([target_index])
    
    while path_builder.len() > 0:
        current_path = path_builder.dequeue()

        current_index = current_path[-1]

        # Sort adjecent indicies of current_index based on distance to start
        # (Horrendous one-liner, I know)
        indicies = sorted(grid.get_adjacent(current_index), key=lambda x: grid.get_value(x))

        min_dist = grid.get_value(indicies[0])

        # Iterate over all indicies
        for index in indicies:
            if index == start_index: # Path finished
                path = current_path + [index]
                directions = as_directions(path[::-1])
                possible_paths.append(directions)
            
            # Continue building path for all minimum-distance indicies
            elif grid.get_value(index) == min_dist:
                path_builder.queue(current_path + [index])

    return possible_paths

# Calculates number of turns in a path
# Path has to be expressed as directions e.g ["left", "right", "right", "up"]
def num_of_turns(path):
    current_direction = path[0]
    turns = 0

    for direction in path:
        if direction != current_direction:
            turns += 1
            current_direction = direction

    return turns

# Find path with least number of turns
def find_minimal_turn_path(grid : Grid, start_index, target_index):
    possible_paths = find_possible_paths(grid, start_index, target_index)

    return sorted(possible_paths, key=lambda x: num_of_turns(x))[0]

# Translate path of indicies to path of directions
# For example: [(0, 0), (0, 1), (1, 1)] -> ["right", "down"]
def as_directions(index_path):
    res = []

    directions = ["up", "right", "down", "left"]

    for i in range(len(index_path) - 1):
        index1 = index_path[i]
        index2 = index_path[i + 1]

        d = get_direction(index1, index2)

        res.append(directions[d])

    return res

if __name__ == "__main__":
    # Example
    
    grid = Grid(5)

    grid.set((1, 0), None)
    grid.set((1, 1), None)

    grid.set((3, 4), None)
    grid.set((3, 3), None)
    grid.set((3, 2), None)

    dijkstra(grid, (0, 0), (4, 4))

    grid.print()

    p = find_minimal_turn_path(grid, (0, 0), (4, 4))
