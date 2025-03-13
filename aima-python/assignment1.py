from time import time
from search import *
from assignment1aux import *

def read_initial_state_from_file(filename):
    # Task 1
    # Return an initial state constructed using a configuration in a file.
    # Replace the line below with your code.
     with open(filename, 'r') as file:
        height = int(file.readline())
        width = int(file.readline())
        gameMap = [[''] * width for _ in range(height)]
        rocks = []
        for line in file:
            rocks.append(tuple(map(int, line.split(','))))
        for rock in rocks:
            gameMap[rock[0]][rock[1]] = 'rock'
        return tuple(tuple(row) for row in gameMap), None, None

class ZenPuzzleGarden(Problem):
    def __init__(self, initial):
        if type(initial) is str:
            super().__init__(read_initial_state_from_file(initial))
        else:
            super().__init__(initial)

    def actions(self, state):
        map = state[0]
        position = state[1]
        direction = state[2]
        height = len(map)
        width = len(map[0])
        action_list = []
        if position:
            if direction in ['up', 'down']:
                if position[1] == 0 or not map[position[0]][position[1] - 1]:
                    action_list.append((position, 'left'))
                if position[1] == width - 1 or not map[position[0]][position[1] + 1]:
                    action_list.append((position, 'right'))
            if direction in ['left', 'right']:
                if position[0] == 0 or not map[position[0] - 1][position[1]]:
                    action_list.append((position, 'up'))
                if position[0] == height - 1 or not map[position[0] + 1][position[1]]:
                    action_list.append((position, 'down'))
        else:
            for i in range(height):
                if not map[i][0]:
                    action_list.append(((i, 0), 'right'))
                if not map[i][width - 1]:
                    action_list.append(((i, width - 1), 'left'))
            for i in range(width):
                if not map[0][i]:
                    action_list.append(((0, i), 'down'))
                if not map[height - 1][i]:
                    action_list.append(((height - 1, i), 'up'))
        return action_list

    def result(self, state, action):
        map = [list(row) for row in state[0]]
        position = action[0]
        direction = action[1]
        height = len(map)
        width = len(map[0])
        while True:
            row_i = position[0]
            column_i = position[1]
            if direction == 'left':
                new_position = (row_i, column_i - 1)
            if direction == 'up':
                new_position = (row_i - 1, column_i)
            if direction == 'right':
                new_position = (row_i, column_i + 1)
            if direction == 'down':
                new_position = (row_i + 1, column_i)
            if new_position[0] < 0 or new_position[0] >= height or new_position[1] < 0 or new_position[1] >= width:
                map[row_i][column_i] = direction
                return tuple(tuple(row) for row in map), None, None
            if map[new_position[0]][new_position[1]]:
                return tuple(tuple(row) for row in map), position, direction
            map[row_i][column_i] = direction
            position = new_position

    def goal_test(self, state):
        # Task 2
        # Return a boolean value indicating if a given state is solved.
        # Replace the line below with your code.
        map = state[0]
        height = len(map)
        width = len(map[0])
        for i in range(height):
            for j in range(width):
                if not map[i][j]:
                    return False
        return True

    

# Task 3
# Implement an A* heuristic cost function and assign it to the variable below.
astar_heuristic_cost = lambda node: sum(
    min(
        abs(rock[0] - rock_position[0]) + abs(rock[1] - rock_position[1])
        for rock in [
            (i, j)
            for i in range(len(node.state[0]))
            for j in range(len(node.state[0][0]))
            if node.state[0][i][j] == 'rock'
        ]
    )
    for rock_position in [
        (i, j)
        for i in range(len(node.state[0]))
        for j in range(len(node.state[0][0]))
        if node.state[0][i][j] == 'rock'
    ]
)
    

def beam_search(problem, f, beam_width):
    # Task 4
    # Implement a beam-width version A* search.
    # Return a search node containing a solved state.
    # Experiment with the beam width in the test code to find a solution.
    # Replace the line below with your code.
    node = Node(problem.initial)
    frontier = [node]
    while frontier:
        new_frontier = []
        for node in frontier:
            for action in problem.actions(node.state):
                child = node.child_node(problem, action)
                if problem.goal_test(child.state):
                    return child
                new_frontier.append(child)
        new_frontier.sort(key=f)
        frontier = new_frontier[:beam_width]
    return None

if __name__ == "__main__":

    # Task 1 test code
    
    print('The loaded initial state is visualised below.')
    visualise(read_initial_state_from_file('assignment1config.txt'))
    

    # Task 2 test code
    
    garden = ZenPuzzleGarden('assignment1config.txt')
    print('Running breadth-first graph search.')
    before_time = time()
    node = breadth_first_graph_search(garden)
    after_time = time()
    print(f'Breadth-first graph search took {after_time - before_time} seconds.')
    if node:
        print(f'Its solution with a cost of {node.path_cost} is animated below.')
        animate(node)
    else:
        print('No solution was found.')
    

    # Task 3 test code
    print('Running A* search.')
    before_time = time()
    node = astar_search(garden, astar_heuristic_cost)
    after_time = time()
    print(f'A* search took {after_time - before_time} seconds.')
    if node:
        print(f'Its solution with a cost of {node.path_cost} is animated below.')
        animate(node)
    else:
        print('No solution was found.')

    # Task 4 test code
    
    print('Running beam search.')
    before_time = time()
    node = beam_search(garden, lambda n: n.path_cost + astar_heuristic_cost(n), 50)
    after_time = time()
    print(f'Beam search took {after_time - before_time} seconds.')
    if node:
        print(f'Its solution with a cost of {node.path_cost} is animated below.')
        animate(node)
    else:
        print('No solution was found.')
    
