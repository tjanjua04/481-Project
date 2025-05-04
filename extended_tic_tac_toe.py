import tkinter as tk
from tkinter import messagebox

# Constants
GRID_SIZE = 4
WIN_LENGTH = 4

# Initialize window
window = tk.Tk()
window.title("4x4 Tic Tac Toe")
current_player = "X"

# Button grid
buttons = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def check_winner():
    board = [[buttons[i][j]['text'] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

    # Check horizontal, vertical, diagonal, and anti-diagonal lines for win
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE - WIN_LENGTH + 1):
            # Horizontal
            if all(board[i][j + k] == current_player for k in range(WIN_LENGTH)):
                return True
            # Vertical
            if all(board[j + k][i] == current_player for k in range(WIN_LENGTH)):
                return True

    # Check diagonals
    for i in range(GRID_SIZE - WIN_LENGTH + 1):
        for j in range(GRID_SIZE - WIN_LENGTH + 1):
            # Top-left to bottom-right
            if all(board[i + k][j + k] == current_player for k in range(WIN_LENGTH)):
                return True
            # Top-right to bottom-left
            if all(board[i + k][j + WIN_LENGTH - 1 - k] == current_player for k in range(WIN_LENGTH)):
                return True
    return False

def check_draw():
    return all(buttons[i][j]['text'] != "" for i in range(GRID_SIZE) for j in range(GRID_SIZE))

def on_click(row, col):
    global current_player
    if buttons[row][col]['text'] == "":
        buttons[row][col]['text'] = current_player
        if check_winner():
            messagebox.showinfo("Game Over", f"Player {current_player} wins!")
            reset_board()
        elif check_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_board()
        else:
            current_player = "O" if current_player == "X" else "X"

def reset_board():
    global current_player
    current_player = "X"
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            buttons[i][j]['text'] = ""

# Create buttons
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        button = tk.Button(window, text="", font=('Arial', 32), width=4, height=2,
                           command=lambda row=i, col=j: on_click(row, col))
        button.grid(row=i, column=j)
        buttons[i][j] = button

window.mainloop()
