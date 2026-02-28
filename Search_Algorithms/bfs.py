"""
Breadth-First Search (BFS)

Complete : YES
Optimal  : YES (unit step costs)
Time     : O(b^d)
Space    : O(b^d)
Queue    : FIFO (collections.deque)
"""

from collections import deque
import time


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0, depth=0):
        self.state     = state
        self.parent    = parent
        self.action    = action
        self.path_cost = path_cost
        self.depth     = depth

    def __repr__(self):
        return "Node({})".format(self.state)


def reconstruct_path(node):
    states  = []
    actions = []
    while node.parent is not None:
        states.append(node.state)
        actions.append(node.action)
        node = node.parent
    states.append(node.state)
    states.reverse()
    actions.reverse()
    return states, actions


def bfs(problem):
    stats = {
        "nodes_expanded"  : 0,
        "nodes_generated" : 1,
        "max_frontier"    : 1,
        "time_seconds"    : 0.0,
    }
    start = time.time()
    root  = Node(state=problem.initial_state())

    if problem.is_goal(root.state):
        stats["time_seconds"] = time.time() - start
        return root, stats

    frontier = deque([root])
    reached  = {root.state}

    while frontier:
        node = frontier.popleft()
        stats["nodes_expanded"] += 1

        for (action, next_state, cost) in problem.expand(node.state):
            child = Node(
                state     = next_state,
                parent    = node,
                action    = action,
                path_cost = node.path_cost + cost,
                depth     = node.depth + 1,
            )
            stats["nodes_generated"] += 1

            if problem.is_goal(next_state):
                stats["time_seconds"] = time.time() - start
                return child, stats

            if next_state not in reached:
                reached.add(next_state)
                frontier.append(child)
                if len(frontier) > stats["max_frontier"]:
                    stats["max_frontier"] = len(frontier)

    stats["time_seconds"] = time.time() - start
    return None, stats


def print_result(algorithm_name, problem_name, goal_node, stats):
    print()
    print("=" * 52)
    print("  {} on {}".format(algorithm_name, problem_name))
    print("=" * 52)
    if goal_node is None:
        print("  Result : FAILURE")
    else:
        states, actions = reconstruct_path(goal_node)
        print("  Result          : SUCCESS")
        print("  Solution depth  :", goal_node.depth)
        print("  Solution cost   :", goal_node.path_cost)
        print("  Actions         :", actions)
    print("  Nodes expanded  :", stats["nodes_expanded"])
    print("  Nodes generated :", stats["nodes_generated"])
    print("  Time (ms)       : {:.4f}".format(stats["time_seconds"] * 1000))
    print("=" * 52)
    print()


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
    print("  BFS Demo")
    print("=" * 52)
    problem     = SimpleGraphProblem()
    goal, stats = bfs(problem)
    print_result("BFS", "Simple Graph", goal, stats)
    if goal:
        states, actions = reconstruct_path(goal)
        print("  Path:", " -> ".join(states))
