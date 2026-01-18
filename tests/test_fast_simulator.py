"""
Unit tests for the vectorized FastSimulator.
"""

import unittest
import numpy as np
try:
    import scipy.sparse as sparse
    HAS_SCIPY = True
except (ImportError, AttributeError):
    HAS_SCIPY = False

from simulation.fast_simulator import FastSimulator

class TestFastSimulator(unittest.TestCase):
    
    def setUp(self):
        if not HAS_SCIPY:
            self.skipTest("SciPy not installed")
            
        # Create a simple 5-node line graph: 0-1-2-3-4
        # Adjacency matrix (5x5)
        # 0 connected to 1
        # 1 connected to 0, 2
        # ...
        data = [1, 1, 1, 1, 1, 1, 1, 1]
        row = [0, 1, 1, 2, 2, 3, 3, 4]
        col = [1, 0, 2, 1, 3, 2, 4, 3]
        self.adj = sparse.csr_matrix((data, (row, col)), shape=(5, 5))

    def test_initialization(self):
        sim = FastSimulator(self.adj, infection_rate=1.0)
        sim.initialize([0])
        
        # Check initial state
        self.assertEqual(sim.state[0], 2) # Node 0 is Infectious
        self.assertEqual(sim.state[1], 0) # Node 1 is Susceptible
        self.assertEqual(sim.total_infected_count, 1)

    def test_propagation_no_latency(self):
        # 100% infection rate, 0 latency
        sim = FastSimulator(self.adj, infection_rate=1.0, latency=0)
        sim.initialize([0])
        
        # Step 1: 0 infects 1
        sim.step()
        self.assertEqual(sim.state[1], 2)
        self.assertEqual(sim.total_infected_count, 2)
        
        # Step 2: 1 infects 2 (0 infects 1 again but no-op)
        sim.step()
        self.assertEqual(sim.state[2], 2)
        self.assertEqual(sim.total_infected_count, 3)

    def test_propagation_with_latency(self):
        # 100% infection, 1 step latency
        sim = FastSimulator(self.adj, infection_rate=1.0, latency=1)
        sim.initialize([0]) # 0 is Infectious
        
        # Step 1: 0 exposes 1. 1 becomes Latent (1)
        sim.step()
        self.assertEqual(sim.state[1], 1)
        self.assertEqual(sim.total_infected_count, 2)
        
        # Step 2: 1 finishes latency -> Infectious. 
        # But 1 was NOT infectious during step calculation, so 2 is NOT exposed yet.
        sim.step()
        self.assertEqual(sim.state[1], 2) # Now infectious
        self.assertEqual(sim.state[2], 0) # Still susceptible
        
        # Step 3: 1 exposes 2. 2 becomes Latent
        sim.step()
        self.assertEqual(sim.state[2], 1)

    def test_probabilistic_spread(self):
        # 0% infection rate
        sim = FastSimulator(self.adj, infection_rate=0.0)
        sim.initialize([0])
        
        sim.step()
        self.assertEqual(sim.state[1], 0) # Should not infect
        self.assertEqual(sim.total_infected_count, 1)

    def test_run_loop(self):
        sim = FastSimulator(self.adj, infection_rate=1.0, latency=0)
        sim.initialize([0])
        
        history = sim.run(max_steps=10)
        
        # Should infect all 5 nodes eventually (0->1->2->3->4 takes 4 steps)
        self.assertEqual(sim.total_infected_count, 5)
        self.assertTrue(len(history) >= 4)

if __name__ == "__main__":
    unittest.main()
