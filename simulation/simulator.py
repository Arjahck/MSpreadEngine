"""
Core simulation engine for malware propagation.

This module handles the main simulation loop and state updates over time.
"""

from typing import Dict, List, Optional

try:
    from network_model import NetworkGraph
    from malware_engine.malware_base import Malware
except ImportError:
    from ..network_model import NetworkGraph
    from ..malware_engine.malware_base import Malware


class Simulator:

    def __init__(self, network: NetworkGraph, malware: Malware):
        """
        Args:
            network: NetworkGraph instance
            malware: Malware instance
        """
        self.network = network
        self.malware = malware
        self.current_step = 0
        self.history = []
        self.infection_timeline = {}

    def initialize(self, initial_infected: List[str]) -> None:
        """
        Initialize the simulation with initially infected devices.

        Args:
            initial_infected: List of initially infected device IDs
        """
        for device_id in initial_infected:
            self.malware.mark_infected(device_id)
            self.infection_timeline[device_id] = 0

    def step(self) -> Dict:
        """
        Execute one simulation time step.

        Returns:
            Dictionary with step information (newly infected, total infected, etc.)
        """
        self.current_step += 1
        newly_infected = []

        # Process each infected device
        for infected_device in list(self.malware.infected_devices):
            neighbors = self.network.get_neighbors(infected_device)
            newly_infected_neighbors = self.malware.spread(infected_device, neighbors)

            for device in newly_infected_neighbors:
                if device not in self.malware.infected_devices:
                    self.malware.mark_infected(device)
                    self.infection_timeline[device] = self.current_step
                    newly_infected.append(device)

        step_data = {
            "step": self.current_step,
            "newly_infected": len(newly_infected),
            "total_infected": self.malware.get_infected_count(),
            "devices_infected": newly_infected,
        }

        self.history.append(step_data)
        return step_data

    def run(self, max_steps: int = 100, stop_condition: Optional[callable] = None) -> List[Dict]:
        """
        Run the simulation for a specified number of steps.

        Args:
            max_steps: Maximum number of simulation steps
            stop_condition: Optional callable that returns True to stop simulation

        Returns:
            List of step data dictionaries
        """
        for _ in range(max_steps):
            if stop_condition and stop_condition(self):
                break

            step_data = self.step()

            # Stop if no new infections
            if step_data["newly_infected"] == 0 and self.current_step > self.malware.latency:
                break

        return self.history

    def get_statistics(self) -> Dict:
        """
        Returns:
            Dictionary with simulation statistics
        """
        total_devices = self.network.graph.number_of_nodes()
        infected_count = self.malware.get_infected_count()

        return {
            "total_steps": self.current_step,
            "total_devices": total_devices,
            "total_infected": infected_count,
            "infection_percentage": (infected_count / total_devices * 100) if total_devices > 0 else 0,
            "malware_type": self.malware.malware_type.value,
            "history": self.history,
        }

    def reset(self) -> None:
        self.current_step = 0
        self.history = []
        self.infection_timeline = {}
        self.malware.infected_devices.clear()
