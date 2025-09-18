import subprocess
import threading
import queue
import os

# Unicode chess piece mapping
UNICODE_PIECES = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
    '.': '.'
}

class StockfishEngine:
    def __init__(self, path='bin/stockfish.exe', skill_level=10):
        self.path = path
        self.skill_level = skill_level
        self.process = subprocess.Popen(
            [self.path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )
        self._output_queue = queue.Queue()
        self._output_thread = threading.Thread(target=self._read_output, daemon=True)
        self._output_thread.start()
        self._send_command('uci')
        self._wait_for('uciok')
        self._send_command(f'setoption name Skill Level value {self.skill_level}')
        self._send_command('isready')
        self._wait_for('readyok')

    def _read_output(self):
        while True:
            line = self.process.stdout.readline()
            if line:
                self._output_queue.put(line.strip())

    def _send_command(self, command):
        self.process.stdin.write(command + '\n')
        self.process.stdin.flush()

    def _wait_for(self, text):
        while True:
            line = self._output_queue.get()
            if text in line:
                break

    def set_skill_level(self, level):
        self.skill_level = level
        self._send_command(f'setoption name Skill Level value {level}')
        self._send_command('isready')
        self._wait_for('readyok')

    def get_best_move(self, fen, movetime=1000):
        self._send_command(f'position fen {fen}')
        self._send_command(f'go movetime {movetime}')
        while True:
            line = self._output_queue.get()
            if line.startswith('bestmove'):
                return line.split()[1]

    def quit(self):
        self._send_command('quit')
        self.process.terminate()

    @staticmethod
    def render_board(board):
        # board: chess.Board object or FEN string
        if hasattr(board, 'board_fen'):
            fen = board.board_fen()
        else:
            fen = board.split()[0]
        rows = fen.split('/')
        display = []
        for row in rows:
            line = ''
            for c in row:
                if c.isdigit():
                    line += '.' * int(c)
                else:
                    line += UNICODE_PIECES.get(c, c)
            display.append(' '.join(line))
        return '\n'.join(display)
