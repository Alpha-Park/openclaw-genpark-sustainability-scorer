# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Sustainability Scorer MCP Server
FastMCP standard interface for carbon footprint calculation and packaging circularity audits.
"""

import json
from typing import Dict, Any, List
from client import OpenClawGenParkSustainabilityScorer

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("openclaw-genpark-sustainability-scorer")
except ImportError:
    class MockFastMCP:
        def __init__(self, name):
            self.name = name
        def tool(self):
            def decorator(f):
                return f
            return decorator
    mcp = MockFastMCP("openclaw-genpark-sustainability-scorer")

scorer = OpenClawGenParkSustainabilityScorer()

@mcp.tool()
def calculate_cradle_to_gate_carbon_footprint(
    bill_of_materials: List[Dict[str, Any]],
    transport_distance_km: float = 1200.0,
    transport_mode: str = "road_freight"
) -> str:
    """
    Estimates total cradle-to-gate carbon footprint from bill of materials and logistics.
    """
    res = scorer.calculate_cradle_to_gate_carbon_footprint(bill_of_materials, transport_distance_km, transport_mode)
    return json.dumps(res, indent=2)

@mcp.tool()
def evaluate_packaging_circularity_ratio(
    packaging_components: List[Dict[str, Any]]
) -> str:
    """
    Calculates Material Circularity Indicator based on recycled content and recyclability.
    """
    res = scorer.evaluate_packaging_circularity_ratio(packaging_components)
    return json.dumps(res, indent=2)

@mcp.tool()
def optimize_esg_carbon_credit_allocation(
    unmitigated_co2e_tonnes: float,
    available_credits: List[Dict[str, Any]],
    budget_usd: float
) -> str:
    """
    Greedy cost-effective portfolio allocation of carbon offset projects.
    """
    res = scorer.optimize_esg_carbon_credit_allocation(unmitigated_co2e_tonnes, available_credits, budget_usd)
    return json.dumps(res, indent=2)

def main():
    print("Testing Sustainability Scorer:")
    bom = [{"material": "aluminum", "weight_kg": 0.5}, {"material": "paper_cardboard", "weight_kg": 0.2}]
    print(calculate_cradle_to_gate_carbon_footprint(bom, 800.0))

if __name__ == "__main__":
    main()
