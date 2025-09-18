import sys
from chess_game import ChessGame


def main():
    from stockfish_engine import StockfishEngine
    print("Welcome to Chess vs Stockfish!")
    try:
        skill = int(input("Choose Stockfish skill level (0-20): "))
    except ValueError:
        skill = 10
    game = ChessGame(skill_level=skill)
    print("Game started! Enter moves in UCI format (e.g., e2e4)")
    while not game.is_game_over():
        print(StockfishEngine.render_board(game.board))
        move = input("Your move: ").strip()
        if move == 'quit':
            break
        if not game.make_human_move(move):
            print("Invalid move. Try again.")
            continue
        if game.is_game_over():
            break
        engine_move = game.make_engine_move()
        print(f"Stockfish plays: {engine_move}")
    print(StockfishEngine.render_board(game.board))
    print("Game over! Result:", game.result())
    game.quit()

if __name__ == "__main__":
    main()
