"""
FastAPI application for MSpread.

Provides REST API endpoints for creating, running, and analyzing
malware simulations.
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import json
import random


class NodeDefinition(BaseModel):
    count: int  # Number of nodes in this batch
    attributes: Dict  # Attributes to apply to nodes in this batch
    vulnerabilities: Optional[List[str]] = Field(None, description="List of CVEs present on these nodes", example=["CVE-2021-34527", "CVE-2023-9999"])
    
    class Config:
        json_schema_extra = {
            "example": {
                "count": 70,
                "attributes": {
                    "admin_user": True,
                    "device_type": "server",
                    "firewall_enabled": True,
                    "antivirus": True,
                    "patch_status": "fully_patched"
                },
                "vulnerabilities": ["CVE-2021-34527", "CVE-2023-9999"]
            }
        }


class NetworkConfig(BaseModel):
    """Configuration for network topology."""
    num_nodes: int = Field(100, description="Number of devices in the network (ignored for segmented topology)", example=100)
    network_type: str = Field("scale_free", description="Type of network topology: scale_free, small_world, random, complete, segmented", example="scale_free")
    device_attributes: Optional[Dict] = Field(None, description="Attributes to apply to ALL nodes uniformly", example={"os": "Windows Server 2019", "firewall_enabled": True})
    node_definitions: Optional[List[NodeDefinition]] = Field(None, description="Batch definitions for per-group device attributes (creates network segmentation)")
    node_distribution: str = Field("sequential", description="Distribution mode: 'sequential' (clusters devices by type) or 'random' (mixes device types throughout network)", example="random")
    subnets: Optional[List[Dict]] = Field(None, description="Subnet configurations for segmented topology")
    interconnects: Optional[List[Dict]] = Field(None, description="Inter-subnet connection configurations")
    
    class Config:
        json_schema_extra = {
            "example": {
                "num_nodes": 100,
                "network_type": "scale_free",
                "device_attributes": {
                    "os": "Windows 10"
                },
                "node_definitions": [
                    {"count": 70, "attributes": {"admin_user": True, "device_type": "server"}},
                    {"count": 30, "attributes": {"admin_user": False, "device_type": "workstation"}}
                ],
                "node_distribution": "random"
            }
        }


class MalwareConfig(BaseModel):
    malware_type: str = Field(..., description="Type of malware: worm, virus, ransomware, custom", example="worm")
    infection_rate: float = Field(0.5, description="Probability of infection spreading to each neighbor (0.0-1.0)", example=0.5, ge=0.0, le=1.0)
    latency: int = Field(1, description="Number of steps before infection can spread", example=1, ge=0)
    spread_pattern: str = Field("random", description="Spread pattern: 'random', 'bfs', 'dfs'", example="random")
    target_os: Optional[List[str]] = Field(None, description="List of target OS (e.g., ['windows', 'linux']) - if None, targets all", example=["windows"])
    target_node_types: Optional[List[str]] = Field(None, description="List of target node types - if None, targets all", example=["server"])
    avoids_admin: bool = Field(False, description="If True, cannot infect admin devices from non-admin devices", example=False)
    requires_interaction: bool = Field(False, description="If True, reduces effective infection rate (simulates user interaction)", example=False)
    bypass_firewall: bool = Field(False, description="If True, ignores firewall protections", example=False)
    zero_day: bool = Field(False, description="If True, can infect fully_patched systems", example=False)
    exploits: Optional[List[str]] = Field(None, description="List of CVEs this malware exploits", example=["CVE-2021-34527"])
    cve_only: bool = Field(False, description="If True, infection only occurs if a matching CVE is found (ignoring general infection rate)", example=False)
    
    class Config:
        json_schema_extra = {
            "example": {
                "malware_type": "worm",
                "infection_rate": 0.5,
                "latency": 1,
                "spread_pattern": "random",
                "avoids_admin": True,
                "bypass_firewall": False,
                "zero_day": False,
                "exploits": ["CVE-2021-34527"],
                "cve_only": True
            }
        }


class SimulationRequest(BaseModel):
    """Request body for running a simulation."""
    network_config: NetworkConfig = Field(..., description="Network topology configuration")
    malware_config: MalwareConfig = Field(..., description="Malware behavior configuration")
    initial_infected: List[str] = Field(..., description="List of initially infected device IDs", example=["device_0", "device_5"])
    max_steps: int = Field(100, description="Maximum simulation steps to run", example=50, ge=1)
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "summary": "Simple 70/30 Admin/Non-Admin Split",
                    "description": "Basic simulation with devices split into admin and non-admin groups",
                    "value": {
                        "network_config": {
                            "num_nodes": 100,
                            "network_type": "scale_free",
                            "node_definitions": [
                                {"count": 70, "attributes": {"admin_user": True, "device_type": "server"}},
                                {"count": 30, "attributes": {"admin_user": False, "device_type": "workstation"}}
                            ],
                            "node_distribution": "random"
                        },
                        "malware_config": {
                            "malware_type": "worm",
                            "infection_rate": 0.35,
                            "latency": 1
                        },
                        "initial_infected": ["device_0"],
                        "max_steps": 50
                    }
                },
                {
                    "summary": "Enterprise Three-Tier Network",
                    "description": "Realistic enterprise network with servers, admin workstations, and guest devices",
                    "value": {
                        "network_config": {
                            "num_nodes": 500,
                            "network_type": "scale_free",
                            "device_attributes": {
                                "os": "Windows",
                                "firewall_enabled": True
                            },
                            "node_definitions": [
                                {
                                    "count": 50,
                                    "attributes": {
                                        "device_type": "server",
                                        "admin_user": True,
                                        "antivirus": True,
                                        "patch_status": "fully_patched",
                                        "firewall_enabled": True
                                    }
                                },
                                {
                                    "count": 200,
                                    "attributes": {
                                        "device_type": "workstation",
                                        "admin_user": True,
                                        "antivirus": True,
                                        "patch_status": "patched"
                                    }
                                },
                                {
                                    "count": 250,
                                    "attributes": {
                                        "device_type": "workstation",
                                        "admin_user": False,
                                        "antivirus": False,
                                        "firewall_enabled": False,
                                        "patch_status": "unpatched"
                                    }
                                }
                            ],
                            "node_distribution": "random"
                        },
                        "malware_config": {
                            "malware_type": "worm",
                            "infection_rate": 0.35,
                            "latency": 1
                        },
                        "initial_infected": ["device_300"],
                        "max_steps": 100
                    }
                },
                {
                    "summary": "Mixed Operating Systems",
                    "description": "Network with Windows servers, Linux workstations, and mixed guest devices",
                    "value": {
                        "network_config": {
                            "num_nodes": 150,
                            "network_type": "scale_free",
                            "device_attributes": {
                                "firewall_enabled": True
                            },
                            "node_definitions": [
                                {
                                    "count": 50,
                                    "attributes": {
                                        "admin_user": True,
                                        "os": "Windows Server 2022",
                                        "device_type": "server",
                                        "antivirus": True
                                    }
                                },
                                {
                                    "count": 50,
                                    "attributes": {
                                        "admin_user": True,
                                        "os": "Linux Ubuntu 20.04",
                                        "device_type": "workstation",
                                        "antivirus": False
                                    }
                                },
                                {
                                    "count": 50,
                                    "attributes": {
                                        "admin_user": False,
                                        "os": "Windows 10",
                                        "device_type": "workstation",
                                        "antivirus": False
                                    }
                                }
                            ],
                            "node_distribution": "random"
                        },
                        "malware_config": {
                            "malware_type": "virus",
                            "infection_rate": 0.25,
                            "latency": 2
                        },
                        "initial_infected": ["device_0"],
                        "max_steps": 50
                    }
                },
                {
                    "summary": "Progressive Security Hardening",
                    "description": "Network showing impact of security layers: unprotected → antivirus → full protection",
                    "value": {
                        "network_config": {
                            "num_nodes": 120,
                            "network_type": "scale_free",
                            "node_definitions": [
                                {
                                    "count": 40,
                                    "attributes": {
                                        "admin_user": False,
                                        "firewall_enabled": False,
                                        "antivirus": False,
                                        "patch_status": "unpatched"
                                    }
                                },
                                {
                                    "count": 40,
                                    "attributes": {
                                        "admin_user": False,
                                        "firewall_enabled": False,
                                        "antivirus": True,
                                        "patch_status": "patched"
                                    }
                                },
                                {
                                    "count": 40,
                                    "attributes": {
                                        "admin_user": True,
                                        "firewall_enabled": True,
                                        "antivirus": True,
                                        "patch_status": "fully_patched"
                                    }
                                }
                            ],
                            "node_distribution": "random"
                        },
                        "malware_config": {
                            "malware_type": "ransomware",
                            "infection_rate": 0.30,
                            "latency": 3
                        },
                        "initial_infected": ["device_10"],
                        "max_steps": 50
                    }
                },
                {
                    "summary": "Sequential Distribution (Clustered)",
                    "description": "Devices grouped sequentially (not mixed) - shows impact of clustering on spread patterns",
                    "value": {
                        "network_config": {
                            "num_nodes": 100,
                            "network_type": "scale_free",
                            "node_definitions": [
                                {"count": 70, "attributes": {"admin_user": True}},
                                {"count": 30, "attributes": {"admin_user": False}}
                            ],
                            "node_distribution": "sequential"
                        },
                        "malware_config": {
                            "malware_type": "worm",
                            "infection_rate": 0.35,
                            "latency": 1
                        },
                        "initial_infected": ["device_0"],
                        "max_steps": 50
                    }
                },
                {
                    "summary": "Simple Homogeneous Network",
                    "description": "All devices identical - baseline for comparison",
                    "value": {
                        "network_config": {
                            "num_nodes": 50,
                            "network_type": "scale_free",
                            "device_attributes": {
                                "admin_user": True,
                                "device_type": "workstation",
                                "os": "Windows 11"
                            }
                        },
                        "malware_config": {
                            "malware_type": "worm",
                            "infection_rate": 0.35,
                            "latency": 1
                        },
                        "initial_infected": ["device_0"],
                        "max_steps": 50
                    }
                },
                {
                    "summary": "Multiple Initial Infections",
                    "description": "Simulation starting with multiple infected devices",
                    "value": {
                        "network_config": {
                            "num_nodes": 200,
                            "network_type": "small_world"
                        },
                        "malware_config": {
                            "malware_type": "virus",
                            "infection_rate": 0.25,
                            "latency": 2
                        },
                        "initial_infected": ["device_0", "device_50", "device_100", "device_150"],
                        "max_steps": 75
                    }
                }
            ]
        }


def _apply_node_definitions(network, node_definitions: List[NodeDefinition], distribution: str = "sequential") -> None:
    """
    Apply node definitions (batch logic) to assign attributes to groups of nodes.
    
    Args:
        network: NetworkGraph instance
        node_definitions: List of NodeDefinition objects specifying batches
        distribution: "sequential" (default) or "random"
            - "sequential": Devices assigned in order (device_0, device_1, ...)
            - "random": Devices randomly shuffled (mixes device types throughout network)
    """
    device_attr_pairs = []
    node_id = 0
    
    for definition in node_definitions:
        # Prepare attributes, converting vulnerabilities list to set for O(1) lookup
        attributes = definition.attributes.copy()
        if definition.vulnerabilities:
            attributes["vulnerabilities"] = set(definition.vulnerabilities)

        for _ in range(definition.count):
            device_id = f"device_{node_id}"
            device_attr_pairs.append((device_id, attributes))
            node_id += 1
    
    if distribution.lower() == "random":
        random.shuffle(device_attr_pairs)
    
    for device_id, attributes in device_attr_pairs:
        if device_id in network.graph.nodes():
            network.set_device_attributes(device_id, **attributes)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI application instance
    """
    app = FastAPI(
        title="MSpreadEngine API",
        description="Malware Spreading Simulation Engine - Simulate malware spread across network topologies",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
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
            from malware_engine.malware_base import Malware
            from simulation import Simulator

            network = NetworkGraph(network_type=request.network_config.network_type)
            network.generate_topology(
                request.network_config.num_nodes,
                device_attributes=request.network_config.device_attributes,
                subnets=request.network_config.subnets,
                interconnects=request.network_config.interconnects
            )

            if request.network_config.node_definitions:
                _apply_node_definitions(
                    network, 
                    request.network_config.node_definitions,
                    distribution=request.network_config.node_distribution
                )

            malware = Malware(
                malware_id="malware_1",
                malware_type=request.malware_config.malware_type,
                infection_rate=request.malware_config.infection_rate,
                latency=request.malware_config.latency,
                spread_pattern=request.malware_config.spread_pattern,
                target_os=request.malware_config.target_os,
                target_node_types=request.malware_config.target_node_types,
                avoids_admin=request.malware_config.avoids_admin,
                requires_interaction=request.malware_config.requires_interaction,
                bypass_firewall=request.malware_config.bypass_firewall,
                zero_day=request.malware_config.zero_day,
                exploits=request.malware_config.exploits,
                cve_only=request.malware_config.cve_only
            )

            simulator = Simulator(network, malware)
            simulator.initialize(request.initial_infected)
            simulator.run(max_steps=request.max_steps)

            return simulator.get_statistics()

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.websocket("/ws/simulate")
    async def websocket_simulate(websocket: WebSocket):
        """
        WebSocket endpoint for real-time simulation streaming.
        
        Supports interactive two-phase protocol:
        1. build_network -> Returns topology
        2. start_simulation -> Runs simulation
        
        Also supports legacy single-shot execution.
        """
        await websocket.accept()
        
        # Session state
        network = None
        
        try:
            while True:
                data = await websocket.receive_json()
                command = data.get("command")
                
                # Support legacy single-shot payload (backwards compatibility)
                if not command and "network_config" in data:
                    command = "legacy_run"
                
                # --- PHASE 1: BUILD NETWORK ---
                if command == "build_network" or command == "legacy_run":
                    from network_model import NetworkGraph
                    
                    network_config = data.get("network_config", {})
                    
                    network = NetworkGraph(network_type=network_config.get("network_type", "scale_free"))
                    network.generate_topology(
                        network_config.get("num_nodes", 100),
                        device_attributes=network_config.get("device_attributes", None),
                        subnets=network_config.get("subnets", None),
                        interconnects=network_config.get("interconnects", None)
                    )

                    if network_config.get("node_definitions"):
                        node_defs = [NodeDefinition(**d) for d in network_config.get("node_definitions", [])]
                        distribution = network_config.get("node_distribution", "sequential")
                        _apply_node_definitions(network, node_defs, distribution=distribution)

                    # Serialize topology for frontend visualization
                    nodes_data = []
                    # NetworkX .nodes(data=True) returns (node_id, attribute_dict)
                    for node_id, attrs in network.graph.nodes(data=True):
                        node_info = {"id": node_id}
                        # Pass relevant attributes to UI
                        for k, v in attrs.items():
                            if isinstance(v, (str, int, float, bool)):
                                node_info[k] = v
                            elif isinstance(v, set):
                                node_info[k] = list(v)
                        nodes_data.append(node_info)
                        
                    links_data = []
                    for u, v, data in network.graph.edges(data=True):
                        link = {"source": u, "target": v}
                        for k, v_attr in data.items():
                            if isinstance(v_attr, (str, int, float, bool)):
                                link[k] = v_attr
                        links_data.append(link)

                    await websocket.send_json({
                        "type": "network_ready",
                        "total_nodes": network.graph.number_of_nodes(),
                        "topology": {
                            "nodes": nodes_data,
                            "links": links_data
                        }
                    })

                # --- PHASE 2: START SIMULATION ---
                if command == "start_simulation" or command == "legacy_run":
                    from malware_engine.malware_base import Malware
                    from simulation import Simulator
                    
                    if not network:
                        await websocket.send_json({"type": "error", "message": "Network not built. Send 'build_network' first."})
                        continue

                    malware_config = data.get("malware_config", {})
                    initial_infected = data.get("initial_infected", [])
                    max_steps = data.get("max_steps", 100)

                    malware = Malware(
                        malware_id="malware_1",
                        malware_type=malware_config.get("malware_type", "custom"),
                        infection_rate=malware_config.get("infection_rate", 0.5),
                        latency=malware_config.get("latency", 1),
                        spread_pattern=malware_config.get("spread_pattern", "random"),
                        target_os=malware_config.get("target_os"),
                        target_node_types=malware_config.get("target_node_types"),
                        avoids_admin=malware_config.get("avoids_admin", False),
                        requires_interaction=malware_config.get("requires_interaction", False),
                        bypass_firewall=malware_config.get("bypass_firewall", False),
                        zero_day=malware_config.get("zero_day", False),
                        exploits=malware_config.get("exploits"),
                        cve_only=malware_config.get("cve_only", False)
                    )

                    simulator = Simulator(network, malware)
                    simulator.initialize(initial_infected)

                    await websocket.send_json({
                        "type": "initialized",
                        "total_devices": network.graph.number_of_nodes(),
                        "initial_infected": len(initial_infected),
                    })

                    for step_num in range(max_steps):
                        step_data = simulator.step()

                        await websocket.send_json({
                            "type": "step",
                            "step": step_data["step"],
                            "newly_infected": step_data["newly_infected"],
                            "total_infected": step_data["total_infected"],
                            "devices_infected": step_data["devices_infected"],
                        })

                        if (step_data["newly_infected"] == 0 and 
                            simulator.current_step > malware.latency):
                            break

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
