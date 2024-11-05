from .utils import (
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

    taxsim_output = {}
    taxsim_output["taxsimid"] = policyengine_situation.get("taxsimid", taxsim_input['taxsimid'])
    output_type = taxsim_input["idtl"]

    for key, value in mappings.items():
        if value['implemented']:
            if key == "year":
                taxsim_output[key] = int(year)
            elif key == "state":
                taxsim_output[key] = get_state_number(state_name)
            else:
                pe_variable = value['variable']

                if "state" in pe_variable:
                    pe_variable = pe_variable.replace("state", state_name).lower()

                for entry in value['idtl']:
                    if output_type in entry.values():
                        taxsim_output[key] = simulate(simulation, pe_variable, year)

    return taxsim_output


def simulate(simulation, variable, year):
    try:
        return to_roundedup_number(simulation.calculate(variable, period=year))
    except:
        return 0.00
