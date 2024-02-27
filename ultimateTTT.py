import sys 

def create_board():
    return [[0 for _ in range(3)] for _ in range(3)]  # 3x3 small board

class GameState:
    def __init__(self):
        self.ultimate_board = [[0 for _ in range(3)] for _ in range(3)]  # 3x3 large board
        self.small_boards = [create_board() for _ in range(9)]
        self.current_player = "X"  # Start with 'X'
        self.active_board = None  # Where the next move must be made
        self.move_history = []

    # Methods for making moves, checking win states, etc. (We'll define these later)
    def make_move(self, board_index, row, col):
        # 1. Input Validation
        if not 0 <= board_index <= 8:
            raise ValueError("Invalid board index")
        if not 0 <= row <= 2 or not 0 <= col <= 2:
            raise ValueError("Invalid row or column")

        small_board = self.small_boards[board_index]

        if small_board[row][col] != 0:
            raise ValueError("Square already occupied")

        print("small board before move", small_board)

        # 2. Place the Mark
        small_board[row][col] = 1 if self.current_player == 'X' else -1 
        
        print(  "small board after move", small_board)

        # 3. Check for Small Board Win and Update Ultimate Board
        small_board_winner = self.check_small_board_win(small_board)
        # Update ultimate board
        if small_board_winner:
            self.ultimate_board[board_index // 3][board_index % 3] = 1 if small_board_winner == 'X' else -1

        # 4. Update Active Board (For Next Turn)
        self.active_board = row * 3 + col

        # 5. Switch Players
        self.current_player = "O" if self.current_player == "X" else "X"

        # Add move to history
        self.move_history.append((board_index, row, col, self.current_player))  # Store previous player


    def check_small_board_win(self, board):
        # Check rows, columns, and diagonals in a single loop
        for i in range(3):
            if all(cell == board[i][0] and cell != 0 for cell in board[i]):  # Row win
                return 1 if board[i][0] == 'X' else -1
            if all(board[r][i] == board[0][i] and board[r][i] != " " for r in range(3)):  # Column win
                return board[0][i]

        # Diagonals
        if all(board[i][i] == board[0][0] and board[i][i] != " " for i in range(3)):
            return board[0][0]
        if all(board[i][2 - i] == board[0][2] and board[i][2 - i] != " " for i in range(3)):
            return board[0][2]

        # Check for tie
        for row in board:
            if " " in row:
                return None
        return "Tie"

    def check_ultimate_board_win(self):
        board = self.ultimate_board

        # Check rows
        for row in board:
            if row[0] != " " and row[0] == row[1] == row[2]:
                return row[0]  # Winner!

        # Check columns
        for col in range(3):
            if board[0][col] != " " and board[0][col] == board[1][col] == board[2][col]:
                return board[0][col]  # Winner!

        # Check diagonals
        if board[0][0] != " " and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]  # Winner!
        if board[2][0] != " " and board[2][0] == board[1][1] == board[0][2]:
            return board[2][0]  # Winner!

        # Check for tie (no need to explicitly check, if no winner is found)
        return None  # Game still in progress

    def get_valid_moves(self):
        print("Inside get_valid_moves")
        valid_moves = []

        if self.active_board is None:  # First move of the game (anywhere is valid)
            for board_index in range(9):
                for row in range(3):
                    for col in range(3):
                        if self.small_boards[board_index][row][col] == " ":
                            valid_moves.append((board_index, row, col))
            return valid_moves

        # Opponent sent the player to a specific board
        board = self.small_boards[self.active_board]
        small_board_winner = self.check_small_board_win(board)

        if small_board_winner is None:  # Board is still in play
            for row in range(3):
                for col in range(3):
                    if board[row][col] == " ":
                        valid_moves.append((self.active_board, row, col))
        else:  # Board is already won (player can go anywhere)
            for board_index in range(9):
                board = self.small_boards[board_index]
                if self.check_small_board_win(board) is None:  # Avoid won boards
                    for row in range(3):
                        for col in range(3):
                            if board[row][col] == " ":
                                valid_moves.append((board_index, row, col))

        return valid_moves


    def minimax(self, depth, is_maximizing):
        game_over = self.check_ultimate_board_win()
        if game_over is not None:
            return game_over  # 1 for X win, -1 for O win, 0 for tie

        if depth == 0:
            return self.simple_heuristic()  # Replace 'simple_heuristic' with your actual function

        if is_maximizing:
            best_score = -float("inf")
            for move in self.get_valid_moves():
                self.make_move(*move)
                score = self.minimax(depth - 1, False)
                self.undo_move(*move)  # You'll need a function to undo moves
                best_score = max(best_score, score)
            return best_score
        else:  # Minimizing player
            best_score = float("inf")
            for move in self.get_valid_moves():
                self.make_move(*move)
                score = self.minimax(depth - 1, True)
                self.undo_move(*move)
                best_score = min(best_score, score)
            return best_score

    def simple_heuristic(self):
        score = 0
        for board in self.small_boards:
            winner = self.check_small_board_win(board)
            if winner == 1:   # If X wins a small board
                score += 10
            elif winner == -1:  # If O wins a small board
                score -= 10
        return score

    def undo_move(self):
        if self.move_history:
            board_index, row, col, player = self.move_history.pop()
            self.small_boards[board_index][row][col] = 0  # Clear the square

            # Undo ultimate board update
            if self.ultimate_board[board_index // 3][board_index % 3] != 0:
                self.ultimate_board[board_index // 3][board_index % 3] = 0

            self.current_player = player  # Restore the previous player

            # Recalculate active board
            self.active_board = None  # Easiest reset might be to clear and let it be recalculated on the next turn
        else:
            print("Error: No moves to undo.")
            
def print_board(game):
    symbols = {0: " ", 1: "X", -1: "O"}  

    # Small Boards
    for board_num, small_board in enumerate(game.small_boards):
        print(f"Board {board_num + 1}")
        for row in small_board:
            print(" | ".join(symbols[cell] for cell in row))
        if board_num % 3 != 2:
            print("---+---+---")

    # Ultimate Board
    print("\nUltimate Board")
    for row in game.ultimate_board:
        print(" | ".join(symbols[cell] for cell in row))
    print()

def get_human_input():
    print("Inside get_human_input")
    while True:
        try:
            input_str = input("Enter your move (board, row, col), e.g., 1 2 3: ").split()
            board_index = int(input_str[0]) - 1
            row = int(input_str[1]) - 1
            col = int(input_str[2]) - 1
            # Ensure the indices are within bounds (you already have validation in 'make_move')
            if 0 <= board_index <= 8 and 0 <= row <= 2 and 0 <= col <= 2:
                return board_index, row, col
            else:
                print("Invalid input. Please enter values between 1 and 3.")
        except (ValueError, IndexError):
            print("Invalid input format. Please enter three numbers separated by spaces.")


def main():
    print("Starting the game!")
    sys.stdout.flush()  
    game = GameState()

    while not game.check_ultimate_board_win():  
        print_board(game) 
        if game.current_player == "X":  # Human's Turn
            valid_move = False
            while not valid_move:
                try:
                    board_index, row, col = get_human_input()
                    game.make_move(board_index, row, col)
                    valid_move = True
                except ValueError as e:
                    print(f"Invalid Move: {e}")
        else:  # AI's turn
            best_score = -float("inf")
            best_move = None
            for move in game.get_valid_moves():
                game.make_move(*move)
                score = game.minimax(depth=4, is_maximizing=True) 
                game.undo_move(*move) 
                if score > best_score:
                    best_score = score
                    best_move = move

            if best_move: 
                game.make_move(*best_move)
            else:
                print("Error: Minimax could not find a valid move.")

    print("Game Over! Winner:", game.check_ultimate_board_win())

if __name__ == "__main__":
    main()
