from policyengine_taxsim.core.utils import (
    load_variable_mappings,
    get_state_number,
)
from policyengine_us import Simulation


def export_single_household(policyengine_situation):
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
        "year": int(year),
        "state": get_state_number(state_name),
        "fiitax": simulation.calculate("income_tax", period=year),
        "siitax": simulation.calculate("state_income_tax", period=year),
    }

    return taxsim_output
