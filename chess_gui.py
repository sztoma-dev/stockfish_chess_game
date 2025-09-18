
import tkinter as tk
from tkinter import simpledialog, messagebox
from chess_game import ChessGame
from stockfish_engine import UNICODE_PIECES

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess vs Stockfish")
        skill = simpledialog.askinteger("Skill Level", "Choose Stockfish skill level (0-20):", minvalue=0, maxvalue=20)
        if skill is None:
            skill = 10
        self.game = ChessGame(skill_level=skill)
        self.selected_square = None
        self.squares = []
        self.canvas = tk.Canvas(root, width=480, height=480)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.on_click)
        self.update_board()

    def update_board(self):
        self.canvas.delete('all')
        board = self.game.board
        size = 60
        colors = ['#F0D9B5', '#B58863']
        fen = board.board_fen()
        rows = fen.split('/')
        for r, row in enumerate(rows):
            file = 0
            for c in row:
                if c.isdigit():
                    file += int(c)
                else:
                    x0 = file * size
                    y0 = r * size
                    color = colors[(r + file) % 2]
                    self.canvas.create_rectangle(x0, y0, x0+size, y0+size, fill=color, outline='black')
                    piece = UNICODE_PIECES.get(c, c)
                    self.canvas.create_text(x0+size//2, y0+size//2, text=piece, font=('Arial', 32))
                    file += 1
            # fill empty squares
            for f in range(8):
                x0 = f * size
                y0 = r * size
                if not self.canvas.find_enclosed(x0, y0, x0+size, y0+size):
                    color = colors[(r + f) % 2]
                    self.canvas.create_rectangle(x0, y0, x0+size, y0+size, fill=color, outline='black')
        if self.selected_square:
            x, y = self.selected_square
            self.canvas.create_rectangle(x*size, y*size, (x+1)*size, (y+1)*size, outline='red', width=3)
        if self.game.is_game_over():
            messagebox.showinfo("Game Over", f"Result: {self.game.result()}")
            self.game.quit()
            self.root.quit()

    def on_click(self, event):
        size = 60
        x = event.x // size
        y = event.y // size
        if self.selected_square is None:
            self.selected_square = (x, y)
            self.update_board()
        else:
            from chess import square_name
            from chess import Board
            # Convert GUI coordinates to chess square
            from_square = square_name(self.selected_square[0] + (7-self.selected_square[1])*8)
            to_square = square_name(x + (7-y)*8)
            move_uci = from_square + to_square
            if self.game.make_human_move(move_uci):
                self.selected_square = None
                self.update_board()
                if not self.game.is_game_over():
                    engine_move = self.game.make_engine_move()
                    self.update_board()
            else:
                self.selected_square = None
                self.update_board()
                messagebox.showerror("Invalid Move", "Please select a valid move.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()
