"""
Eight Queens Problem

State: tuple where state[col] = row of queen in that column
Initial: ()   Goal: length N tuple with no conflicts
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bfs import bfs, reconstruct_path
from dfs import dfs, iddfs


class EightQueensProblem:
    def __init__(self, n=8):
        self.n = n

    def initial_state(self):
        return ()

    def is_goal(self, state):
        return len(state) == self.n

    def no_conflict(self, state, new_row):
        new_col = len(state)
        for col, row in enumerate(state):
            if row == new_row:
                return False
            if abs(row - new_row) == abs(col - new_col):
                return False
        return True

    def expand(self, state):
        if len(state) >= self.n:
            return []
        nc   = len(state)
        succ = []
        for row in range(self.n):
            if self.no_conflict(state, row):
                succ.append(("col={} row={}".format(nc, row), state + (row,), 1))
        return succ


def draw(state, n):
    print()
    print("    " + " ".join(str(i) for i in range(n)))
    print("  +" + "---" * n + "+")
    for row in range(n):
        line = "  |"
        for col in range(n):
            if col < len(state) and state[col] == row:
                line += " Q "
            else:
                line += " . " if (row + col) % 2 == 0 else " _ "
        line += "|"
        print(line)
    print("  +" + "---" * n + "+")
    print()


def show(name, n, goal, stats):
    print()
    print("=" * 52)
    print(" ", name, "—", n, "Queens")
    print("=" * 52)
    if goal is None:
        print("  FAILURE")
        return
    print("  Solution        :", goal.state)
    print("  Nodes expanded  :", stats["nodes_expanded"])
    print("  Time (ms)       : {:.4f}".format(stats["time_seconds"] * 1000))
    draw(goal.state, n)
    print("=" * 52)


if __name__ == "__main__":
    N = 6
    print()
    print("  {}-QUEENS PROBLEM".format(N))
    print("  Change N=6 to N=8 for full problem")
    print()
    p = EightQueensProblem(n=N)
    show("BFS",   N, *bfs(p))
    show("DFS",   N, *dfs(p))
    show("IDDFS", N, *iddfs(p, max_depth=N))
