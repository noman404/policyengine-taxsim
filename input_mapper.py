from policyengine_us import Simulation
from policyengine_us import parameters
from policyengine_us.model_api import *

import pandas as pd

import argparse

import os

from TaxsimInputReader import InputReader

import importlib.metadata

# Example simulation imported from policyengine.org
# Single 40 years old parent with $100,000 income, 2 kids (10 years old), living in CA
situation1 = {
    "people": {
        "you": {
            "age": {
                "2024": 40
            },
            "employment_income": {
                "2024": 100000
            }
        },
        "your first dependent": {
            "age": {
                "2024": 10
            },
            "employment_income": {
                "2024": 0
            }
        },
        "your second dependent": {
            "age": {
                "2024": 10
            },
            "employment_income": {
                "2024": 0
            }
        }
    },
    "families": {
        "your family": {
            "members": [
                "you",
                "your first dependent",
                "your second dependent"
            ]
        }
    },
    "marital_units": {
        "your marital unit": {
            "members": [
                "you"
            ]
        },
        "your first dependent's marital unit": {
            "members": [
                "your first dependent"
            ],
            "marital_unit_id": {
                "2024": 1
            }
        },
        "your second dependent's marital unit": {
            "members": [
                "your second dependent"
            ],
            "marital_unit_id": {
                "2024": 2
            }
        }
    },
    "tax_units": {
        "your tax unit": {
            "members": [
                "you",
                "your first dependent",
                "your second dependent"
            ]
        }
    },
    "spm_units": {
        "your household": {
            "members": [
                "you",
                "your first dependent",
                "your second dependent"
            ]
        }
    },
    "households": {
        "your household": {
            "members": [
                "you",
                "your first dependent",
                "your second dependent"
            ],
            "state_name": {
                "2024": "CA"
            }
        }
    }
}

situation2 = {
    "people": {
        "you": {
            "age": {
                "2024": 40
            },
            "employment_income": {
                "2024": 100000
            }
        },
        "your partner": {
            "age": {
                "2024": 40
            },
            "employment_income": {
                "2024": 50000
            }
        }
    },
    "families": {
        "your family": {
            "members": [
                "you",
                "your partner"
            ]
        }
    },
    "marital_units": {
        "your marital unit": {
            "members": [
                "you",
                "your partner"
            ]
        }
    },
    "tax_units": {
        "your tax unit": {
            "members": [
                "you",
                "your partner"
            ]
        }
    },
    "spm_units": {
        "your household": {
            "members": [
                "you",
                "your partner"
            ]
        }
    },
    "households": {
        "your household": {
            "members": [
                "you",
                "your partner"
            ],
            "state_name": {
                "2024": "AL"
            }
        }
    }
}


def read_input_file(input_file):
    reader = InputReader(input_file)
    return reader.situations


# input a list of situations and convert each situation into a simulation object
def make_simulation(list_of_households):
    list_of_simulations = []
    for situation in list_of_households:
        list_of_simulations.append(Simulation(situation=situation, ))
    return list_of_simulations


# Return true if the string is a date
def is_date(string):
    try:
        pd.to_datetime(string, format='%Y')
        return True
    except Exception:
        return False


# Return true if the string can create a StateCode instance
def is_state_code(string):
    try:
        StateCode[string]
        return True
    except Exception:
        return False


# Get the user's state
def get_state(situation):
    year_and_state = list(situation["households"]["your household"]["state_name"].items())
    for item in year_and_state:
        for string in item:
            if is_state_code(string):
                return string


# Get the tax filing year
def get_year(situation):
    year_and_state = list(situation["households"]["your household"]["state_name"].items())
    for item in year_and_state:
        for string in item:
            if is_date(string):
                return string


# Returns the itemized_deduction function for the user's state
def state_itemized_deductions(situation):
    state = get_state(situation).lower()
    return state + "_itemized_deductions"


# Returns the standard_deduction function for the user's state
def state_standard_deduction(situation):
    state = get_state(situation).lower()
    return state + "_standard_deduction"


# Returns the function that computes Child and Dependent Care Credit for the user's state
def state_child_care_credit(situation):
    state = get_state(situation).lower()
    return state + "_cdcc"


# Returns the function that computes the user's AGI based on filing state
def state_adjusted_gross_income(situation):
    state = get_state(situation).lower()
    return state + "_agi"


# Returns the function that computes the user's state taxable income
def state_taxable_income(situation):
    state = get_state(situation).lower()
    return state + "_taxable_income"


# Returns the function that computes state income tax
def state_income_tax(situation):
    state = get_state(situation).lower()
    return state + "_income_tax"


# Return the function that computes total state exemptions
def state_exemptions(situation):
    state = get_state(situation).lower()
    # try to calculate state_exemption, if error, return 0 --> NEED TO ADD Feature
    return state + "_exemptions"


def state_agi(situation):
    state = get_state(situation).lower()
    return state + "_agi"


def placeholder():
    return "placeholder"


# List of variables that aren't mapped in Policy Engine
placeholder_variables = ["fica", "frate", "srate", "ficar", "tfica", "exemption_phaseout", "deduction_phaseout",
                         "income_tax19", "exemption_surtax", "general_tax_credit", "FICA", "state_rent_expense",
                         "state_property_tax_credit", "state_eic", "state_total_credits", "state_bracket_rate",
                         "state_exemptions", "state_cdcc"]

# list of variables that match Taxsim output variables
variables = ["get_year", "get_state", "income_tax", "state_income_tax", "fica", "frate", "srate", "ficar", "tfica",
             "adjusted_gross_income", "tax_unit_taxable_unemployment_compensation", "tax_unit_taxable_social_security",
             "basic_standard_deduction", "exemptions", "exemption_phaseout", "deduction_phaseout",
             "taxable_income_deductions",
             "taxable_income", "income_tax19", "exemption_surtax", "general_tax_credit", "ctc", "refundable_ctc",
             "cdcc",
             "eitc", "amt_income", "alternative_minimum_tax", "income_tax_before_refundable_credits", "FICA",
             "household_net_income",
             "state_rent_expense", "state_agi", "state_exemptions", "state_standard_deduction",
             "state_itemized_deductions",
             "state_taxable_income", "state_property_tax_credit", "state_child_care_credit", "state_eic",
             "state_total_credits",
             "state_bracket_rate", "self_employment_income", "net_investment_income_tax", "employee_medicare_tax",
             "rrc_cares"]

# list of dictiionaries where each Policy Engine variable is mapped to the Taxsim name.
# Booleans indicate whether the variable is a placeholder, a local variable, or a local variable that doesn't return a function (only get_year and state)
# list of variables mapped to taxsim "2" input (full variables)
full_variables = [
    {'variable': 'get_year', 'taxsim_name': 'year', 'is_placeholder': False, 'is_local': True, 'is_local_getter': True},
    {'variable': 'get_state', 'taxsim_name': 'state', 'is_placeholder': False, 'is_local': True,
     'is_local_getter': True},
    {'variable': 'income_tax', 'taxsim_name': 'fiitax', 'is_placeholder': False, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'state_income_tax', 'taxsim_name': 'siitax', 'is_placeholder': False, 'is_local': True,
     'is_local_getter': False},
    {'variable': 'fica', 'taxsim_name': 'fica', 'is_placeholder': True, 'is_local': False, 'is_local_getter': False},
    {'variable': 'frate', 'taxsim_name': 'frate', 'is_placeholder': True, 'is_local': False, 'is_local_getter': False},
    {'variable': 'srate', 'taxsim_name': 'srate', 'is_placeholder': True, 'is_local': False, 'is_local_getter': False},
    {'variable': 'ficar', 'taxsim_name': 'ficar', 'is_placeholder': True, 'is_local': False, 'is_local_getter': False},
    {'variable': 'tfica', 'taxsim_name': 'tfica', 'is_placeholder': True, 'is_local': False, 'is_local_getter': False},
    {'variable': 'adjusted_gross_income', 'taxsim_name': 'v10', 'is_placeholder': False, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'tax_unit_taxable_unemployment_compensation', 'taxsim_name': 'v11', 'is_placeholder': False,
     'is_local': False, 'is_local_getter': False},
    {'variable': 'tax_unit_taxable_social_security', 'taxsim_name': 'v12', 'is_placeholder': False, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'basic_standard_deduction', 'taxsim_name': 'v13', 'is_placeholder': False, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'exemptions', 'taxsim_name': 'v14', 'is_placeholder': False, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'exemption_phaseout', 'taxsim_name': 'v15', 'is_placeholder': True, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'deduction_phaseout', 'taxsim_name': 'v16', 'is_placeholder': True, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'taxable_income_deductions', 'taxsim_name': 'v17', 'is_placeholder': False, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'taxable_income', 'taxsim_name': 'v18', 'is_placeholder': False, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'income_tax19', 'taxsim_name': 'v19', 'is_placeholder': True, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'exemption_surtax', 'taxsim_name': 'v20', 'is_placeholder': True, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'general_tax_credit', 'taxsim_name': 'v21', 'is_placeholder': True, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'ctc', 'taxsim_name': 'v22', 'is_placeholder': False, 'is_local': False, 'is_local_getter': False},
    {'variable': 'refundable_ctc', 'taxsim_name': 'v23', 'is_placeholder': False, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'cdcc', 'taxsim_name': 'v24', 'is_placeholder': False, 'is_local': False, 'is_local_getter': False},
    {'variable': 'eitc', 'taxsim_name': 'v25', 'is_placeholder': False, 'is_local': False, 'is_local_getter': False},
    {'variable': 'amt_income', 'taxsim_name': 'v26', 'is_placeholder': False, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'alternative_minimum_tax', 'taxsim_name': 'v27', 'is_placeholder': False, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'income_tax_before_refundable_credits', 'taxsim_name': 'v28', 'is_placeholder': False,
     'is_local': False, 'is_local_getter': False},
    {'variable': 'FICA', 'taxsim_name': 'v29', 'is_placeholder': True, 'is_local': True, 'is_local_getter': False},
    {'variable': 'household_net_income', 'taxsim_name': 'v30', 'is_placeholder': False, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'state_rent_expense', 'taxsim_name': 'v31', 'is_placeholder': True, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'state_agi', 'taxsim_name': 'v32', 'is_placeholder': False, 'is_local': True,
     'is_local_getter': False},
    {'variable': 'state_exemptions', 'taxsim_name': 'v33', 'is_placeholder': True, 'is_local': True,
     'is_local_getter': False},
    {'variable': 'state_standard_deduction', 'taxsim_name': 'v34', 'is_placeholder': False, 'is_local': True,
     'is_local_getter': False},
    {'variable': 'state_itemized_deductions', 'taxsim_name': 'v35', 'is_placeholder': False, 'is_local': True,
     'is_local_getter': False},
    {'variable': 'state_taxable_income', 'taxsim_name': 'v36', 'is_placeholder': False, 'is_local': True,
     'is_local_getter': False},
    {'variable': 'state_property_tax_credit', 'taxsim_name': 'v37', 'is_placeholder': True, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'state_child_care_credit', 'taxsim_name': 'v38', 'is_placeholder': True, 'is_local': True,
     'is_local_getter': False},
    {'variable': 'state_eic', 'taxsim_name': 'v39', 'is_placeholder': True, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'state_total_credits', 'taxsim_name': 'v40', 'is_placeholder': True, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'state_bracket_rate', 'taxsim_name': 'v41', 'is_placeholder': True, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'self_employment_income', 'taxsim_name': 'v42', 'is_placeholder': False, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'net_investment_income_tax', 'taxsim_name': 'v43', 'is_placeholder': False, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'employee_medicare_tax', 'taxsim_name': 'v44', 'is_placeholder': False, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'rrc_cares', 'taxsim_name': 'v45', 'is_placeholder': False, 'is_local': False,
     'is_local_getter': False}
]

# variables mapped to taxsim "0" input (standard)
standard_variables = [
    {'variable': 'get_year', 'taxsim_name': 'year', 'is_placeholder': False, 'is_local': True, 'is_local_getter': True},
    {'variable': 'get_state', 'taxsim_name': 'state', 'is_placeholder': False, 'is_local': True,
     'is_local_getter': True},
    {'variable': 'income_tax', 'taxsim_name': 'fiitax', 'is_placeholder': False, 'is_local': False,
     'is_local_getter': False},
    {'variable': 'state_income_tax', 'taxsim_name': 'siitax', 'is_placeholder': False, 'is_local': True,
     'is_local_getter': False},
    {'variable': 'fica', 'taxsim_name': 'fica', 'is_placeholder': True, 'is_local': False, 'is_local_getter': False},
    {'variable': 'frate', 'taxsim_name': 'frate', 'is_placeholder': True, 'is_local': False, 'is_local_getter': False},
    {'variable': 'srate', 'taxsim_name': 'srate', 'is_placeholder': True, 'is_local': False, 'is_local_getter': False},
    {'variable': 'ficar', 'taxsim_name': 'ficar', 'is_placeholder': True, 'is_local': False, 'is_local_getter': False},
    {'variable': 'tfica', 'taxsim_name': 'tfica', 'is_placeholder': True, 'is_local': False, 'is_local_getter': False},
]


# Calculate the variables based on the user's information and save them to a dataframe

# input a list of simulations, a list of households, and a variable_dict. 
# variable dict will be switched to either 0, 2, 5 to correspond with taxsim inputs --> to be implemented

# separate iteration into one single household output
def single_household(household):
    row = []

    simulation = Simulation(situation=household, )

    variable_dict = full_variables

    for variable_info in variable_dict:
        variable = variable_info['variable']
        taxsim_name = variable_info['taxsim_name']
        is_placeholder = variable_info['is_placeholder']
        is_local = variable_info['is_local']
        is_local_getter = variable_info["is_local_getter"]

        # if the variable is a placeholder, append "placeholder"
        if is_placeholder:
            row.append(placeholder())
        else:
            # if the variable is local, return the value of the local function (returns a  to policyenginge function name)
            if is_local:
                function = globals()[variable]
                result = function(household)
                # if the variable is a local getter, just return the value of the local function
                if is_local_getter:
                    calculation = result
                # otherwise, run policy engine calculation using the function name
                else:
                    calculation = simulation.calculate(result)
            # if the variable is not local, just run policy engine calculation
            else:
                calculation = simulation.calculate(variable)

            row.append(calculation)

    return row


# second function that calls the single household for each in the list
def multiple_households(list_of_households):
    output = []

    list_of_simulations = make_simulation(list_of_households)

    for simulation, household in zip(list_of_simulations, list_of_households):
        row = single_household(household)
        output.append(row)

    # Create DataFrame from the output with taxsim_names as columns
    return output


def make_dataframe(input_file, variable_dict, is_multiple_households: bool):
    if not is_multiple_households:
        household = input_file[0]
        output = [single_household(household)]
        df = pd.DataFrame(output, columns=[var['taxsim_name'] for var in variable_dict],
                          index=pd.RangeIndex(start=1, stop=len(output) + 1, name='taxsimid'))
        return df
    else:
        output = multiple_households(input_file)
        df = pd.DataFrame(output, columns=[var['taxsim_name'] for var in variable_dict],
                          index=pd.RangeIndex(start=1, stop=len(output) + 1, name='taxsimid'))
        return df


# return true if the input file contains more than one household
def is_multiple_households(list):
    return len(list) > 1


# run main with an input file to execute the methods in the correct order
def main(input_file):
    print("running script")

    list_of_households = read_input_file(input_file)
    print(list_of_households)
    variable_dict = full_variables  # going to use a condition to set the correct variable list depending on the input

    output = make_dataframe(list_of_households, variable_dict, is_multiple_households(list_of_households))

    output.to_csv('output.csv', index=True)
    print("script finished")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process input file and generate output.')
    parser.add_argument('input_file', type=str, help='Path to the input CSV file')
    args = parser.parse_args()

    main(args.input_file)
