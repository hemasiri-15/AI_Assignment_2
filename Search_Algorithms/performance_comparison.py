"""
Performance Comparison — BFS vs DFS vs IDDFS
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bfs import bfs
from dfs import dfs, iddfs
from problems.missionaries_cannibals import MissionariesCannibals
from problems.water_jug               import WaterJugProblem
from problems.eight_queens            import EightQueensProblem
from problems.tic_tac_toe             import TicTacToeProblem


def run(name, fn, problem, **kw):
    goal, stats = fn(problem, **kw)
    return {
        "algorithm"       : name,
        "solved"          : "YES" if goal else "NO",
        "depth"           : str(goal.depth)     if goal else "N/A",
        "cost"            : str(goal.path_cost) if goal else "N/A",
        "nodes_expanded"  : stats["nodes_expanded"],
        "nodes_generated" : stats["nodes_generated"],
        "time_ms"         : "{:.4f}".format(stats["time_seconds"] * 1000),
    }


def table(title, results):
    print()
    print("=" * 72)
    print("  Problem:", title)
    print("=" * 72)
    print("  {:<8} {:>7} {:>7} {:>7} {:>11} {:>12} {:>11}".format(
        "Algo", "Solved", "Depth", "Cost",
        "Expanded", "Generated", "Time(ms)"))
    print("  " + "-" * 65)
    for r in results:
        print("  {:<8} {:>7} {:>7} {:>7} {:>11} {:>12} {:>11}".format(
            r["algorithm"], r["solved"], r["depth"], r["cost"],
            r["nodes_expanded"], r["nodes_generated"], r["time_ms"]))
    print("=" * 72)


if __name__ == "__main__":
    print()
    print("=" * 72)
    print("  PERFORMANCE COMPARISON — BFS vs DFS vs IDDFS")
    print("=" * 72)

    table("Water Jug (4L 3L -> 2L in A)", [
        run("BFS",   bfs,   WaterJugProblem()),
        run("DFS",   dfs,   WaterJugProblem()),
        run("IDDFS", iddfs, WaterJugProblem()),
    ])

    table("Missionaries and Cannibals (3M 3C)", [
        run("BFS",   bfs,   MissionariesCannibals()),
        run("DFS",   dfs,   MissionariesCannibals()),
        run("IDDFS", iddfs, MissionariesCannibals()),
    ])

    table("6-Queens (change N=6 to N=8 for full)", [
        run("BFS",   bfs,   EightQueensProblem(n=6)),
        run("DFS",   dfs,   EightQueensProblem(n=6)),
        run("IDDFS", iddfs, EightQueensProblem(n=6), max_depth=6),
    ])

    table("Tic Tac Toe (find X win)", [
        run("BFS", bfs, TicTacToeProblem()),
        run("DFS", dfs, TicTacToeProblem()),
    ])

    print()
    print("=" * 72)
    print("  OBSERVATIONS")
    print("=" * 72)
    print("""
  BFS   Complete=YES  Optimal=YES  Queue=FIFO  Space=O(b^d)
  DFS   Complete=NO   Optimal=NO   Queue=LIFO  Space=O(b*m)
  IDDFS Complete=YES  Optimal=YES  Queue=LIFO  Space=O(b*d)

  BFS always finds the shortest path but uses more memory.
  DFS uses much less memory but may not find shortest path.
  IDDFS is the best uninformed strategy — complete, optimal,
  and memory efficient. Recommended when depth is unknown.
  """)
    print("=" * 72)
    print()
