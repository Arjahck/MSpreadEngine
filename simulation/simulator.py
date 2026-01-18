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
        self.network = network
        self.malware = malware
        
        self.malware.network = network
        
        self.current_step = 0
        self.history = []
        self.infection_timeline = {}

    def initialize(self, initial_infected: List[str]) -> None:
        """Initialize the simulation with initially infected devices."""
        for device_id in initial_infected:
            self.malware.mark_infected(device_id)
            self.infection_timeline[device_id] = 0

    def step(self) -> Dict:
        """Execute one simulation time step."""
        self.current_step += 1
        newly_infected = []

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
        """Run the simulation for a specified number of steps."""
        for _ in range(max_steps):
            if stop_condition and stop_condition(self):
                break

            step_data = self.step()

            if step_data["newly_infected"] == 0 and self.current_step > self.malware.latency:
                break

        return self.history

    def get_statistics(self) -> Dict:
        """Returns comprehensive simulation statistics including speed, attribute analysis, and network topology."""
        total_devices = self.network.graph.number_of_nodes()
        infected_count = self.malware.get_infected_count()
        
        # Get base network statistics
        network_stats = self.network.get_statistics(skip_expensive=True)
        
        # Calculate Peak Velocity (Speed)
        new_infections = [step['newly_infected'] for step in self.history]
        peak_velocity = max(new_infections) if new_infections else 0
        step_at_peak = new_infections.index(peak_velocity) + 1 if peak_velocity > 0 else 0
        
        # Calculate Time to Saturation (Milestones)
        steps_to_50 = None
        steps_to_90 = None
        for step in self.history:
            ratio = step['total_infected'] / total_devices if total_devices > 0 else 0
            if ratio >= 0.5 and steps_to_50 is None:
                steps_to_50 = step['step']
            if ratio >= 0.9 and steps_to_90 is None:
                steps_to_90 = step['step']

        # Infected Attribute Breakdown
        infected_os_counts = {}
        for device_id in self.malware.infected_devices:
            try:
                attrs = self.network.get_device_attributes(device_id)
                os = str(attrs.get('os', 'Unknown'))
                infected_os_counts[os] = infected_os_counts.get(os, 0) + 1
            except:
                pass

        return {
            "total_steps": self.current_step,
            "total_devices": total_devices,
            "total_infected": infected_count,
            "infection_percentage": (infected_count / total_devices * 100) if total_devices > 0 else 0,
            "malware_type": self.malware.malware_type.value if hasattr(self.malware.malware_type, 'value') else str(self.malware.malware_type),
            "network_topology": network_stats,
            "performance": {
                "peak_velocity": peak_velocity,
                "step_at_peak": step_at_peak,
                "steps_to_50_percent": steps_to_50,
                "steps_to_90_percent": steps_to_90
            },
            "infected_demographics": {
                "os_breakdown": infected_os_counts
            },
            "history": self.history
        }

    def reset(self) -> None:
        self.current_step = 0
        self.history = []
        self.infection_timeline = {}
        self.malware.infected_devices.clear()
