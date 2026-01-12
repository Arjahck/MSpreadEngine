"""
FastAPI application for MSpread.

Provides REST API endpoints for creating, running, and analyzing
malware simulations.
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
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

    # Add CORS middleware to allow cross-origin requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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

    @app.websocket("/ws/simulate")
    async def websocket_simulate(websocket: WebSocket):
        """
        WebSocket endpoint for real-time simulation streaming.
        
        Receives simulation configuration and streams step-by-step updates.
        """
        await websocket.accept()
        try:
            # Receive simulation configuration from client
            data = await websocket.receive_json()
            
            from network_model import NetworkGraph
            from malware_engine.malware_base import Worm, Virus, Ransomware
            from simulation import Simulator

            # Parse configuration
            network_config = data.get("network_config", {})
            malware_config = data.get("malware_config", {})
            initial_infected = data.get("initial_infected", [])
            max_steps = data.get("max_steps", 100)

            # Create network
            network = NetworkGraph(network_type=network_config.get("network_type", "scale_free"))
            network.generate_topology(network_config.get("num_nodes", 100))

            # Create malware
            malware_type = malware_config.get("malware_type", "worm").lower()
            if malware_type == "worm":
                malware = Worm(
                    "malware_1",
                    infection_rate=malware_config.get("infection_rate", 0.3),
                    latency=malware_config.get("latency", 1),
                )
            elif malware_type == "virus":
                malware = Virus(
                    "malware_1",
                    infection_rate=malware_config.get("infection_rate", 0.3),
                    latency=malware_config.get("latency", 1),
                )
            elif malware_type == "ransomware":
                malware = Ransomware(
                    "malware_1",
                    infection_rate=malware_config.get("infection_rate", 0.3),
                    latency=malware_config.get("latency", 1),
                )
            else:
                raise ValueError(f"Unknown malware type: {malware_type}")

            # Initialize simulator
            simulator = Simulator(network, malware)
            simulator.initialize(initial_infected)

            # Send initial state
            await websocket.send_json({
                "type": "initialized",
                "total_devices": network.graph.number_of_nodes(),
                "initial_infected": len(initial_infected),
            })

            # Run simulation and stream updates
            for step_num in range(max_steps):
                step_data = simulator.step()

                # Send step update to client
                await websocket.send_json({
                    "type": "step",
                    "step": step_data["step"],
                    "newly_infected": step_data["newly_infected"],
                    "total_infected": step_data["total_infected"],
                    "devices_infected": step_data["devices_infected"],
                })

                # Stop if no new infections after latency period
                if (step_data["newly_infected"] == 0 and 
                    simulator.current_step > malware.latency):
                    break

            # Send final statistics
            stats = simulator.get_statistics()
            await websocket.send_json({
                "type": "complete",
                "statistics": stats,
            })

        except WebSocketDisconnect:
            print("Client disconnected")
        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "message": str(e),
            })
            await websocket.close(code=1008)

    return app
