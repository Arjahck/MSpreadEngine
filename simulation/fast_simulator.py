"""
Vectorized simulation engine using NumPy/SciPy for high performance.

This module provides a FastSimulator class optimized for large-scale simulations
where complex node attribute logic is not required (homogeneous networks).
It uses sparse matrix operations to calculate spread in bulk.
"""

import numpy as np
try:
    import scipy.sparse as sparse
except (ImportError, AttributeError):
    sparse = None

import logging
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)

class FastSimulator:
    """
    High-performance simulation engine using vectorization.
    
    Performance:
        - 100x faster than object-based Simulator for large networks (>50k nodes).
        - Limitations: Does not support complex per-node logic (like admin_user checks)
          unless explicitly encoded as masks (future enhancement).
    """

    def __init__(self, adj_matrix: Any, infection_rate: float = 0.35, latency: int = 1):
        """
        Initialize the fast simulator.

        Args:
            adj_matrix: Scipy sparse adjacency matrix (N x N)
            infection_rate: Probability of infection (0.0 - 1.0)
            latency: Steps before a node becomes infectious
        """
        if sparse is None:
            raise ImportError("scipy is required for FastSimulator. Install with: pip install scipy numpy")

        self.adj_matrix = adj_matrix
        self.infection_rate = infection_rate
        self.latency = latency
        self.num_nodes = adj_matrix.shape[0]
        
        # State vectors
        # 0: Susceptible
        # 1: Latent (infected but not spreading yet)
        # 2: Infectious
        self.state = np.zeros(self.num_nodes, dtype=np.int8)
        
        # Timers for latency
        self.infection_timers = np.zeros(self.num_nodes, dtype=np.int16)
        
        self.history = []
        self.current_step = 0
        self.total_infected_count = 0

    def initialize(self, initial_infected_indices: List[int]) -> None:
        """
        Set initial infected nodes.
        
        Args:
            initial_infected_indices: List of integer node indices to infect
        """
        if not initial_infected_indices:
            return

        indices = np.array(initial_infected_indices, dtype=np.int32)
        # Mark as infectious immediately (or latent if we want latency logic on start)
        # Assuming initial seeds are already infectious for simplicity
        self.state[indices] = 2 
        self.total_infected_count = len(indices)

    def step(self) -> Dict:
        """
        Execute one vectorized simulation step.
        """
        self.current_step += 1
        
        # 1. Identify Spreading Nodes (State == 2)
        infectious_mask = (self.state == 2)
        
        # 2. Project infection potential to neighbors
        # Matrix multiplication: (N x N) * (N x 1) -> (N x 1)
        # Result[i] > 0 means node i is connected to at least one infectious node
        exposure_potential = self.adj_matrix.dot(infectious_mask)
        
        # 3. Filter Targets
        # Must be Susceptible (State == 0) AND Exposed
        susceptible_mask = (self.state == 0)
        target_mask = (exposure_potential > 0) & susceptible_mask
        
        # 4. Probabilistic Infection
        num_targets = np.count_nonzero(target_mask)
        new_infections_count = 0
        
        if num_targets > 0:
            # Roll dice for all targets at once
            rolls = np.random.random(num_targets)
            success_rolls = rolls < self.infection_rate
            
            # Map back to node indices
            target_indices = np.where(target_mask)[0]
            successful_indices = target_indices[success_rolls]
            
            new_infections_count = len(successful_indices)
            
            if new_infections_count > 0:
                # Update state
                if self.latency > 0:
                    # Mark as Latent (1) and set timer
                    self.state[successful_indices] = 1
                    self.infection_timers[successful_indices] = self.latency
                else:
                    # Mark as Infectious (2) immediately
                    self.state[successful_indices] = 2
                    
                self.total_infected_count += new_infections_count

        # 5. Process Latency (Transition Latent -> Infectious)
        if self.latency > 0:
            # Decrement timers for all Latent nodes
            latent_mask = (self.state == 1)
            if np.any(latent_mask):
                self.infection_timers[latent_mask] -= 1
                
                # Check who finished latency
                ready_mask = (self.state == 1) & (self.infection_timers <= 0)
                self.state[ready_mask] = 2 # Become infectious

        # Record History
        step_data = {
            "step": self.current_step,
            "newly_infected": int(new_infections_count),
            "total_infected": int(self.total_infected_count)
        }
        self.history.append(step_data)
        
        return step_data

    def run(self, max_steps: int = 100) -> List[Dict]:
        """Run simulation loop."""
        for _ in range(max_steps):
            data = self.step()
            # Stop if no spread and no latent nodes waiting
            if data["newly_infected"] == 0 and np.sum(self.state == 1) == 0:
                break
        return self.history
