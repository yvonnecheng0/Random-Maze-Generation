""""
Module generates a maze given the width and height desired 
Yvonne Cheng 
csci 112
Winter, 2023
"""

import random
import matplotlib.pyplot as plt

def create_adjacent_pairs(width, height):
    adjacent_pairs = []

    #Add adjacent pairs for horizontal walls
    for y in range(height):
        for x in range(width - 1):
            curr_cell = y * width + x
            adjacent_pairs.append((curr_cell, curr_cell + 1))

    #Add adjacent pairs for vertical walls
    for y in range(height - 1):
        for x in range(width):
            curr_cell = y * width + x
            adjacent_pairs.append((curr_cell, curr_cell + width))

    #Remove walls for entrance and exit
    adjacent_pairs.remove((0, 1))  #Remove top left wall
    adjacent_pairs.remove((width * height - 1 - width, width * height - 1))  #Remove bottom right wall

    return adjacent_pairs

#Find the root of a cell from the parents
def root(cell, parents):
    #Update the parent of the current cell if parent of cell is not None 
    while parents[cell] is not None:
        cell = parents[cell]
    return cell

#Join the two sets of cells in different sets into one set
def join(cell1, cell2, parents, sizes, removed_walls):
    #Initialize roots 
    root1 = root(cell1, parents)
    root2 = root(cell2, parents)

    #If root1 != root2, check which root has a smaller size
    if root1 != root2:
        #If root1 has smaller size than root2, roots are swapped
        if sizes[root1] < sizes[root2]:
            root1, root2 = root2, root1
        #Set parent of root2 = root1, joining the two set 
        parents[root2] = root1
        #Increase size of root1 by size of root2
        sizes[root1] += sizes[root2]
        #Add tuple of (cell1, cell2) to removed_walls
        removed_walls.append((cell1, cell2))

#Loop through the list of walls and eliminate them one by one as we unify cells, in line with the above algorithm
def erase_walls(walls, parents, sizes):
    #Randomly shuffle list of walls
    random.shuffle(walls)
    remaining_walls = []
    removed_walls = []

    #Check if two cells on either side of wall are part of same root
    for wall in walls:
        cell1, cell2 = wall
        #If they are not, join two cells into the same root by removing the wall between them, and add wall to list of removed walls
        if root(cell1, parents) != root(cell2, parents):
            join(cell1, cell2, parents, sizes, removed_walls)
            continue
        
        #Add wall to list of remaining walls
        remaining_walls.append(wall)

    return remaining_walls, removed_walls

def generate_maze(width, height):
    #Create list of all possible adjacent pairs of cells in maze using create_adjacent_pairs function
    walls = create_adjacent_pairs(width, height)

    #Parents dictionary assigns a value of None to each cell in the maze
    parents = {cell: None for cell in range(width * height)}

    #Sizes dictionary assigns a value of 1 to each cell in the maze
    sizes = {cell: 1 for cell in range(width * height)}

    #Set remaining_walls and removed_walls = erase_walls
    remaining_walls, removed_walls = erase_walls(walls, parents, sizes)
    
    return remaining_walls, removed_walls

def position(cell, maze_size):
    #Set rows and cols of maze = maze_size
    nrows, ncols = maze_size

    #calculate row index of cell by integer division on cell index using number of columns in maze
    row = cell // ncols

    #calculate col index of cell by integer division on cell index using number of columns in maze
    col = cell % ncols
    return row, col

def draw_maze(remaining_walls, removed_walls, maze_size):
    #Set rows and cols of maze = maze_size
    nrows, ncols = maze_size

    #Set up figure and axis object
    fig, ax = plt.subplots()

    #Turns off the axis 
    ax.axis('off')

    #Draws the four outer walls of maze 
    plt.plot((0, ncols), (nrows, nrows), linestyle='-', color='black')
    plt.plot((ncols, ncols), (nrows, 0), linestyle='-', color='black')
    plt.plot((ncols, 0), (0, 0), linestyle='-', color='black')
    plt.plot((0, 0), (0, nrows), linestyle='-', color='black')

    #Don't draw top-left and bottom-right walls
    plt.plot((0, 1), (nrows, nrows), linestyle='-', color='white')
    plt.plot((ncols-1, ncols), (0, 0), linestyle='-', color='white')
    
    #Loop through the remaining_walls list
    for wall in remaining_walls:
        #Set up pair of integers in list to wall 
        i, j = wall
        #Calculate position of wall in the maze 
        y1, x1 = position(i, maze_size)
        y2, x2 = position(j, maze_size)

        #Draw wall on plot 
        if abs(x1 - x2) == 1:
            #Vertical wall
            plt.plot((max(x1, x2), max(x1, x2)), (y1, y1 + 1), linestyle='-', color='black')
        elif abs(y1 - y2) == 1:
            #Horizontal wall 
            plt.plot((x1, x1 + 1), (max(y1, y2), max(y1, y2)), linestyle='-', color='black')
    
    #Display maze 
    plt.show()

if __name__ == "__main__":
    maze_size = (40, 40)
    remaining_walls, removed_walls = generate_maze(*maze_size)
    draw_maze(remaining_walls, removed_walls, maze_size)