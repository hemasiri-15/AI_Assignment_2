"""
Tic Tac Toe Search Problemx

State: tuple of 9 values X O or .
Board: 0|1|2  3|4|5  6|7|8
Goal : X wins
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bfs import bfs, reconstruct_path
from dfs import dfs

E = "."
X = "X"
O = "O"
WINS = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]


class TicTacToeProblem:
    def initial_state(self):
        return tuple([E] * 9)

    def is_goal(self, state):
        return self.winner(state) == X

    def winner(self, state):
        for (a, b, c) in WINS:
            if state[a] == state[b] == state[c] and state[a] != E:
                return state[a]
        return None

    def terminal(self, state):
        return self.winner(state) is not None or E not in state

    def turn(self, state):
        return X if state.count(X) == state.count(O) else O

    def expand(self, state):
        if self.terminal(state):
            return []
        t    = self.turn(state)
        succ = []
        if t == X:
            for i in range(9):
                if state[i] == E:
                    ns = list(state)
                    ns[i] = X
                    succ.append(("X plays {}".format(i), tuple(ns), 1))
        else:
            for i in range(9):
                if state[i] == E:
                    ns = list(state)
                    ns[i] = O
                    succ.append(("O plays {}".format(i), tuple(ns), 1))
                    break
        return succ


def draw(state):
    print()
    for r in range(3):
        print("  {} | {} | {}".format(
            state[r*3], state[r*3+1], state[r*3+2]))
        if r < 2:
            print("  ---------")
    print()


def show(name, goal, stats):
    print()
    print("=" * 50)
    print(" ", name, "— Tic Tac Toe")
    print("=" * 50)
    if goal is None:
        print("  No winning sequence found")
        return
    states, actions = reconstruct_path(goal)
    print("  X wins in {} moves".format(len(actions)))
    print("  Nodes expanded  :", stats["nodes_expanded"])
    print("  Time (ms)       : {:.4f}".format(stats["time_seconds"] * 1000))
    for i, state in enumerate(states):
        label = "Initial" if i == 0 else actions[i - 1]
        print("  Step {}: {}".format(i, label))
        draw(state)
    print("  X WINS!")
    print("=" * 50)


if __name__ == "__main__":
    print()
    print("  TIC TAC TOE")
    print("  Find X winning sequence")
    print()
    p = TicTacToeProblem()
    show("BFS", *bfs(p))
    show("DFS", *dfs(p))
