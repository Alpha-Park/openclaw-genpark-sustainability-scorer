# -*- coding: utf-8 -*-
from client import OpenClawGenParkSustainabilityScorer

eco = OpenClawGenParkSustainabilityScorer()

# 1. Carbon Footprint LCA
bom = [
    {"material": "aluminum", "weight_kg": 0.45},
    {"material": "plastic_recycled", "weight_kg": 0.20},
    {"material": "electronics_pcba", "weight_kg": 0.08}
]
lca = eco.calculate_cradle_to_gate_carbon_footprint(bom, transport_distance_km=1500.0, transport_mode="road_freight")
print(f"LCA Carbon Footprint: {lca['total_co2e_kg']} kg CO2e ({lca['sustainability_rating']})")
print(f"  Materials: {lca['material_co2e_kg']} kg, Transport: {lca['transport_co2e_kg']} kg")

# 2. Packaging Circularity
packaging = [
    {"weight_grams": 120.0, "recycled_content_pct": 100.0, "recyclable_pct": 100.0},
    {"weight_grams": 15.0, "recycled_content_pct": 30.0, "recyclable_pct": 50.0}
]
circ = eco.evaluate_packaging_circularity_ratio(packaging)
print()
print(f"Packaging Circularity: {circ['circularity_percentage']}% ({circ['classification']})")

# 3. ESG Offset Optimization
credits = [
    {"project_id": "biochar_carbon_removal", "price_per_tonne_usd": 45.0, "available_tonnes": 50.0},
    {"project_id": "gold_standard_reforestation", "price_per_tonne_usd": 18.0, "available_tonnes": 200.0}
]
alloc = eco.optimize_esg_carbon_credit_allocation(unmitigated_co2e_tonnes=100.0, available_credits=credits, budget_usd=2500.0)
print()
print(f"Offset Optimization: Offset {alloc['total_offset_tonnes']}t (Spent ${alloc['total_spent_usd']}, Neutrality={alloc['carbon_neutrality_achieved']})")
