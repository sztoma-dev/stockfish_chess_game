import chess
from stockfish_engine import StockfishEngine

class ChessGame:
    def __init__(self, skill_level=10):
        self.board = chess.Board()
        self.engine = StockfishEngine(skill_level=skill_level)
        self.skill_level = skill_level

    def set_skill_level(self, level):
        self.skill_level = level
        self.engine.set_skill_level(level)

    def get_fen(self):
        return self.board.fen()

    def make_human_move(self, move_uci):
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                return True
            else:
                return False
        except Exception:
            return False

    def make_engine_move(self):
        fen = self.get_fen()
        best_move = self.engine.get_best_move(fen)
        move = chess.Move.from_uci(best_move)
        self.board.push(move)
        return best_move

    def is_game_over(self):
        return self.board.is_game_over()

    def result(self):
        return self.board.result()

    def quit(self):
        self.engine.quit()
