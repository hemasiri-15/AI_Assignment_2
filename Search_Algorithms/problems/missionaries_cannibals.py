"""
Missionaries and Cannibals

State  : (missionaries_left, cannibals_left, boat_side)
Initial: (3, 3, 1)   Goal: (0, 0, 0)
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bfs import bfs, reconstruct_path
from dfs import dfs, iddfs


class MissionariesCannibals:
    TOTAL_M = 3
    TOTAL_C = 3

    def initial_state(self):
        return (3, 3, 1)

    def is_goal(self, state):
        return state == (0, 0, 0)

    def is_valid(self, state):
        m_l, c_l, _ = state
        m_r = self.TOTAL_M - m_l
        c_r = self.TOTAL_C - c_l
        if m_l < 0 or c_l < 0 or m_r < 0 or c_r < 0:
            return False
        if m_l > 0 and c_l > m_l:
            return False
        if m_r > 0 and c_r > m_r:
            return False
        return True

    def expand(self, state):
        m, c, boat = state
        moves      = [(1,0),(2,0),(0,1),(0,2),(1,1)]
        result     = []
        for (dm, dc) in moves:
            if dm + dc < 1 or dm + dc > 2:
                continue
            if boat == 1:
                ns  = (m - dm, c - dc, 0)
                act = "Move {}M {}C right".format(dm, dc)
            else:
                ns  = (m + dm, c + dc, 1)
                act = "Move {}M {}C left".format(dm, dc)
            if self.is_valid(ns):
                result.append((act, ns, 1))
        return result


def draw(state):
    m_l, c_l, boat = state
    m_r = 3 - m_l
    c_r = 3 - c_l
    b   = "[BOAT]" if boat == 1 else "      "
    print("  LEFT {}M {}C  {}  ~~river~~  {}M {}C  RIGHT".format(
        m_l, c_l, b, m_r, c_r))


def show(name, goal, stats):
    print()
    print("=" * 55)
    print(" ", name, "— Missionaries and Cannibals")
    print("=" * 55)
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
        draw(state)
    print()
    print("  GOAL REACHED")
    print("=" * 55)


if __name__ == "__main__":
    print()
    print("  MISSIONARIES AND CANNIBALS")
    print("  Initial (3,3,1) -> Goal (0,0,0)")
    print()
    p = MissionariesCannibals()
    show("BFS",   *bfs(p))
    show("DFS",   *dfs(p))
    show("IDDFS", *iddfs(p))
