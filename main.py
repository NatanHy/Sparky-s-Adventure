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

    def get(self, index):
        return self.arr[index[0]][index[1]]

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
    weight = get_weight(unvisited_index)

    # Direction travelling from visited node to unvisited node
    direction = get_direction(visited_index, unvisited_index)

    # Iterate over node value pairs
    for i in range(4):
        # Cost of turning towards target node
        start_turn_cost = get_turn_cost(i, direction)

        for j in range(4):
            elm1 = visited_node.values[i]
            elm2 = unvisited_node.values[j]

            # Cost of turning to correct orientation after getting to the node
            end_turn_cost = get_turn_cost(direction, j)

            turn_weight = start_turn_cost + end_turn_cost

            # Update one value at unvisited node
            unvisited_node.values[j] = min(elm2, elm1 + weight + turn_weight)

def dijkstra(grid : Grid, start_index, target_index):
    visited = []     # List of visited nodes
    queue = Queue()  # Queue of nodes to update

    grid.set_start(start_index) # Initialize start_index

    queue.queue(start_index)

    while True:
        index = queue.dequeue()

        # Update values around index
        for adj in grid.get_adjacent(index):
            update(grid, index, adj)

            queue.queue(adj)

        visited.append(index)

        # If target_index is reached, the algorithm is finished
        if index == target_index:
            return

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

