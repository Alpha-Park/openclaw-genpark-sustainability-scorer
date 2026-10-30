# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Sustainability Scorer Client
Pure Python Standard Library (Zero External Dependencies)
Implements cradle-to-gate LCA carbon footprint estimation, packaging circularity recyclability ratio,
and ESG carbon credit offset linear optimization.
"""

import math
from typing import Dict, Any, List, Optional

class OpenClawGenParkSustainabilityScorer:
    """
    Environmental Life Cycle Assessment (LCA) and circularity auditing engine for commerce agents.
    """

    def __init__(self):
        # Default emission factors (kg CO2e per kg material)
        self.emission_factors = {
            "aluminum": 8.2,
            "steel": 1.9,
            "plastic_virgin": 3.1,
            "plastic_recycled": 0.8,
            "cotton_organic": 1.6,
            "cotton_conventional": 5.9,
            "paper_cardboard": 0.9,
            "glass": 0.85,
            "electronics_pcba": 42.0
        }

    def calculate_cradle_to_gate_carbon_footprint(
        self,
        bill_of_materials: List[Dict[str, Any]],
        transport_distance_km: float = 1200.0,
        transport_mode: str = "road_freight"
    ) -> Dict[str, Any]:
        """
        Estimates total cradle-to-gate carbon footprint:
          Emissions = sum( weight_kg * emission_factor ) + ( total_weight * distance_km * transport_ef )
        """
        material_emissions = 0.0
        total_weight_kg = 0.0
        breakdown = []

        for item in bill_of_materials:
            mat = item.get("material", "plastic_virgin").lower()
            weight = max(0.001, float(item.get("weight_kg", 0.1)))
            ef = self.emission_factors.get(mat, 2.5)

            item_co2 = weight * ef
            material_emissions += item_co2
            total_weight_kg += weight

            breakdown.append({
                "material": mat,
                "weight_kg": round(weight, 3),
                "emission_factor_kg_co2e_per_kg": ef,
                "co2e_kg": round(item_co2, 3)
            })

        # Transport emission factor per tonne-km
        transport_ef_map = {
            "air_freight": 0.602,
            "road_freight": 0.096,
            "rail_freight": 0.028,
            "sea_freight": 0.015
        }
        t_ef = transport_ef_map.get(transport_mode.lower(), 0.096)
        transport_co2 = (total_weight_kg / 1000.0) * transport_distance_km * t_ef

        total_co2e = material_emissions + transport_co2

        if total_co2e <= 5.0:
            rating = "A_ECO_OPTIMAL"
        elif total_co2e <= 25.0:
            rating = "B_LOW_IMPACT"
        elif total_co2e <= 75.0:
            rating = "C_MODERATE_IMPACT"
        else:
            rating = "D_HIGH_CARBON_INTENSIVE"

        return {
            "total_weight_kg": round(total_weight_kg, 3),
            "total_co2e_kg": round(total_co2e, 3),
            "material_co2e_kg": round(material_emissions, 3),
            "transport_co2e_kg": round(transport_co2, 3),
            "sustainability_rating": rating,
            "material_breakdown": breakdown
        }

    def evaluate_packaging_circularity_ratio(
        self,
        packaging_components: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculates Material Circularity Indicator (MCI) approximation based on post-consumer recycled (PCR) content
        and end-of-life recyclability percentage:
          Circularity = sum( weight * (0.5 * pcr_pct + 0.5 * recyclable_pct) ) / total_weight
        """
        if not packaging_components:
            return {"circularity_ratio": 0.0, "classification": "NO_PACKAGING_DATA"}

        weighted_circularity = 0.0
        total_weight = 0.0

        for comp in packaging_components:
            weight = max(0.001, float(comp.get("weight_grams", 10.0)))
            pcr = min(100.0, max(0.0, float(comp.get("recycled_content_pct", 0.0))))
            recyc = min(100.0, max(0.0, float(comp.get("recyclable_pct", 0.0))))

            comp_score = (0.5 * pcr + 0.5 * recyc) / 100.0
            weighted_circularity += weight * comp_score
            total_weight += weight

        circularity_ratio = round(weighted_circularity / max(0.001, total_weight), 4)

        if circularity_ratio >= 0.85:
            classification = "FULLY_CIRCULAR_CLOSED_LOOP"
        elif circularity_ratio >= 0.60:
            classification = "HIGHLY_CIRCULAR_TRANSITIONAL"
        elif circularity_ratio >= 0.30:
            classification = "PARTIALLY_RECYCLABLE"
        else:
            classification = "LINEAR_TAKEMAKEWASTE"

        return {
            "total_packaging_weight_grams": round(total_weight, 2),
            "circularity_ratio": circularity_ratio,
            "circularity_percentage": round(circularity_ratio * 100.0, 2),
            "classification": classification
        }

    def optimize_esg_carbon_credit_allocation(
        self,
        unmitigated_co2e_tonnes: float,
        available_credits: List[Dict[str, Any]],
        budget_usd: float
    ) -> Dict[str, Any]:
        """
        Greedy cost-effective portfolio allocation of carbon offset projects (Gold Standard, Verra, Biochar)
        maximizing offset tonnes within the defined ESG budget.
        """
        # Sort credits by price per tonne ascending
        sorted_credits = sorted(available_credits, key=lambda c: float(c.get("price_per_tonne_usd", 25.0)))
        
        remaining_budget = budget_usd
        remaining_co2 = unmitigated_co2e_tonnes
        allocations = []
        total_offset_tonnes = 0.0
        total_spent = 0.0

        for cred in sorted_credits:
            if remaining_budget <= 0.01 or remaining_co2 <= 0.01:
                break
            
            project_id = cred.get("project_id", "offset_proj")
            price = max(1.0, float(cred.get("price_per_tonne_usd", 25.0)))
            available_tonnes = float(cred.get("available_tonnes", 1000.0))

            needed_tonnes = min(remaining_co2, available_tonnes)
            affordable_tonnes = min(needed_tonnes, remaining_budget / price)

            if affordable_tonnes > 0.001:
                cost = affordable_tonnes * price
                allocations.append({
                    "project_id": project_id,
                    "tonnes_offset": round(affordable_tonnes, 3),
                    "price_per_tonne_usd": price,
                    "total_cost_usd": round(cost, 2)
                })
                total_offset_tonnes += affordable_tonnes
                total_spent += cost
                remaining_budget -= cost
                remaining_co2 -= affordable_tonnes

        net_emissions = max(0.0, round(unmitigated_co2e_tonnes - total_offset_tonnes, 3))
        neutral_achieved = net_emissions <= 0.001

        return {
            "initial_unmitigated_tonnes": unmitigated_co2e_tonnes,
            "total_offset_tonnes": round(total_offset_tonnes, 3),
            "net_remaining_emissions_tonnes": net_emissions,
            "total_spent_usd": round(total_spent, 2),
            "budget_remaining_usd": round(remaining_budget, 2),
            "carbon_neutrality_achieved": neutral_achieved,
            "allocations": allocations
        }
