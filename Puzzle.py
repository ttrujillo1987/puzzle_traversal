import heapq

def solve_puzzle(Board, Source, Destination):
    """Finds the shortest path in a puzzle sized MxN. Each cell in the puzzle is either open or has a barrier (denoted
    with '-' and '#' respectively). The path can only travel through open cells and not cells with barriers. Function
    returns the nodes the optimal path travels through as well as a string with the directions taken in the path."""

    paths = []                              # Create a priority queue for storing the paths from Source to Destination
    visited = []
    directions = [(1, 0, "D"), (0, 1, "R"), (-1, 0, "U"), (0, -1, "L")]

    dest_row, dest_col = (Destination)
    source_row, source_col = (Source)

    heapq.heappush(paths, (0, (source_row, source_col), "", []))    # Initialize the source

    if Source == Destination:
        return [Destination]

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

            if 0 <= neighbor_row < len(Board) and 0 <= neighbor_col < len(Board[0]):  # If neighbor is in graph

                if Board[neighbor_row][neighbor_col] == "#" and (neighbor_row, neighbor_col) not in visited:
                    visited.append((neighbor_row, neighbor_col))    # If neighbor has barrier, add to visited

                elif Board[neighbor_row][neighbor_col] == "-":  # Otherwise, process node
                    destination_dist = abs(neighbor_row - dest_row) + abs(neighbor_col - dest_col)
                    updated_path_string = current_path_string + string_direction  # Update the path taken to reach node
                    updated_path = current_path + [source_node]

                    if (neighbor_row, neighbor_col) == Destination:     # If Destination found, return path
                        updated_path = current_path + [source_node] + [Destination]
                        return updated_path, updated_path_string

                    heapq.heappush(paths,
                                   (destination_dist, (neighbor_row, neighbor_col), updated_path_string, updated_path))

        visited.append(source_node)

    return None
