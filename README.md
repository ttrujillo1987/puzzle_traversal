December 2024 Update:
A GUI has been added to make interacting with this program easier.

Puzzle that takes in a 2-D puzzle of size MxN, that has N rows and M columns. It also takes in a tuple for a source and a tuple for destination. Each cell in the puzzle is either empty or has a barrier. 
Empty cells are marked with ‘-’ and cells with barriers are marked with ‘#’. 

Sample Input Puzzle Board: [[-,-,-,-,-],[-,-,#,-,-],[-,-,-,-,-],[#,-,#,#,-],[-#,-,-,-]] 

The goal is to find the minimum path from the source cell to the desitination cell. You can only move to empty cells and cannot move to 
a cell with a barrier in it. If there is not possible path from source to destination return None.

You can move only in the following directions. 
L: move to left cell from the current cell 
R: move to right cell from the current cell 
U: move to upper cell from the current cell 
D: move to the lower cell from the current cell  
