import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

def display_grid(grid, nb):
    fig, ax = plt.subplots()
    ax.set_xticks(range(len(grid[0]) + 1))
    ax.set_yticks(range(len(grid) + 1))
    ax.grid(True)

    colors = plt.cm.get_cmap('tab20', nb + 1)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != 0:
                if grid[i][j] == nb+1:
                    ax.add_patch(plt.Rectangle((j, len(grid) - i - 1), 1, 1, color='black'))
                else:  
                    ax.add_patch(plt.Rectangle((j, len(grid) - i - 1), 1, 1, color=colors(grid[i][j] - 1)))

    
    legend_elements = []
    for block_id in range(1, nb + 1):
        legend_elements.append(plt.Line2D([0], [0], color=colors(block_id - 1), lw=4, label=f'Block {block_id}'))
    legend_elements.append(plt.Line2D([0], [0], color='black', lw=4, label='Cut-out'))

    ax.legend(handles=legend_elements, loc='upper right', title="Legend")

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def can_place(grid, block, row, col):
    for i in range(len(block)):
        for j in range(len(block[i])):
            if block[i][j] == 1:
                if row + i >= len(grid) or col + j >= len(grid[0]) or grid[row + i][col + j] != 0:
                    return False
    return True

def place(grid, block, row, col, block_id):
    for i in range(len(block)):
        for j in range(len(block[i])):
            if block[i][j] == 1:
                grid[row + i][col + j] = block_id

def remove(grid, block, row, col):
    for i in range(len(block)):
        for j in range(len(block[i])):
            if block[i][j] == 1:
                grid[row + i][col + j] = 0

def get_rots(block):
    rotations = [block]
    for _ in range(3):  
        block = [list(row) for row in zip(*block[::-1])]
        rotations.append(block)
    return rotations

def adj_checker(grid, row, col, adj, block, block_id, len_blocks):
    ab = set(range(1, len_blocks+1))
    inverted_adj = [x for x in ab if x not in adj]
    inverted_adj = [x for x in inverted_adj if x <= block_id]

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for i in range(len(block)):
        for j in range(len(block[0])):
            if block[i][j] == 1:
                for rd, cd in directions:
                    if 0 <= row + i + rd < len(grid) and 0 <= col + j + cd < len(grid[0]) and grid[row + i + rd][col + j + cd] in adj and grid[row + i + rd][col + j + cd] not in inverted_adj:
                        return False
                    
    return True
                
                
# def solve(grid, blocks, adj, block_index=0):
#     if block_index == len(blocks):

#         return True

#     block_id = block_index + 1
#     block = blocks[block_index]

#     for rot in get_rots(block):
#         for row in range(len(grid)):
#             for col in range(len(grid[0])):
#                 if can_place(grid, rot, row, col):
#                     if block_id in adj:
#                         req_blocks = adj[block_id]
#                         if not adj_checker(grid, row, col, req_blocks, rot, block_id, len(blocks)):
#                             continue
#                     place(grid, rot, row, col, block_id)
#                     if solve(grid, blocks, adj, block_index + 1):
#                         return True
#                     remove(grid, rot, row, col)
#     return False                        

def solve(grid, blocks, adj):
    from copy import deepcopy

    nb = len(blocks)
    stack = []
    stack.append((deepcopy(grid), 0))

    while stack:
        current_grid, block_index = stack.pop()

        if block_index == nb:
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    grid[i][j] = current_grid[i][j]
            return True

        block_id = block_index + 1
        block = blocks[block_index]

        placed = False
        for rot in get_rots(block):
            for row in range(len(current_grid)):
                for col in range(len(current_grid[0])):
                    if can_place(current_grid, rot, row, col):
                        if block_id in adj:
                            req_blocks = adj[block_id]
                            if not adj_checker(current_grid, row, col, req_blocks, rot, block_id, nb):
                                continue
                        next_grid = deepcopy(current_grid)
                        place(next_grid, rot, row, col, block_id)
                        stack.append((next_grid, block_index + 1))
                        placed = True

    return False


def main():
    row = int(input("Enter the number of rows for the grid: "))
    col = int(input("Enter the number of columns for the grid: "))
    grid = [[0 for a in range(col)] for a in range(row)]

    blocks = []
    nb = int(input("Enter the number of blocks: "))
    '''print("\n block input must be in the form of the smallest rectangle containing the block - so a T shaped block would be [[1 1 1], [0 1 0]].\n add 1s where the block exists, and 0 where it doesnt.\n")
    for b in range(nb):
        print(f"\nEnter block {b + 1}:")
        block_rows = int(input("  Number of rows: "))
        block = []
        for r in range(block_rows):
            row_input = input(f"  Enter row {r + 1} (e.g., 1 1 0): ")
            row = [int(x) for x in row_input.split()]
            block.append(row)
        blocks.append(block)'''
    for b in range(nb):
        print(f"\nEnter block {b + 1} details:")
        block_rows = int(input("  Number of rows: "))
        block_cols = int(input("  Number of columns: "))
        block = []
        for r in range(block_rows):
            l=[]
            for c in range(block_cols):
                l.append(1)
            block.append(l)
        blocks.append(block)
    print("L shape is formed by cutting out a rectangle from corner of a rectangle.")
    pos=int(input("Enter 1 for top left corner, 2 for top right, 3 for bottom left, 4 for bottom right corner of grid: "))
    rowc=int(input("Enter number of rows of cut out rectangle: "))
    colc=int(input("Enter number of columns of cut out rectangle: "))
    if pos==1:
        for i in range(rowc):
            for j in range(colc):
                grid[i][j]=nb+1
    elif pos==2:
        for i in range(rowc):
            for j in range(colc):
                grid[i][col-j-1]=nb+1
    elif pos==3:
        for i in range(rowc):
            for j in range(colc):
                grid[row-i-1][j]=nb+1
    elif pos==4:
        for i in range(rowc):
            for j in range(colc):
                grid[row-i-1][col-j-1]=nb+1

    adj = {}
    num_pairs = int(input("\nEnter the number of adjacent pair conditions: "))
    for a in range(num_pairs):
        pair = input("Enter a pair (e.g., 1 2): ")
        block1, block2 = map(int, pair.split())
        if block1 not in adj:
            adj[block1] = []
        if block2 not in adj:
            adj[block2] = []
        adj[block1].append(block2)
        adj[block2].append(block1)

    bl = set(range(1, nb+1))
    for key in adj:
        adj[key] = list(bl-set(adj[key]))
    
    if solve(grid, blocks, adj):
        print("\nSolution found!")
        print(grid)
        display_grid(grid, nb)
    else:
        print("\n failed")

main()