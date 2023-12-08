class TicTacToe:
    """
    A tic-tac-toe class that creates instances of tic-tac-toe rounds
    """
    positions = [(row, col)
                 for row in range(1, 4)
                 for col in range(1, 4)]

    # a list of lists all three position tuples forming a line in the board
    lines = [
        [(row, col) for col in range(1, 4)]
        for row in range(1, 4)
    ] + [
        [(row, col) for row in range(1, 4)]
        for col in range(1, 4)
    ] + [
        [(i, i) for i in range(1, 4)]
    ] + [
        [(2+i, 2-i) for i in range(-1, 2)]
    ]

    teams = ('o', 'x')

    def __init__(self, print_round):
        """
        Constructor for the TicTacToe class
        Starts a new Tic Tac Toe Match by setting and empty board in a
        dictionary

        :param print_round: True of False whether
        """
        self.board = {position: ' ' for position in self.positions}
        self.empty_positions = self.positions[:] # not the same reference
        self.x_turn = True
        self.print_round = print_round
        self.outcome = None


    def is_win(self):
        """
        Checks if one of the teams has already won

        :return: True if one of the teams has won, or false otherwise
        """
        for sequence in self.lines:
            if (self.board[sequence[0]]
                    == self.board[sequence[1]]
                    == self.board[sequence[2]]
                    != ' '):
                return True
        return False


    def play(self, position):
        """
        plays for the team who has the current turn at `position`

        :param position: A tuple of the form {(i, j) | 1<=i<=3, 1<=j<=3}
        """
        assert position in self.empty_positions
        assert not self.is_over()

        self.board[position] = self.current_turn()
        self.empty_positions.remove(position)

        if self.is_win():
            self.outcome = self.current_turn()
        elif self.is_full():
            self.outcome = 'tie'

        if self.print_round:
            print()
            self.print_board()
            if self.is_over():
                if self.outcome == 'tie':
                    print("It's a tie!\n\n")
                else:
                    print(f'{self.current_turn()} won!\n\n')

        self.x_turn = not self.x_turn


    def is_over(self):
        """
        Checks whether the game is over

        :return: True if the game is over, false otherwise
        """
        # self.outcome could only be: None, 'x', 'o', 'tie'
        return self.outcome != None


    def is_full(self):
        """
        Checks if the board is full

        :return: True if the board is full, or False otherwise
        """
        # no empty positions = full
        return not self.empty_positions


    def print_board(self):
        """
        Prints the board
        """
        print(self.board[(1, 1)], self.board[(1, 2)], self.board[(1, 3)],
              sep='|')
        print('-' * 5)
        print(self.board[(2, 1)], self.board[(2, 2)], self.board[(2, 3)],
              sep='|')
        print('-' * 5)
        print(self.board[(3, 1)], self.board[(3, 2)], self.board[(3, 3)],
              sep='|')
        print()


    def crucial_move(self):
        """
        Checks if there is a crucial (must-take) move. If there is a winning
        move it returns it, otherwise, it returns a defense move if there is
        one or None if there isn't crucial moves at this point

        :return: a tuple of length 2 or None
        """
        move = None
        for line in self.lines:
            # stores the values of that line in a list
            line_values = [self.board[position]
                           for position in line]

            # remove empty slots
            while ' ' in line_values:
                line_values.remove(' ')

            # if there are two non-empty slots and they are equal, it means
            # there is a winning or blocking move
            if len(line_values) == 2 and line_values[0] == line_values[1]:
                move = self.missing_piece(line)
                if line_values[0] == self.current_turn():
                    return move # winning move
        return move # defence move


    def missing_piece(self, line):
        """
        Returns the empty position given a line that has two symbols lined up

        :param line: A list of three positions (tuples of length 2)
        that form a line in the board
        :return: a tuple of length two
        """
        for position in line:
            if self.board[position] == ' ':
                return position


    def current_turn(self):
        """
        Returns the team that has the current turn

        :return: 'x' or 'o'
        """
        return self.teams[self.x_turn]


    def is_valid_move(self, position):
        """
        Checks if a position value is valid in terms of form and emptiness of
        the position in the board (used to check users input)

        :param position: a tuple of length 2
        :return: True if `position is valid, False otherwise
        """
        if len(position) != 2 or not position.isnumeric():
            return False
        position = tuple([int(num) for num in position])
        return position in self.empty_positions

