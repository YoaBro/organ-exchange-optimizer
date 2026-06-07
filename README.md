# Organ Exchange Optimizer

This is a small coursework project that models a simplified kidney exchange problem as an Integer Linear Programming (ILP) problem.

This project implements only the core algorithmic idea from that setting. It is not a medical system and does not model the full set of real-world medical, legal, ethical, and logistical constraints.

## Problem Overview

Organ exchange is a critical problem in medical logistics where patient-donor pairs are matched to perform organ transplants. The challenge is to find compatible exchanges in a directed graph where:
- **Nodes** represent patient-donor pairs
- **Edges** represent compatibility (donor from pair A can give to patient from pair B)
- **Cycles** represent valid exchanges (2-way swaps or 3-way exchanges)

This solver finds the maximum number of disjoint cycles (length 2 or 3) to maximize the total number of patients who can receive transplants.

## Solution Approach

The solver uses **Integer Linear Programming** via PuLP and CBC solver:

1. **Cycle Discovery**: Enumerate all valid 2-cycles (mutual exchanges) and 3-cycles in the graph
2. **ILP Formulation**:
   - **Decision Variables**: Binary variable for each cycle (selected or not)
   - **Objective**: Maximize total patients helped (sum of cycle lengths)
   - **Constraints**: Each patient-donor pair participates in at most one cycle

## Features

- Finds optimal solution to the organ exchange matching problem
- Efficient cycle enumeration for 2-cycles and 3-cycles
- Uses proven ILP solver (CBC) for guaranteed optimal results
- Includes performance benchmarking on random graphs
- Handles graphs up to 500+ nodes efficiently
- Easy-to-use API with comprehensive documentation

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Basic Example

```python
import networkx as nx
from organ_exchange_optimizer import find_organ_exchange

# Create a directed graph of patient-donor pairs
G = nx.DiGraph()
G.add_edge(0, 1)  # Donor of pair 0 compatible with patient of pair 1
G.add_edge(1, 0)  # Donor of pair 1 compatible with patient of pair 0
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 2)

# Solve for optimal organ exchanges
cycles, num_transplants = find_organ_exchange(G)

print(f"Total transplants possible: {num_transplants}")
print("Exchange cycles:")
for cycle in cycles:
    print(f"  {cycle}")
```

### Running Tests

```bash
python organ_exchange_optimizer.py
```

This will run:
- **Part A**: Basic test case with predefined cycles
- **Part B**: Performance benchmarking on random graphs (up to 500 nodes)

## Requirements

- Python 3.7+
- NetworkX - Graph data structure and algorithms
- PuLP - Linear programming modeling
- CBC - Coin-or branch and cut solver

Install all dependencies:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install networkx pulp
```

## Algorithm Details

### Complexity Analysis

- **Cycle Enumeration**: O(n²) for 2-cycles, O(n³) for 3-cycles
- **ILP Solving**: Polynomial time for small cycles (typical case)
- **Overall**: Efficient for practical network sizes

### Performance Benchmarks

The solver efficiently handles:
- **n=100**: < 1 second
- **n=300**: < 10 seconds
- **n=500**: < 60 seconds

(Benchmarks run with 30% edge probability)

## How It Works

### Step 1: Cycle Discovery

The algorithm exhaustively searches the graph for:
- **2-cycles**: Bidirectional edges where donor pairs can mutually exchange
- **3-cycles**: Three patient-donor pairs in circular compatibility

```
2-cycle:        3-cycle:
0 <-> 1         0 -> 1
                |    |
                v    v
                3 <- 2
```

### Step 2: ILP Optimization

For each cycle found, a binary variable x_i is created. The solver then:
- **Maximizes**: Σ (cycle_length × x_i)
- **Subject to**: For each node, Σ x_i (cycles containing node) ≤ 1

This ensures a valid matching without conflicts.

### Step 3: Solution Extraction

All cycles with x_i = 1 are selected, and the total number of transplants is computed.

## Example Output

```
=== Part A: Basic Test ===
transplants: 5
cycles found:
   [0, 1]
   [2, 3, 4]

=== Part B: Random Graphs (max 60 sec) ===
n=10: 4 transplants, time=0.01s
n=20: 8 transplants, time=0.01s
n=50: 18 transplants, time=0.05s
n=100: 35 transplants, time=0.12s
n=300: 105 transplants, time=5.43s
n=500: 152 transplants, time=8.45s

largest n that finishes in under 1 minute: 500
```

## API Reference

### `find_organ_exchange(g)`

Finds the maximum set of disjoint cycles in a patient-donor compatibility graph.

**Parameters:**
- `g` (networkx.DiGraph): Directed graph where nodes are patient-donor pairs and edges represent compatibility

**Returns:**
- `cycles` (list): List of selected cycles, each cycle is a list of node indices
- `total` (int): Total number of patients who can receive transplants

**Example:**
```python
cycles, num = find_organ_exchange(G)
for cycle in cycles:
    print(f"Cycle: {cycle}")
print(f"Total transplants: {num}")
```

### `generate_random_graph(n, p)`

Generates a random directed graph for testing and benchmarking.

**Parameters:**
- `n` (int): Number of nodes
- `p` (float): Edge probability (0 to 1)

**Returns:**
- `g` (networkx.DiGraph): Random directed graph

## Real-World Applications

This algorithm is used in:
- **Medical Transplant Networks**: National Kidney Registry, UNOS Kidney Paired Donation Program
- **Organ Donation Coordination**: Matching compatible patient-donor pairs
- **Fairness-Aware Matching**: Incorporating constraints for equity and accessibility
- **Logistics Optimization**: Coordinating multi-hospital exchanges

## Research References

- Roth, A. E., Sönmez, T., & Ünver, M. U. (2007). "Efficient Kidney Exchange: Coincidence of Wants in Markets with Compatibility." American Economic Review.
- Anderson, R., Ashlagi, I., Gamarnik, D., & Kannan, A. (2015). "Efficient Dynamic Barter Exchange." Operations Research.
- Glorie, K. B., van de Velde, S. L., & Wagelmans, A. P. (2014). "Kidney Exchange with Long Chains: Efficient Algorithms and Optimal Solutions." Transplantation.

## Project Structure

```
organ-exchange-optimizer/
├── organ_exchange_optimizer.py   # Main solver implementation
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── LICENSE                        # MIT License
└── tests/                         # Test cases
    └── test_optimizer.py          # Unit tests
```

## Disclaimer

**Note**: This is a solution to an academic assignment. For real medical applications, additional constraints must be included:
- Blood type compatibility
- Tissue matching (HLA compatibility)
- Waiting time priorities
- Geographic constraints
- Medical urgency factors
- Fairness and ethical considerations

Consult medical professionals and regulatory bodies before deploying in real transplant networks.

