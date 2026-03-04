"""
dls.py — Depth-Limited Search (DLS)
AI Assignment 2 | Search Algorithms (AIMA Chapter 3)

DLS is a variant of DFS with a depth limit l.
- If solution found within limit  → return solution
- If limit reached before goal    → return CUTOFF
- If no solution exists at all    → return FAILURE

Used as a building block inside IDDFS.
"""

CUTOFF  = "CUTOFF"
FAILURE = "FAILURE"


def dls(problem, limit):
    """
    Depth-Limited Search.

    Args:
        problem : object with initial_state, actions(s), result(s,a), is_goal(s)
        limit   : maximum depth to search

    Returns:
        solution path, CUTOFF, or FAILURE
    """
    def recursive_dls(node, depth):
        state, path, cost = node

        if problem.is_goal(state):
            return path

        if depth == 0:
            return CUTOFF

        cutoff_occurred = False
        for action, next_state, step_cost in problem.actions(state):
            result = recursive_dls(
                (next_state, path + [next_state], cost + step_cost),
                depth - 1
            )
            if result == CUTOFF:
                cutoff_occurred = True
            elif result != FAILURE:
                return result

        return CUTOFF if cutoff_occurred else FAILURE

    initial = (problem.initial_state, [problem.initial_state], 0)
    return recursive_dls(initial, limit)


def run_demo():
    """
    Demo: Water Jug problem using DLS with limit=6
    """
    class WaterJug:
        def __init__(self):
            self.initial_state = (0, 0)

        def is_goal(self, state):
            return state[0] == 2

        def actions(self, state):
            a, b = state
            moves = []
            if a < 4: moves.append(("Fill A",   (4, b),          0))
            if b < 3: moves.append(("Fill B",   (a, 3),          0))
            if a > 0: moves.append(("Empty A",  (0, b),          0))
            if b > 0: moves.append(("Empty B",  (a, 0),          0))
            pour = min(a, 3 - b)
            if pour > 0: moves.append(("Pour A→B", (a-pour, b+pour), 0))
            pour = min(b, 4 - a)
            if pour > 0: moves.append(("Pour B→A", (a+pour, b-pour), 0))
            return moves

    problem = WaterJug()

    print("=" * 55)
    print("  DEPTH-LIMITED SEARCH (DLS) — Water Jug Demo")
    print("=" * 55)

    for limit in [3, 5, 6, 10]:
        result = dls(problem, limit)
        if result == CUTOFF:
            print(f"  Limit={limit} → CUTOFF (solution deeper than {limit})")
        elif result == FAILURE:
            print(f"  Limit={limit} → FAILURE (no solution exists)")
        else:
            print(f"  Limit={limit} → SOLVED! Path length={len(result)-1}")
            print(f"  Path: {result}")
            break

    print("=" * 55)
    print()
    print("  Key insight:")
    print("  - Limit=3 → CUTOFF  (solution at depth 6, too shallow)")
    print("  - Limit=5 → CUTOFF  (still too shallow)")
    print("  - Limit=6 → SOLVED  (found optimal solution)")
    print()
    print("  This is why IDDFS tries l=0,1,2,3... automatically.")
    print("=" * 55)


if __name__ == "__main__":
    run_demo()
