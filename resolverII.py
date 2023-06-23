from copy import deepcopy
import json
from enum import IntEnum

class Maze(IntEnum):
    GROUND = 0
    WALL = 1
    START = 2
    ARRIVAL = 3

class Analysed(IntEnum):
    NOT_ANALYSED = 0
    ANALYSED = 1

class Solution(IntEnum):
    START_OR_ARRIVAL = 0
    WALL = -1

def show(mazes):
    for maze in mazes:
            text = ""
            for row in range(len(maze)):
                for col in range(len(maze[row])):
                    value = maze[row][col]

                    if value == Solution.WALL: # show analysed walls
                        text += "🟨"
                    elif maze[row][col] == Maze.WALL: # show other walls
                        text += "🟦"
                    elif value == Solution.START_OR_ARRIVAL:
                        text += "🟩"
                    elif type(value) is int and value >= 1:
                        text += f"{value:2}"
                        # text += "⬛"
                    else:
                        text += "🟫"
                text += "\n"

            print(text)

with open("maze.json", "r") as f:
    maze = json.loads(f.read())

empty_maze = [[None for x in range(len(maze[y]))] for y in range(len(maze))]

# init start and end position
start_pos = (0, 0)
end_pos = (4, 4)
for y in range(len(maze)):
    for x in range(len(maze[y])):
        if maze[y][x] == Maze.START:
            start_pos = (x, y)
        elif maze[y][x] == Maze.ARRIVAL:
            end_pos = (x, y)

temp_analysed = deepcopy(empty_maze)
temp_analysed[start_pos[1]][start_pos[0]] = Analysed.ANALYSED

temp_solution = deepcopy(empty_maze)
temp_solution[start_pos[1]][start_pos[0]] = Solution.START_OR_ARRIVAL

curr_solutions = [{
     "place": start_pos,
     "analysed": empty_maze,
     "solution": temp_solution
}]

final_solutions = []

finished = False
while not finished:
    for j in range(len(curr_solutions)):
        sol = curr_solutions[0]
        place = sol["place"]

        # always take the first element of curr_solutions as it's deleted
        for d in [(1,0),(-1,0),(0,1),(0,-1)]: # d means direction - it's to make the name shorter
            new_x = place[0]+d[0]
            new_y = place[1]+d[1]

            if new_y >= 0 and new_y < len(maze) and\
                new_x >= 0 and new_x < len(maze[new_y])\
                and sol["analysed"][place[1]+d[1]][place[0]+d[0]] != 1: # if in the limits of the maze and not a wall

                sol["analysed"][new_y][new_x] = 1 # if never analysed, then make it analysed

                t_sol = deepcopy(sol)
                t_sol["solution"][new_y][new_x] = t_sol["solution"][place[1]][place[0]]+1
                t_sol["place"] = (new_x, new_y)

                if maze[new_y][new_x] == Maze.WALL: #wall ?
                    for elm in curr_solutions:
                        elm["solution"][new_y][new_x] = -1

                elif maze[new_y][new_x] == Maze.GROUND: #path ?
                    curr_solutions.append(t_sol)
                
                elif maze[new_y][new_x] == Maze.ARRIVAL: #goal ?
                    t_sol["solution"][new_y][new_x] = Solution.START_OR_ARRIVAL
                    final_solutions.append(t_sol) # then append the solution to final_solutions

        curr_solutions.pop(0)

        if len(curr_solutions) > 0:
            pass
        else:
            finished = True
    
# show the final solutions
if len(final_solutions) > 0:
    print("All solutions :")

show([elm["solution"] for elm in final_solutions])

best_i = None
best_sol = None
for solution in final_solutions:
    higher = 0
    for y in range(len(solution["solution"])):
        for x in solution["solution"][y]:
            if x and x > higher:
                higher = x
    
    if best_i == None or higher < best_i:
        best_i = higher
        best_sol = solution

if best_sol:
    print(f"best (In {best_i} moves) :")
    show([best_sol["solution"]])
else:
    print("There's no solution")