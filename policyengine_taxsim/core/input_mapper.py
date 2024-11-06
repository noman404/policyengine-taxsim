from .utils import (
    load_variable_mappings,
    get_state_code,
)
import copy


def form_household_situation(depx, year, state, taxsim_vars):
    mappings = load_variable_mappings()["taxsim_to_policyengine"]

    base_situation = copy.deepcopy(mappings["household_situation"])

    if depx == 1:
        household_type = "single_household"
    elif depx == 2:
        household_type = "joint_household"
    else:
        household_type = "single_household"

    household_members = mappings["household_type"][household_type]

    base_situation["families"]["your family"]["members"] = household_members
    base_situation["households"]["your household"]["members"] = household_members
    base_situation["tax_units"]["your tax unit"]["members"] = household_members
    base_situation["spm_units"]["your household"]["members"] = household_members

    base_situation["marital_units"]["your marital unit"]["members"] = (
        ["you", "your partner"] if household_type == "joint_household" else ["you"]
    )

    base_situation["households"]["your household"]["state_name"][str(year)] = state

    people = base_situation["people"]

    people["you"] = {
        "age": {str(year): int(taxsim_vars.get("page", 40))},
        "employment_income": {str(year): int(taxsim_vars.get("pwages", 0))}
    }

    if household_type == "joint_household":
        people["your partner"] = {
            "age": {str(year): int(taxsim_vars.get("sage", 40))},
            "employment_income": {str(year): int(taxsim_vars.get("swages", 0))}
        }

    return base_situation


def generate_household(taxsim_vars):
    """
    Convert TAXSIM input variables to a PolicyEngine situation.

    Args:
        taxsim_vars (dict): Dictionary of TAXSIM input variables

    Returns:
        dict: PolicyEngine situation dictionary
    """

    year = str(int(taxsim_vars["year"]))  # Ensure year is an integer string

    taxsim_vars["state"] = taxsim_vars.get("state",
                                           44) or 44  # set TX texas as default is no state has passed or passed as 0
    state = get_state_code(taxsim_vars["state"])

    taxsim_vars["depx"] = taxsim_vars.get("depx", 1) or 1

    situation = form_household_situation(taxsim_vars["depx"], year, state, taxsim_vars)

    return situation
