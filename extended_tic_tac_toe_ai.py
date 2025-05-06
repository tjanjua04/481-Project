import tkinter as tk
from tkinter import messagebox
import copy

# Constants
GRID_SIZE = 4
WIN_LENGTH = 4
vs_ai = True  # Set to False to play 2-player

# Initialize window
window = tk.Tk()
window.title("4x4 Tic Tac Toe")
current_player = "X"

# Button grid
buttons = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def get_board():
    return [[buttons[i][j]['text'] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

def check_draw_board(board):
    return all(cell != "" for row in board for cell in row)

def has_winner(board, player):
    # Horizontal and Vertical
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE - WIN_LENGTH + 1):
            if all(board[i][j + k] == player for k in range(WIN_LENGTH)):
                return True
            if all(board[j + k][i] == player for k in range(WIN_LENGTH)):
                return True

    # Diagonals
    for i in range(GRID_SIZE - WIN_LENGTH + 1):
        for j in range(GRID_SIZE - WIN_LENGTH + 1):
            if all(board[i + k][j + k] == player for k in range(WIN_LENGTH)):
                return True
            if all(board[i + k][j + WIN_LENGTH - 1 - k] == player for k in range(WIN_LENGTH)):
                return True

    return False

def evaluate(board):
    if has_winner(board, "O"):
        return 10
    elif has_winner(board, "X"):
        return -10
    else:
        return 0

def minimax(board, depth, is_maximizing):
    score = evaluate(board)
    if score == 10 or score == -10 or depth == 0 or check_draw_board(board):
        return score

    if is_maximizing:
        best = -float("inf")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if board[i][j] == "":
                    board[i][j] = "O"
                    value = minimax(board, depth - 1, False)
                    board[i][j] = ""
                    best = max(best, value)
        return best
    else:
        best = float("inf")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if board[i][j] == "":
                    board[i][j] = "X"
                    value = minimax(board, depth - 1, True)
                    board[i][j] = ""
                    best = min(best, value)
        return best

def best_move():
    board = get_board()
    best_score = -float("inf")
    move = None
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == "":
                board[i][j] = "O"
                score = minimax(board, 3, False)  # Depth-limited to 3 for performance
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def ai_turn():
    global current_player
    move = best_move()
    if move:
        i, j = move
        buttons[i][j]['text'] = "O"
        if has_winner(get_board(), "O"):
            messagebox.showinfo("Game Over", "AI (O) wins!")
            reset_board()
        elif check_draw_board(get_board()):
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_board()
        else:
            current_player = "X"

def on_click(row, col):
    global current_player
    if buttons[row][col]['text'] == "" and current_player == "X":
        buttons[row][col]['text'] = "X"
        if has_winner(get_board(), "X"):
            messagebox.showinfo("Game Over", "Player X wins!")
            reset_board()
        elif check_draw_board(get_board()):
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_board()
        elif vs_ai:
            current_player = "O"
            window.after(300, ai_turn)
        else:
            current_player = "O"

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

