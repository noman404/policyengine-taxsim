from policyengine_taxsim.core.utils import (
    load_variable_mappings,
    get_state_number, to_roundedup_number,
)
from policyengine_us import Simulation


def export_single_household(taxsim_input, policyengine_situation):
    """
    Convert a PolicyEngine situation to TAXSIM output variables.

    Args:
        policyengine_situation (dict): PolicyEngine situation dictionary

    Returns:
        dict: Dictionary of TAXSIM output variables
    """
    mappings = load_variable_mappings()["policyengine_to_taxsim"]

    simulation = Simulation(situation=policyengine_situation)

    year = list(
        policyengine_situation["households"]["your household"][
            "state_name"
        ].keys()
    )[0]
    state_name = policyengine_situation["households"]["your household"][
        "state_name"
    ][year]

    taxsim_output = {
        "taxsimid": policyengine_situation.get("taxsimid", taxsim_input['taxsimid']),
        "year": int(year),
        "state": get_state_number(state_name),
        "mstat": policyengine_situation["tax_units"]["your tax unit"]
        .get("marital_status", {})
        .get(year, 1),
        "page": policyengine_situation["people"]["you"]["age"][year],
        "sage": policyengine_situation["people"]
        .get("your spouse", {})
        .get("age", {})
        .get(year, 0),
        "fiitax": to_roundedup_number(simulation.calculate("income_tax", period=year)),
        "siitax": to_roundedup_number(simulation.calculate("state_income_tax", period=year)),
        "fica": to_roundedup_number(simulation.calculate(
            "employee_social_security_tax", period=year
        )
        + simulation.calculate("employee_medicare_tax", period=year)),
    }

    # Add more variables as needed to match TAXSIM output

    return taxsim_output
