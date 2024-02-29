class TicTacToeBoard:
    """General board class. Extended by GlobalBoard and LocalBoard"""

    def __init__(self):
        # 3x3 grid of zeros. Will be set to 1 or 2 when the square is claimed
        self.board = [[0, 0, 0] for _ in range(3)]

    # Does this board have tic tac toe
    def has_tic_tac_toe(self, player):
        """Checks if the current board has a tic-tac-toe for the given player"""
        # Check for horizontal and vertical tic tac toe
        for x in range(3):
            # Horizontal tic tac toe
            if self.board[x][0] == player and self.board[x][0] == self.board[x][1] and self.board[x][0] == self.board[x][2]:
                return True
            # Vertical tic tac toe
            if self.board[0][x] == player and self.board[0][x] == self.board[1][x] and self.board[0][x] == self.board[2][x]:
                return True

        # Check for negative diagonal tic tac toe
        if self.board[0][0] == player and self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2]:
            return True

        # Check for positive diagonal tic tac toe
        if self.board[2][0] == player and self.board[2][0] == self.board[1][1] and self.board[2][0] == self.board[0][2]:
            return True

        return False

    def is_full(self):
        """Checks if every space on the board has been played (i.e. there is a draw)"""
        return not any(0 in row for row in self.board)

    def check_draw_local(self, local_board_index):
        """Checks if a local board is drawn (i.e., no winner and no playable moves left)"""
        local_board = self.local_board_list[local_board_index]
        return not local_board.has_tic_tac_toe(1) and not local_board.has_tic_tac_toe(2) and local_board.is_full() and not self.has_tic_tac_toe(1) and not self.has_tic_tac_toe(2)

    def check_draw_global(self):
        """Checks if the global board is drawn (i.e., all local boards are drawn or not playable)"""
        return all(self.check_draw_local(i) or not self.local_board_list[i].playable for i in range(9))


class LocalBoard(TicTacToeBoard):
    def __init__(self, index):
        super().__init__()
        self.index = index  # The board's index in the local_board_list (from the GlobalBoard class)
        self.winner = None  # To track the winner of this local board
        self.playable = True  # Indicates if the board is playable or not

    def has_tic_tac_toe(self, player):
        """Checks if the local board has a tic-tac-toe for the given player"""
        if super().has_tic_tac_toe(player):
            self.winner = player
            self.playable = False  # Mark the board as not playable
            return True
        return False


class GlobalBoard(TicTacToeBoard):
    def __init__(self):
        super().__init__()
        self.local_board_list = [LocalBoard(i) for i in range(9)]  # 3x3 grid of local boards
        self.legal_boards = [board.index for board in self.local_board_list]  # List of legal (playable) boards

    def has_tic_tac_toe(self, player):
        """Checks if the global board has a tic-tac-toe for the given player"""
        # Check for horizontal and vertical tic-tac-toe
        for i in range(3):
            if self.local_board_list[i * 3].winner == player and self.local_board_list[i * 3 + 1].winner == player and self.local_board_list[i * 3 + 2].winner == player:
                return True  # Horizontal tic-tac-toe
            if self.local_board_list[i].winner == player and self.local_board_list[i + 3].winner == player and self.local_board_list[i + 6].winner == player:
                return True  # Vertical tic-tac-toe

        # Check for diagonal tic-tac-toe
        if self.local_board_list[0].winner == player and self.local_board_list[4].winner == player and self.local_board_list[8].winner == player:
            return True  # Negative diagonal tic-tac-toe
        if self.local_board_list[2].winner == player and self.local_board_list[4].winner == player and self.local_board_list[6].winner == player:
            return True  # Positive diagonal tic-tac-toe

        return False

    def print_board(self):
        """Prints the board in the command line"""
        print()
        print('-' * 35)
        print()

        for i in range(0, 9, 3):
            for row in range(3):
                for j in range(3):
                    print(self.local_board_list[i + j].board[row], end='\t')
                    if (j + 1) % 3 == 0:
                        print('|', end='\t')
                print()
                if (row + 1) % 3 == 0:
                    print('-' * 35)

    def mark_global_board(self, local_board, player):
        """Records when a local board has been won"""
        row = local_board.index // 3
        col = local_board.index % 3
        self.board[row][col] = player

    def update_focus(self, old_row, old_col):
        """Use the previous move to set the focus of the local boards for the next turn"""
        # Local board in the same position as the previous guess. May or may not be playable
        next_lb = self.local_board_list[old_row * 3 + old_col]

        # Update the playable status of local boards
        for local_board in self.local_board_list:
            # If the board is won by a player or is full, it is not playable
            if local_board.winner is not None or local_board.is_full():
                local_board.playable = False
            # If the board is not won by a player and is not full, it is playable
            else:
                local_board.playable = True

        # If the next board is playable, set its focus to True
        if next_lb.playable:
            for local_board in self.local_board_list:
                local_board.focus = False
            next_lb.focus = True
        # If the next board is not playable, set all playable boards in focus
        else:
            for local_board in self.local_board_list:
                if local_board.playable:
                    local_board.focus = True
                else:
                    local_board.focus = False


class TicTacToeGame:
    def __init__(self):
        self.global_board = GlobalBoard()  # Creamos un tablero global
        self.current_player = 1  # Jugador 1 empieza
        self.last_move = None  # Último movimiento registrado

    def play(self):
        while True:
            self.global_board.print_board()  # Mostramos el tablero

            # Verificamos si el juego ha terminado
            if self.global_board.has_tic_tac_toe(1):
                print("¡Jugador 1 gana!")
                break  # Salir del bucle si el jugador 1 gana globalmente
            elif self.global_board.has_tic_tac_toe(2):
                print("¡Jugador 2 gana!")
                break  # Salir del bucle si el jugador 2 gana globalmente
            elif self.global_board.check_draw_global():
                print("¡Empate!")
                break  # Salir del bucle si hay un empate global
            # Si el juego no ha terminado, seguimos jugando
            else:
                # Pedimos al jugador actual que haga su movimiento
                self.make_move()

                # Alternamos el turno de los jugadores
                self.current_player = 2 if self.current_player == 1 else 1

    def make_move(self):
        while True:
            try:
                if self.last_move is None or self.global_board.local_board_list[self.last_move].winner or not self.global_board.local_board_list[self.last_move].playable:
                    # Si es el primer movimiento, el tablero al que te mando tu rival con su jugada anterior se encuentra ganado,
                    # o el tablero al que te mandó tu rival está completo, el jugador puede elegir cualquier tablero para jugar
                    print(f"Jugador {self.current_player}, elige un tablero (0-8): ")
                    local_board_index = int(input())
                else:
                    # El jugador debe jugar en el tablero al que apunta el último movimiento del oponente
                    local_board_index = self.last_move

                if local_board_index not in self.global_board.legal_boards or self.global_board.local_board_list[local_board_index].is_full():
                    print("El tablero seleccionado no está disponible o está completo. Por favor, elige otro tablero.")
                    continue

                row = int(input(f"Jugador {self.current_player}, elige una fila (0, 1, 2) en el tablero {local_board_index}: "))
                col = int(input(f"Jugador {self.current_player}, elige una columna (0, 1, 2) en el tablero {local_board_index}: "))

                if 0 <= row < 3 and 0 <= col < 3 and self.global_board.local_board_list[local_board_index].board[row][col] == 0:
                    # Si la casilla está vacía y dentro del tablero seleccionado
                    self.global_board.local_board_list[local_board_index].board[row][col] = self.current_player
                    self.last_move = row * 3 + col  # Actualizar el último movimiento

                    # Comprobamos si el jugador ha ganado el tablero local
                    if self.global_board.local_board_list[local_board_index].has_tic_tac_toe(self.current_player):
                        print(f"¡Jugador {self.current_player} ha ganado el tablero {local_board_index}!")
                        # Eliminamos el tablero de la lista de tableros legales
                        self.global_board.legal_boards.remove(local_board_index)

                    self.global_board.mark_global_board(self.global_board.local_board_list[local_board_index], self.current_player)
                    self.update_focus(row, col)  # Actualizar el foco de los tableros locales
                    break
                else:
                    print("Movimiento inválido. Por favor, intenta nuevamente.")
            except (ValueError, IndexError):
                print("Entrada inválida. Por favor, intenta nuevamente.")

    def update_focus(self, old_row, old_col):
        """Use the previous move to set the focus of the local boards for the next turn"""
        # Local board in the same position as the previous guess. May or may not be playable
        next_lb = self.global_board.local_board_list[old_row * 3 + old_col]

        # Update the playable status of local boards
        for local_board in self.global_board.local_board_list:
            # If the board is won by a player or is full, it is not playable
            if local_board.winner is not None or local_board.is_full():
                local_board.playable = False
            # If the board is not won by a player and is not full, it is playable
            else:
                local_board.playable = True

        # If the next board is playable, set its focus to True
        if next_lb.playable:
            for local_board in self.global_board.local_board_list:
                local_board.focus = False
            next_lb.focus = True
        # If the next board is not playable, set all playable boards in focus
        else:
            for local_board in self.global_board.local_board_list:
                if local_board.playable:
                    local_board.focus = True
                else:
                    local_board.focus = False


# Creamos un juego y lo iniciamos
game = TicTacToeGame()
game.play()
