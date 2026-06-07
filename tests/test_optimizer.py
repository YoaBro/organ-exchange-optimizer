"""Unit tests for organ exchange optimizer"""

import unittest
import networkx as nx
from organ_exchange_optimizer import find_organ_exchange, generate_random_graph


class TestOrganExchangeOptimizer(unittest.TestCase):
    """Test cases for the organ exchange optimizer"""
    
    def test_simple_2cycle(self):
        """Test basic 2-cycle (mutual exchange)"""
        G = nx.DiGraph()
        G.add_edge(0, 1)
        G.add_edge(1, 0)
        
        cycles, total = find_organ_exchange(G)
        
        self.assertEqual(total, 2)
        self.assertEqual(len(cycles), 1)
        self.assertIn([0, 1], cycles)
    
    def test_simple_3cycle(self):
        """Test basic 3-cycle"""
        G = nx.DiGraph()
        G.add_edge(0, 1)
        G.add_edge(1, 2)
        G.add_edge(2, 0)
        
        cycles, total = find_organ_exchange(G)
        
        self.assertEqual(total, 3)
        self.assertEqual(len(cycles), 1)
    
    def test_multiple_disjoint_cycles(self):
        """Test multiple disjoint cycles"""
        G = nx.DiGraph()
        # First 2-cycle: 0 <-> 1
        G.add_edge(0, 1)
        G.add_edge(1, 0)
        # Second 2-cycle: 2 <-> 3
        G.add_edge(2, 3)
        G.add_edge(3, 2)
        
        cycles, total = find_organ_exchange(G)
        
        self.assertEqual(total, 4)
        self.assertEqual(len(cycles), 2)
    
    def test_no_cycles(self):
        """Test graph with no cycles"""
        G = nx.DiGraph()
        G.add_edge(0, 1)
        G.add_edge(1, 2)
        # No cycles possible
        
        cycles, total = find_organ_exchange(G)
        
        self.assertEqual(total, 0)
        self.assertEqual(len(cycles), 0)
    
    def test_complex_case(self):
        """Test complex case with multiple cycles"""
        G = nx.DiGraph()
        # 2-cycle: 0 <-> 1
        G.add_edge(0, 1)
        G.add_edge(1, 0)
        # 3-cycle: 2 -> 3 -> 4 -> 2
        G.add_edge(2, 3)
        G.add_edge(3, 4)
        G.add_edge(4, 2)
        # Extra edge
        G.add_edge(1, 2)
        
        cycles, total = find_organ_exchange(G)
        
        self.assertEqual(total, 5)
        self.assertEqual(len(cycles), 2)
    
    def test_generate_random_graph(self):
        """Test random graph generation"""
        G = generate_random_graph(n=10, p=0.5)
        
        self.assertEqual(G.number_of_nodes(), 10)
        self.assertIsInstance(G, nx.DiGraph)
        # With p=0.5 and 10 nodes, expect roughly 45 edges (n*(n-1)*p)
        self.assertGreater(G.number_of_edges(), 20)
        self.assertLess(G.number_of_edges(), 80)
    
    def test_single_node(self):
        """Test with single node (no self-loops expected)"""
        G = nx.DiGraph()
        G.add_node(0)
        
        cycles, total = find_organ_exchange(G)
        
        self.assertEqual(total, 0)
        self.assertEqual(len(cycles), 0)
    
    def test_empty_graph(self):
        """Test with empty graph"""
        G = nx.DiGraph()
        
        cycles, total = find_organ_exchange(G)
        
        self.assertEqual(total, 0)
        self.assertEqual(len(cycles), 0)


if __name__ == '__main__':
    unittest.main()
