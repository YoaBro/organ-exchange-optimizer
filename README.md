# Kidney Exchange ILP Solver

An Integer Linear Programming (ILP) solution for optimizing kidney exchange networks to maximize the number of life-saving transplants.

## Problem Overview

Kidney exchange is a critical problem in medical logistics where patient-donor pairs are matched to perform kidney transplants. The challenge is to find compatible exchanges in a directed graph where:
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

- Finds optimal solution to the kidney exchange matching problem
- Efficient cycle enumeration for 2-cycles and 3-cycles
- Uses proven ILP solver (CBC) for guaranteed optimal results
- Includes performance benchmarking on random graphs
- Handles graphs up to 500+ nodes efficiently

## Usage

### Basic Example

```python
import networkx as nx
from q5_kidney_exchange import find_kidney_exchange

# Create a directed graph of patient-donor pairs
G = nx.DiGraph()
G.add_edge(0, 1)  # Donor of pair 0 compatible with patient of pair 1
G.add_edge(1, 0)  # Donor of pair 1 compatible with patient of pair 0
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 2)

# Solve for optimal kidney exchanges
cycles, num_transplants = find_kidney_exchange(G)

print(f"Total transplants possible: {num_transplants}")
print("Exchange cycles:")
for cycle in cycles:
    print(f"  {cycle}")
