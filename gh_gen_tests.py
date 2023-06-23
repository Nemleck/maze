from gh_generator_classes import Maze
import json

# Maze dimensions (ncols, nrows)
nx, ny = 3, 4
# Maze entry position
ix, iy = 0, 0

maze = Maze(nx, ny, ix, iy)
maze.make_maze()

maze_list = str(maze).replace("|","+").replace("+","-").replace("-","1").replace(" ","0").split("\n")
maze_listII = []
for i in range(len(maze_list)):
    if not "0" in maze_list[i]:
        continue

    maze_listII.append([])

    for letter in maze_list[i]:
        maze_listII[-1].append(int(letter))

with open("maze.json", "w") as f:
    maze_listII[0][0] = 2
    maze_listII[-1][-1] = 3
    f.write(json.dumps(maze_listII).replace("], [","],\n["))

# print(str(maze_listII).replace(", ",",").replace("],[","],\n   [").replace("[[","[\n   [").replace("]]","]\n]").replace("'",""))

import resolverII