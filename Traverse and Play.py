import random
import time
from TicTacToe import TicTacToe
from Node import Node

# it takes about 5 seconds to play all games when it doesn't print them out
print_rounds = input(
    "Enter 'p' if you want the program to print tic-tac-toe rounds\n"
    + "as it learns, or press 'Enter' if you want it to learn silently: "
).strip().lower() == 'p'


root = Node()

# loops through all (logical) games and adds nodes containing
# moves and data to the tree rooted at `root`
while not root.discovered:
    round = TicTacToe(print_rounds)
    current_node = root  # root's children are the nine first 'x' moves
    while not round.is_over():
        next_node = current_node.next_traversal(round)
        round.play(next_node.position)
        current_node = next_node

    current_node.record_round(round.outcome, True)

root.print_outcomes()

print("""
Positions:

11 | 12 | 13
------------
21 | 22 | 23
------------
31 | 32 | 33
""".lstrip())

help_me = False  # if you want it to show you move scores before you choose
waiting_secs = 0.7  # seconds to wait before choosing a move

first_entrance = True  # to pass first entrance to the loop w/o question
while (first_entrance
        or input("Enter 'q' to quit or press 'Enter' to play again: ")
               .strip().lower() != 'q'):
    first_entrance = False
    round = TicTacToe(True)
    current_node = root
    familiar = True  # program's familiarity with the current game so far
    team = None
    while team not in ('x', 'o', 'r'):
        team = input('choose x, o, or r for random: ').strip().lower()
    if team == 'r':
        team = random.choice(TicTacToe.teams)

    while not round.is_over():
        if team == round.current_turn():
            # Player's turn
            if help_me and familiar:
                current_node.children.sort(
                    reverse=True,
                    key=lambda child: child.winning_ratio(team)
                )
                current_node.print_stats()
            position = ''
            while not round.is_valid_move(position):
                position = input('Choose move: ').strip()
            position = tuple([int(num) for num in position])
            round.play(position)
            if familiar:
                # checks if your move exist as a node inside the tree
                if current_node.has_child(position):
                    current_node = current_node.get_child(position)
                else:
                    familiar = False

        else:
            # Program's turn
            time.sleep(waiting_secs)
            if familiar:
                next_node = current_node.next_move(round)
                time.sleep(waiting_secs)
                round.play(next_node.position)
                current_node = next_node

            else:
                # usually it enters here in the last moves after it expects
                # you to block it but you don't. It would still proceed to
                # play a winning move in that case
                print('Unfamiliar Territory')
                position = round.crucial_move()
                if position == None:
                    # I believe my implementation prevents the need to enter
                    # this block. However, I put it just in case
                    print('Eenie meenie miney moe...')
                    position = random.choice(round.empty_positions)
                time.sleep(waiting_secs)
                round.play(position)

