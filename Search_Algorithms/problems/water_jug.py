"""
Water Jug Problem

Jug A: 4L   Jug B: 3L   Goal: 2L in Jug A
State: (litres_in_A, litres_in_B)
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bfs import bfs, reconstruct_path
from dfs import dfs, iddfs


class WaterJugProblem:
    def __init__(self, cap_a=4, cap_b=3, goal_a=2):
        self.cap_a  = cap_a
        self.cap_b  = cap_b
        self.goal_a = goal_a

    def initial_state(self):
        return (0, 0)

    def is_goal(self, state):
        return state[0] == self.goal_a

    def expand(self, state):
        a, b  = state
        ca    = self.cap_a
        cb    = self.cap_b
        moves = []
        if a < ca:
            moves.append(("Fill A",    (ca, b),        1))
        if b < cb:
            moves.append(("Fill B",    (a, cb),         1))
        if a > 0:
            moves.append(("Empty A",   (0, b),          1))
        if b > 0:
            moves.append(("Empty B",   (a, 0),          1))
        if a > 0 and b < cb:
            p = min(a, cb - b)
            moves.append(("Pour A->B", (a - p, b + p), 1))
        if b > 0 and a < ca:
            p = min(b, ca - a)
            moves.append(("Pour B->A", (a + p, b - p), 1))
        return moves


def draw(state, ca=4, cb=3):
    a, b = state
    ba   = "#" * a + "." * (ca - a)
    bb   = "#" * b + "." * (cb - b)
    print("  JugA [{}] {}/{}L    JugB [{}] {}/{}L".format(
        ba, a, ca, bb, b, cb))


def show(name, goal, stats, ca=4, cb=3):
    print()
    print("=" * 52)
    print(" ", name, "— Water Jug")
    print("=" * 52)
    if goal is None:
        print("  FAILURE")
        return
    states, actions = reconstruct_path(goal)
    print("  Steps           :", len(actions))
    print("  Nodes expanded  :", stats["nodes_expanded"])
    print("  Time (ms)       : {:.4f}".format(stats["time_seconds"] * 1000))
    print()
    for i, state in enumerate(states):
        label = "Initial" if i == 0 else actions[i - 1]
        print("  Step {:2d}: {}".format(i, label))
        draw(state, ca, cb)
    print()
    print("  GOAL — {} litres in Jug A".format(states[-1][0]))
    print("=" * 52)


if __name__ == "__main__":
    print()
    print("  WATER JUG PROBLEM")
    print("  JugA=4L  JugB=3L  Goal=2L in JugA")
    print()
    p = WaterJugProblem()
    show("BFS",   *bfs(p))
    show("DFS",   *dfs(p))
    show("IDDFS", *iddfs(p))
