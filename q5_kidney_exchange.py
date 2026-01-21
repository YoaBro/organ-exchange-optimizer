
import networkx as nx
import pulp
import random
import time

def find_kidney_exchange(g):
    """
    gets a directed graph where nodes = patient-donor pairs
    edge a->b means donor of a can give to patient of b
    returns max set of disjoint cycles (len 2 or 3) to maximize transplants
    """
    
    # first find all cycles of length 2 and 3
    cycles = []
    seen = set()
    
    # cycles of length 2 - mutual exchange
    for u, v in g.edges():
        if g.has_edge(v, u):
            c = tuple(sorted([u, v]))
            if c not in seen:
                seen.add(c)
                cycles.append([u, v])

    # cycles of length 3
    for u in g.nodes():
        for v in g.successors(u):
            if v == u:
                continue
            for w in g.successors(v):
                if w == u or w == v:
                    continue
                if g.has_edge(w, u):  # closes the cycle
                    c = tuple(sorted([u, v, w]))
                    if c not in seen:
                        seen.add(c)
                        cycles.append([u, v, w])

    # now build ILP
    # maximize sum of cycle lengths (= number of patients helped)
    # constraint: each node in at most one cycle
    
    prob = pulp.LpProblem("kidney", pulp.LpMaximize)
    
    # x_i = 1 if we pick cycle i
    x = {}
    for i in range(len(cycles)):
        x[i] = pulp.LpVariable(f"x{i}", cat='Binary')

    # objective - maximize total patients
    prob += pulp.lpSum(len(cycles[i]) * x[i] for i in range(len(cycles)))

    # each node appears in at most one selected cycle
    for node in g.nodes():
        relevant = [i for i in range(len(cycles)) if node in cycles[i]]
        if len(relevant) > 0:
            prob += pulp.lpSum(x[i] for i in relevant) <= 1

    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    # get results
    result = []
    total = 0
    for i in range(len(cycles)):
        if pulp.value(x[i]) == 1:
            result.append(cycles[i])
            total += len(cycles[i])
            
    return result, total


def generate_random_graph(n, p):
    """generate random directed graph with n nodes, edge prob p"""
    g = nx.DiGraph()
    g.add_nodes_from(range(n))
    for i in range(n):
        for j in range(n):
            if i != j and random.random() < p:
                g.add_edge(i, j)
    return g


if __name__ == "__main__":
    # part a - basic test
    print("=== Part A: Basic Test ===")
    G = nx.DiGraph()
    
    # cycle of 2: 0 <-> 1
    G.add_edge(0, 1)
    G.add_edge(1, 0)
    
    # cycle of 3: 2 -> 3 -> 4 -> 2
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 2)
    
    # extra edge that doesnt form a new cycle
    G.add_edge(1, 2)

    cycles, num = find_kidney_exchange(G)
    print(f"transplants: {num}")
    print("cycles found:")
    for c in cycles:
        print("  ", c)
    
    # part b - test on random graphs with increasing size
    print("\n=== Part B: Random Graphs (max 60 sec) ===")
    
    edge_prob = 0.3
    max_n = 0
    
    # start from small and increase
    for n in [10, 20, 30, 50, 75, 100, 150, 200, 250, 300, 400, 500]:
        g = generate_random_graph(n, edge_prob)
        
        start = time.time()
        cycles, num = find_kidney_exchange(g)
        elapsed = time.time() - start
        
        print(f"n={n}: {num} transplants, time={elapsed:.2f}s")
        
        if elapsed <= 60:
            max_n = n
        else:
            print(f"exceeded 60 seconds at n={n}")
            break
    
    print(f"\nlargest n that finishes in under 1 minute: {max_n}")
