from policyengine_us import Simulation
from policyengine_us import parameters
from policyengine_us.model_api import *

import pandas as pd

import argparse

import os

from TaxsimInputReader import InputReader

import importlib.metadata


def read_input_file(input_file):
    reader = InputReader(input_file)
    return (reader)


def get_situations(reader):
    return (reader.situations)


def get_output_level(reader):
    return (reader.output_level)


def get_variables(output_level):
    if output_level == "standard":
        return standard_variables
    elif output_level == "full":
        return full_variables
    elif output_level == "text_descriptions":
        raise ValueError(
            "Emulator does not support the text description option yet. Please use standard or full output levels")


# input a list of situations and convert each situation into a simulation object
def make_simulation(list_of_households):
    list_of_simulations = []
    for situation in list_of_households:
        list_of_simulations.append(Simulation(situation=situation, ))
    return list_of_simulations


def convert_to_number(arr):
    # Access the element (assuming it's a single-element array)
    value = arr[0]
    # Round to two decimal places
    rounded_value = round(value, 2)
    # Format as string with two decimal places and trailing zeros
    return f"{rounded_value:.2f}"


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


# Get the state SOI code for the state output column
def get_state_code(situation):
    state = get_state(situation)
    state_code_mapping = {
        "AL": 1, "AK": 2, "AZ": 3, "AR": 4, "CA": 5, "CO": 6, "CT": 7, "DE": 8, "DC": 9, "FL": 10,
        "GA": 11, "HI": 12, "ID": 13, "IL": 14, "IN": 15, "IA": 16, "KS": 17, "KY": 18, "LA": 19,
        "ME": 20, "MD": 21, "MA": 22, "MI": 23, "MN": 24, "MS": 25, "MO": 26, "MT": 27, "NE": 28,
        "NV": 29, "NH": 30, "NJ": 31, "NM": 32, "NY": 33, "NC": 34, "ND": 35, "OH": 36, "OK": 37,
        "OR": 38, "PA": 39, "RI": 40, "SC": 41, "SD": 42, "TN": 43, "TX": 44, "UT": 45, "VT": 46,
        "VA": 47, "WA": 48, "WV": 49, "WI": 50, "WY": 51
    }
    return (state_code_mapping.get(state))


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


def placeholder(situation):
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
    {'taxsim_name': 'year', 'calculation': 'get_year'},
    {'taxsim_name': 'state', 'calculation': 'get_state_code'},
    {'taxsim_name': 'fiitax', 'calculation': 'income_tax'},
    {'taxsim_name': 'siitax', 'calculation': lambda household: globals()['state_income_tax'](household)},
    {'taxsim_name': 'fica', 'calculation': 'placeholder'},
    {'taxsim_name': 'frate', 'calculation': 'placeholder'},
    {'taxsim_name': 'srate', 'calculation': 'placeholder'},
    {'taxsim_name': 'ficar', 'calculation': 'placeholder'},
    {'taxsim_name': 'tfica', 'calculation': 'placeholder'},
    {'taxsim_name': 'v10', 'calculation': 'adjusted_gross_income'},
    {'taxsim_name': 'v11', 'calculation': 'tax_unit_taxable_unemployment_compensation'},
    {'taxsim_name': 'v12', 'calculation': 'tax_unit_taxable_social_security'},
    {'taxsim_name': 'v13', 'calculation': 'basic_standard_deduction'},
    {'taxsim_name': 'v14', 'calculation': 'exemptions'},
    {'taxsim_name': 'v15', 'calculation': 'placeholder'},
    {'taxsim_name': 'v16', 'calculation': 'placeholder'},
    {'taxsim_name': 'v17', 'calculation': 'taxable_income_deductions'},
    {'taxsim_name': 'v18', 'calculation': 'taxable_income'},
    {'taxsim_name': 'v19', 'calculation': 'placeholder'},
    {'taxsim_name': 'v20', 'calculation': 'placeholder'},
    {'taxsim_name': 'v21', 'calculation': 'placeholder'},
    {'taxsim_name': 'v22', 'calculation': 'ctc'},
    {'taxsim_name': 'v23', 'calculation': 'refundable_ctc'},
    {'taxsim_name': 'v24', 'calculation': 'cdcc'},
    {'taxsim_name': 'v25', 'calculation': 'eitc'},
    {'taxsim_name': 'v26', 'calculation': 'amt_income'},
    {'taxsim_name': 'v27', 'calculation': 'alternative_minimum_tax'},
    {'taxsim_name': 'v28', 'calculation': 'income_tax_before_refundable_credits'},
    {'taxsim_name': 'v29', 'calculation': 'placeholder'},
    {'taxsim_name': 'v30', 'calculation': 'household_net_income'},
    {'taxsim_name': 'v31', 'calculation': 'placeholder'},
    {'taxsim_name': 'v32', 'calculation': lambda household: globals()['state_agi'](household)},
    {'taxsim_name': 'v33', 'calculation': 'placeholder'},
    {'taxsim_name': 'v34', 'calculation': lambda household: globals()['state_standard_deduction'](household)},
    {'taxsim_name': 'v35', 'calculation': lambda household: globals()['state_itemized_deductions'](household)},
    {'taxsim_name': 'v36', 'calculation': lambda household: globals()['state_taxable_income'](household)},
    {'taxsim_name': 'v37', 'calculation': 'placeholder'},
    {'taxsim_name': 'v38', 'calculation': 'placeholder'},
    {'taxsim_name': 'v39', 'calculation': 'placeholder'},
    {'taxsim_name': 'v40', 'calculation': 'placeholder'},
    {'taxsim_name': 'v41', 'calculation': 'placeholder'},
    {'taxsim_name': 'v42', 'calculation': 'self_employment_income'},
    {'taxsim_name': 'v43', 'calculation': 'net_investment_income_tax'},
    {'taxsim_name': 'v44', 'calculation': 'employee_medicare_tax'},
    {'taxsim_name': 'v45', 'calculation': 'rrc_cares'}
]

# variables mapped to taxsim "0" input (standard)
standard_variables = [
    {'taxsim_name': 'year', 'calculation': 'get_year'},
    {'taxsim_name': 'state', 'calculation': 'get_state'},
    {'taxsim_name': 'fiitax', 'calculation': 'income_tax'},
    {'taxsim_name': 'siitax', 'calculation': lambda household: globals()['state_income_tax'](household)},
    {'taxsim_name': 'fica', 'calculation': 'placeholder'},
    {'taxsim_name': 'frate', 'calculation': 'placeholder'},
    {'taxsim_name': 'srate', 'calculation': 'placeholder'},
    {'taxsim_name': 'ficar', 'calculation': 'placeholder'},
    {'taxsim_name': 'tfica', 'calculation': 'placeholder'}
]


# Calculate the variables based on the user's information and save them to a dataframe

# input a list of simulations, a list of households, and a variable_dict. 
# variable dict will be switched to either 0, 2, 5 to correspond with taxsim inputs --> to be implemented


# separate iteration into one single household output
def single_household(household, variable_dict):
    row = []

    simulation = Simulation(situation=household, )

    for variable_info in variable_dict:
        calculation = variable_info['calculation']
        # check that the string isn't a local function. If it is, assign the result of the local function to result
        if calculation in ['get_year', 'get_state_code', 'placeholder']:
            function = globals()[calculation]
            result = function(household)
        # if calculation is a string, it is a policy engine function, so use the simulation to calculate
        elif isinstance(calculation, str):
            result = simulation.calculate(calculation)
            result = convert_to_number(result)
        # if calculation is not a string, it is a local function that returns the name of a policy engine function
        # take the result of calculation, input it to the simulation.calculate, and assign the result to result
        else:
            func = calculation(household)
            result = simulation.calculate(func)
            result = convert_to_number(result)

        row.append(result)

    return row


# second function that calls the single household for each in the list
def multiple_households(list_of_households, variable_dict):
    output = []

    list_of_simulations = make_simulation(list_of_households)

    for simulation, household in zip(list_of_simulations, list_of_households):
        row = single_household(household, variable_dict)
        output.append(row)

    # Create DataFrame from the output with taxsim_names as columns
    return output


def make_dataframe(input_file, variable_dict, is_multiple_households: bool):
    if not is_multiple_households:
        household = input_file[0]
        output = [single_household(household, variable_dict)]
        df = pd.DataFrame(output, columns=[var['taxsim_name'] for var in variable_dict],
                          index=pd.RangeIndex(start=1, stop=len(output) + 1, name='taxsimid'))
        return df
    else:
        output = multiple_households(input_file, variable_dict)
        df = pd.DataFrame(output, columns=[var['taxsim_name'] for var in variable_dict],
                          index=pd.RangeIndex(start=1, stop=len(output) + 1, name='taxsimid'))
        return df


# return true if the input file contains more than one household
def is_multiple_households(list):
    return len(list) > 1


# run main with an input file to execute the methods in the correct order
def main(input_file):
    print("running script")

    reader = read_input_file(input_file)
    list_of_households = get_situations(reader)
    output_level = get_output_level(reader)
    variable_dict = get_variables(output_level)

    print("Chosen Output Level: " + output_level)

    output = make_dataframe(list_of_households, variable_dict, is_multiple_households(list_of_households))

    output.to_csv('output.csv', index=True)

    print("script finished")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process input file and generate output.')
    parser.add_argument('input_file', type=str, help='Path to the input CSV file')
    args = parser.parse_args()

    main(args.input_file)
