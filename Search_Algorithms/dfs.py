"""
DFS, DLS, IDDFS

DFS   : LIFO stack. Not complete. Not optimal. Space O(b*m)
DLS   : DFS with depth limit
IDDFS : Runs DLS with limits 0,1,2... Complete + Optimal + Space O(b*d)
"""

import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bfs import Node, reconstruct_path, print_result

CUTOFF  = "CUTOFF"
FAILURE = "FAILURE"


def dfs(problem):
    stats = {
        "nodes_expanded"  : 0,
        "nodes_generated" : 1,
        "max_frontier"    : 1,
        "time_seconds"    : 0.0,
    }
    start    = time.time()
    root     = Node(state=problem.initial_state())
    frontier = [root]
    reached  = {root.state}

    while frontier:
        node = frontier.pop()
        stats["nodes_expanded"] += 1

        if problem.is_goal(node.state):
            stats["time_seconds"] = time.time() - start
            return node, stats

        for (action, next_state, cost) in problem.expand(node.state):
            child = Node(
                state     = next_state,
                parent    = node,
                action    = action,
                path_cost = node.path_cost + cost,
                depth     = node.depth + 1,
            )
            stats["nodes_generated"] += 1
            if next_state not in reached:
                reached.add(next_state)
                frontier.append(child)
                if len(frontier) > stats["max_frontier"]:
                    stats["max_frontier"] = len(frontier)

    stats["time_seconds"] = time.time() - start
    return None, stats


def dls(problem, limit):
    stats = {
        "nodes_expanded"  : 0,
        "nodes_generated" : 1,
        "max_frontier"    : 1,
        "time_seconds"    : 0.0,
    }
    start    = time.time()
    root     = Node(state=problem.initial_state())
    frontier = [root]
    result   = None
    reached  = set()

    while frontier:
        node = frontier.pop()
        stats["nodes_expanded"] += 1

        if problem.is_goal(node.state):
            stats["time_seconds"] = time.time() - start
            return node, stats

        if node.depth >= limit:
            result = CUTOFF
            continue

        if node.state in reached:
            continue
        reached.add(node.state)

        for (action, next_state, cost) in problem.expand(node.state):
            child = Node(
                state     = next_state,
                parent    = node,
                action    = action,
                path_cost = node.path_cost + cost,
                depth     = node.depth + 1,
            )
            stats["nodes_generated"] += 1
            frontier.append(child)
            if len(frontier) > stats["max_frontier"]:
                stats["max_frontier"] = len(frontier)

    stats["time_seconds"] = time.time() - start
    if result == CUTOFF:
        return CUTOFF, stats
    return None, stats


def iddfs(problem, max_depth=50):
    stats = {
        "nodes_expanded"  : 0,
        "nodes_generated" : 0,
        "max_frontier"    : 0,
        "iterations"      : 0,
        "time_seconds"    : 0.0,
    }
    start = time.time()

    for depth in range(max_depth + 1):
        stats["iterations"] += 1
        result, iter_stats  = dls(problem, depth)

        stats["nodes_expanded"]  += iter_stats["nodes_expanded"]
        stats["nodes_generated"] += iter_stats["nodes_generated"]
        if iter_stats["max_frontier"] > stats["max_frontier"]:
            stats["max_frontier"] = iter_stats["max_frontier"]

        if result is CUTOFF:
            continue
        elif result is None:
            break
        else:
            stats["time_seconds"] = time.time() - start
            return result, stats

    stats["time_seconds"] = time.time() - start
    return None, stats


class SimpleGraphProblem:
    def initial_state(self): return "S"
    def is_goal(self, s):    return s == "G"
    def expand(self, state):
        graph = {
            "S": [("to_A", "A", 1), ("to_B", "B", 4)],
            "A": [("to_G", "G", 1), ("to_C", "C", 2)],
            "B": [("to_G", "G", 2)],
            "C": [("to_G", "G", 1)],
            "G": [],
        }
        return graph.get(state, [])


if __name__ == "__main__":
    print()
    print("=" * 52)
    print("  DFS / DLS / IDDFS Demo")
    print("=" * 52)
    problem = SimpleGraphProblem()

    goal, stats = dfs(problem)
    print_result("DFS", "Simple Graph", goal, stats)

    result, stats = dls(problem, limit=1)
    if result is CUTOFF:
        print("  DLS (limit=1): CUTOFF — solution deeper than limit\n")
    else:
        print_result("DLS (limit=1)", "Simple Graph", result, stats)

    result, stats = dls(problem, limit=5)
    print_result("DLS (limit=5)", "Simple Graph", result, stats)

    goal, stats = iddfs(problem)
    print("  IDDFS iterations used:", stats["iterations"])
    print_result("IDDFS", "Simple Graph", goal, stats)
