"""
FastAPI application for MSpread.

Provides REST API endpoints for creating, running, and analyzing
malware simulations.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import json


class NetworkConfig(BaseModel):
    """Configuration for network topology."""
    num_nodes: int
    network_type: str = "scale_free"


class MalwareConfig(BaseModel):
    """Configuration for malware."""
    malware_type: str
    infection_rate: float = 0.3
    latency: int = 1


class SimulationRequest(BaseModel):
    """Request body for running a simulation."""
    network_config: NetworkConfig
    malware_config: MalwareConfig
    initial_infected: List[str]
    max_steps: int = 100


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI application instance
    """
    app = FastAPI(
        title="MSpreadEngine API",
        description="Malware Spreading Simulation Engine",
        version="0.1.0",
    )

    @app.get("/")
    def read_root() -> Dict:
        """Root endpoint."""
        return {
            "name": "MSpreadEngine",
            "description": "Malware Spreading Simulation Engine",
            "version": "0.1.0",
        }

    @app.get("/health")
    def health_check() -> Dict:
        """Health check endpoint."""
        return {"status": "healthy"}

    @app.post("/api/v1/simulate")
    def run_simulation(request: SimulationRequest) -> Dict:
        """
        Run a malware simulation.

        Args:
            request: Simulation request configuration

        Returns:
            Simulation results
        """
        try:
            from network_model import NetworkGraph
            from malware_engine.malware_base import Malware, Worm, Virus, Ransomware
            from simulation import Simulator

            # Create network
            network = NetworkGraph(network_type=request.network_config.network_type)
            network.generate_topology(request.network_config.num_nodes)

            # Create malware
            malware_type = request.malware_config.malware_type.lower()
            if malware_type == "worm":
                malware = Worm(
                    "malware_1",
                    infection_rate=request.malware_config.infection_rate,
                    latency=request.malware_config.latency,
                )
            elif malware_type == "virus":
                malware = Virus(
                    "malware_1",
                    infection_rate=request.malware_config.infection_rate,
                    latency=request.malware_config.latency,
                )
            elif malware_type == "ransomware":
                malware = Ransomware(
                    "malware_1",
                    infection_rate=request.malware_config.infection_rate,
                    latency=request.malware_config.latency,
                )
            else:
                raise ValueError(f"Unknown malware type: {malware_type}")

            # Run simulation
            simulator = Simulator(network, malware)
            simulator.initialize(request.initial_infected)
            simulator.run(max_steps=request.max_steps)

            return simulator.get_statistics()

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/v1/network/stats")
    def get_network_stats() -> Dict:
        """Get network statistics."""
        return {"status": "not implemented"}

    return app
