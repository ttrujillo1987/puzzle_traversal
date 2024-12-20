import tkinter as tk
from tkinter import ttk
import heapq

current_stage = "select_source"

source = ("", "")
destination = ("", "")

board = [["-","-","-","-","-","-","-","-","-","-"],
        ["-","-","-","-","-","-","-","-","-","-"],
        ["-","-","-","-","-","-","-","-","-","-"],
        ["-","-","-","-","-","-","-","-","-","-"],
        ["-","-","-","-","-","-","-","-","-","-"],
        ["-","-","-","-","-","-","-","-","-","-"],
        ["-","-","-","-","-","-","-","-","-","-"],
        ["-","-","-","-","-","-","-","-","-","-"],
        ["-","-","-","-","-","-","-","-","-","-"],
        ["-","-","-","-","-","-","-","-","-","-"]]

def on_click(row, col):
    global current_stage, source, destination, board
    if current_stage == "select_source":
        grid_colors[row][col] = 'green' if grid_colors[row][col] == 'white' else 'white'
        canvas.itemconfig(grid_rects[row][col], fill=grid_colors[row][col])
        source = (row, col)
        current_stage = "select_destination"
        instructions_string.set('Now, select a destination. This is cell where the traversal will end.')
    elif current_stage == "select_destination" and (row, col) != source:
        grid_colors[row][col] = 'blue' if grid_colors[row][col] == 'white' else 'white'
        canvas.itemconfig(grid_rects[row][col], fill=grid_colors[row][col])
        destination = (row, col)
        current_stage = "select_barriers"
        instructions_string.set("Finally, select barriers. These cells cannot be traveled through on the way from the source to the destination. Select as many as you like. Once you are finished selecting barriers, click 'Find Path'")
    elif current_stage == "select_barriers" and (row, col) != source and (row, col) != destination:
        grid_colors[row][col] = 'black' if grid_colors[row][col] == 'white' else 'white'
        canvas.itemconfig(grid_rects[row][col], fill=grid_colors[row][col])
        board[row][col] = "#" if board[row][col] == "-" else '-'

def solve_puzzle():
    """Finds the shortest path in a puzzle sized MxN. Each cell in the puzzle is either open or has a barrier (denoted
    with '-' and '#' respectively). The path can only travel through open cells and not cells with barriers. Function
    returns the nodes the optimal path travels through as well as a string with the directions taken in the path."""

    paths = []                              # Create a priority queue for storing the paths from Source to Destination
    visited = []
    directions = [(1, 0, "D"), (0, 1, "R"), (-1, 0, "U"), (0, -1, "L")]

    dest_row, dest_col = (destination)
    source_row, source_col = (source)

    heapq.heappush(paths, (0, (source_row, source_col), "", []))    # Initialize the source

    if source == destination:
        instructions_string.set(f"Path: {destination}")

    while len(paths) > 0:
        greedy_choice = heapq.heappop(paths)        # Pop the closest node to the destination node in the priority queue
        distance, source_node, current_path_string, current_path = greedy_choice
        source_row, source_col = source_node

        if len(paths) > 0:      # If next two nodes have same priority, make sure they are processed consecutively
            match_check = paths[0]
            match_check = match_check[0]
            if match_check == distance:
                distance_match = heapq.heappop(paths)
                priority, match_node, match_path_string, math_path = distance_match
                heapq.heappush(paths, (0, match_node, match_path_string, math_path))

        if source_node in visited:                  # If this node has a barrier or has been processed skip it
            continue

        for direction in directions:                                # Check all neighboring nodes
            row_direction, col_direction, string_direction = direction
            neighbor_row = source_row + row_direction
            neighbor_col = source_col + col_direction

            if 0 <= neighbor_row < len(board) and 0 <= neighbor_col < len(board[0]):  # If neighbor is in graph

                if board[neighbor_row][neighbor_col] == "#" and (neighbor_row, neighbor_col) not in visited:
                    visited.append((neighbor_row, neighbor_col))    # If neighbor has barrier, add to visited

                elif board[neighbor_row][neighbor_col] == "-":  # Otherwise, process node
                    destination_dist = abs(neighbor_row - dest_row) + abs(neighbor_col - dest_col)
                    updated_path_string = current_path_string + string_direction  # Update the path taken to reach node
                    updated_path = current_path + [source_node]

                    if (neighbor_row, neighbor_col) == destination:     # If Destination found, return path
                        updated_path = current_path + [source_node] + [destination]
                        instructions_string.set(f"Path: {updated_path}, {updated_path_string}")
                        reveal_path(updated_path)

                    heapq.heappush(paths,
                                   (destination_dist, (neighbor_row, neighbor_col), updated_path_string, updated_path))

        visited.append(source_node)

def reveal_path(updated_path):
    for step in updated_path:
        row, col = step
        if grid_colors[row][col] == 'white':
            grid_colors[row][col] = 'yellow'
            canvas.itemconfig(grid_rects[row][col], fill=grid_colors[row][col])
        

def create_grid(canvas, rows, cols, cell_size):
    grid_rects = []
    for row in range(rows):
        row_rects = []
        for col in range(cols):
            x1 = col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            rect = canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')
            canvas.tag_bind(rect, '<Button-1>', lambda event, r=row, c=col: on_click(r, c))
            row_rects.append(rect)
        grid_rects.append(row_rects)
    return grid_rects

root = tk.Tk()
root.title('Puzzle Traversal')
root.geometry("1200x1200")

#title
title_label = ttk.Label(master = root, text = "Puzzle Traversal", font = "Calibri 24 bold")
title_label.pack()

#canvas
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

rows = 10
cols = 10
cell_size = 50
grid_colors = [['white' for _ in range(cols)] for _ in range(rows)]
grid_rects = create_grid(canvas, rows, cols, cell_size)

#input field
input_frame = ttk.Frame(master = root)
button = ttk.Button(master = input_frame, text = "Find Path", padding = 10, command=solve_puzzle)
button.pack()
input_frame.pack()

#instructions
instructions_string = tk.StringVar(value="Select a source by clicking one of the cells. This is the starting point for the traversal.")
instructions = ttk.Label(master = root, font = "Calibri 16", padding=20, wraplength=800, textvariable=instructions_string)
instructions.pack()

root.mainloop()
