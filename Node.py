from TicTacToe import TicTacToe

class Node:
    """
    A class that creates instances of nodes that represent moves in
    tic-tac-toe rounds and stores information with each move to use to when
    traversing through possible games and when playing against the user.
    """

    def __init__(self, position=None, parent=None):
        """
        Constructor of the Node class

        Creates a new node representing a move in a particular game, sets
        its `parent` to the node representing the move before it, sets its
        children to an empty list to be later populated with nodes representing
        possible moves that could come after it and that will be parented by
        it, sets x_move which is whether this is a move for x to the opposite
        of its parent's x_move value, sets its discovery status (which
        means that all the games that include this move has been played) to
        false, and sets the record holding counts of outcomes of all the games
        that include this move to 0.

        :param position: position of the new node in the form of a tuple
        :param parent: another Node object
        """
        self.position = position
        self.parent = parent
        self.children = []
        self.discovered = False
        self.record = {
            'x': 0,
            'o': 0,
            'tie': 0,
        }
        if self.parent == None:
            self.x_move = False
        else:
            self.x_move = not self.parent.x_move


    def add_child(self, position):
        """
        Adds a child to the current node

        :param position: the position the child holds
        """
        self.children.append(Node(position, self))


    def generate_moves(self, round):
        """
        Populates `children` with possible moves (or just one crucial move
        whether that is a blocking or a winning move)

        :param round: the TicTacToe object representing the round
        """
        crucial_pos = round.crucial_move()
        if crucial_pos != None:
            self.add_child(crucial_pos)
        else:
            for position in round.empty_positions:
                self.add_child(position)


    def next_traversal(self, round):
        """
        returns an undiscovered move

        :param round: the TicTacToe object representing the round
        :return: Node object storing the move's position
        """
        if not self.children:
            self.generate_moves(round)

        if self.children[0].discovered:
            # sort children based on discovery status
            self.children.sort(
                key=lambda child: child.discovered
            )
        if round.print_round:
            self.print_discovery()

        assert not self.children[0].discovered

        return self.children[0]  # undiscovered child


    def print_discovery(self):
        """
        Print discovery statuses of possible moves as the program is
        discovering the possible games
        """
        print('Discovery Status')
        for child in self.children:
            print(child.position, child.discovered)


    def next_move(self, round):
        """
        Choose next move based on the highest move score

        :param round: the TicTacToe object representing the round
        :return: Node object storing the move's position
        """
        self.children.sort(
            reverse=True,  # So highest is first
            key=lambda child: child.move_score()
        )
        if round.print_round:
            self.print_stats()
        return self.children[0]


    def move_score(self):
        """
        Assign a score for the move represented by the current node. The score
        is to be used to compare possible moves

        :return: the calculated score as a float
        """
        if (self.record[self.get_team()] > 0
                and self.record[self.get_opponent()] == 0
                and self.record['tie'] == 0):
            return 99.999
        # After trial and error, I found this formula to best prioritize
        # between going for a win or a tie depending on the situation
        # Note: Ties are more important when winning chances are less
        # formula ≈ (wins + ties/wins) / (sqrt(xWins) + oWins)
        return (
            (self.record[self.get_team()]
             + self.record['tie']/max(1, self.record[self.get_team()]))
            / max(1.0, self.record['x']**(1/2) + self.record['o'])
        )


    def record_round(self, outcome, discovery_chance):
        """
        Recursively increment the records of each node with the outcome of
        the round, and update discovery status of the nodes, starting from
        the leaf node representing the last move in the round to the root
        representing the empty tic-tac-toe board
        """
        self.record[outcome] += 1
        if discovery_chance:
            self.discovered = self.is_discovered()
        if self.parent != None:
            # if child is not discovered, parent will definitely not be
            self.parent.record_round(outcome, self.discovered)


    def is_discovered(self):
        """
        Determines whether a node is discovered or not. A node is discovered
        if all of its children are discovered. If a node doesn't have children
        it's discovered

        :return: True or False
        """
        return all([child.discovered for child in self.children])


    def print_stats(self):
        """
        Prints the move scores the program is using to choose its next move
        """
        print('\n' + 'Move Scores')
        for child in self.children:
            print(
                str(child.position) + ':',
                round(child.move_score() * 100, 2),
                '  x:', child.record['x'],
                '  o:', child.record['o'],
                '  tie:', child.record['tie']
            )


    def print_outcomes(self):
        """
        Prints the total counts of outcomes in rounds where this particular
        move was played
        """
        print('\nOutcomes')
        for outcome in ('x', 'o', 'tie'):
            print(f'{outcome}: {self.record[outcome]}')
        print('\n')


    def has_child(self, position):
        """
        Checks if it has a child holding the passed position

        :param position: a tuple in the form (1<=i<=3, 1<=j<=3)
        :return: True or False
        """
        for child in self.children:
            if child.position == position:
                return True
        return False


    def get_child(self, position):
        """
        Returns the child node holding the passed position

        :param position: a tuple in the form (1<=i<=3, 1<=j<=3)
        :return: The child node holding the particular position
        """
        for child in self.children:
            if child.position == position:
                return child


    def get_team(self):
        """
        Returns the team of the current move

        :return: 'x' or 'o'
        """
        return TicTacToe.teams[self.x_move]


    def get_opponent(self):
        """
        Returns the opponent team of the current move

        :return: 'x' or 'o'
        """
        return TicTacToe.teams[not self.x_move]

