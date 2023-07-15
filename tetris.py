import curses
import random

# Tetris shapes
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 1], [0, 0, 1]]
]

# Initialize the game
def start_game(board):
    # Pick a random shape
    current_shape = random.choice(shapes)
    # Position it at the top in the middle of the board
    shape_row, shape_col = 0, len(board[0]) // 2 - len(current_shape[0]) // 2
    return current_shape, shape_row, shape_col

# Check if a move is valid
def valid_move(board, shape, row, col):
    for r, row_squares in enumerate(shape):
        for c, square in enumerate(row_squares):
            if square:  # If the square is part of the shape
                if r + row >= len(board) or c + col < 0 or c + col >= len(board[r]) or board[r + row][c + col]:
                    return False
    return True

# Merge the shape with the board
def merge_shape(board, shape, row, col):
    for r, row_squares in enumerate(shape):
        for c, square in enumerate(row_squares):
            if square:
                board[r + row][c + col] = 1

# Check and clear any full lines
def clear_lines(board):
    full_lines = [i for i, row in enumerate(board) if all(row)]
    # Remove full lines
    for i in full_lines:
        del board[i]
    # Add new lines at the top
    for i in range(len(full_lines)):
        board.insert(0, [0] * len(board[0]))
    return len(full_lines)

# Draw the board
def draw(screen, board, shape, row, col):
    screen.clear()
    for r, row_squares in enumerate(board):
        for c, square in enumerate(row_squares):
            if square or (r >= row and r < row + len(shape) and c >= col and c < col + len(shape[0]) and shape[r - row][c - col]):
                screen.addch(r, c, '#')
    screen.refresh()

def main(screen):
    curses.curs_set(0)
    h, w = 20, 10  # Height and width of the board
    board = [[0] * w for _ in range(h)]
    shape, row, col = start_game(board)
    while True:
        draw(screen, board, shape, row, col)
        key = screen.getch()
        new_row, new_col = row, col
        if key == curses.KEY_LEFT:
            new_col -= 1
        elif key == curses.KEY_RIGHT:
            new_col += 1
        elif key == curses.KEY_DOWN:
            new_row += 1
        if valid_move(board, shape, new_row, new_col):
            row, col = new_row, new_col
        else:
            if key == curses.KEY_DOWN:
                merge_shape(board, shape, row, col)
                lines_cleared = clear_lines(board)
                shape, row, col = start_game(board)
                if not valid_move(board, shape, row, col):
                    break  # Game over
            else:
                draw(screen, board, shape, row, col)  # Redraw the current state

if __name__ == '__main__':
    curses.wrapper(main)
