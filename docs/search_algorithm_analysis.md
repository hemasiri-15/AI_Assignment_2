# Search Algorithm Analysis

## Uninformed Search Strategies (AIMA Chapter 3)

### Complexity Parameters
| Symbol | Meaning |
|--------|---------|
| b | Branching factor (max children per node) |
| d | Depth of shallowest goal node |
| m | Maximum depth of search tree |
| l | Depth limit (DLS only) |

### Algorithm Comparison

| Algorithm | Complete | Optimal | Time | Space | Queue |
|-----------|----------|---------|------|-------|-------|
| BFS | YES | YES (unit cost) | O(b^d) | O(b^d) | FIFO |
| DFS | NO | NO | O(b^m) | O(b×m) | LIFO Stack |
| DLS | NO | NO | O(b^l) | O(b×l) | LIFO Stack |
| IDDFS | YES | YES (unit cost) | O(b^d) | O(b×d) | Stack + reset |

### Key Observations from Performance Comparison

| Problem | BFS Nodes | DFS Nodes | IDDFS Nodes | BFS Time | DFS Time |
|---------|-----------|-----------|-------------|----------|----------|
| Water Jug | 11 | 7 | 92 | 0.109ms | 0.059ms |
| Missionaries & Cannibals | 13 | 12 | 184 | 0.178ms | 0.114ms |
| 6-Queens | 114 | 32 | 388 | 1.480ms | 0.237ms |
| Tic Tac Toe | 56 | 6 | — | 0.666ms | 0.090ms |

### Why IDDFS is the Best Uninformed Strategy
- **Complete** like BFS — always finds a solution if one exists
- **Optimal** like BFS — finds shallowest solution
- **Memory efficient** like DFS — only O(b×d) space
- Re-expansion overhead is negligible in practice

### DLS — Depth Limited Search
- DFS with a hard depth limit `l`
- Returns **CUTOFF** if limit reached before goal
- Returns **FAILURE** if no solution exists within limit
- Building block of IDDFS (which tries l=0,1,2,3...)
