from policyengine_us import Simulation
from policyengine_us import parameters
from policyengine_us.model_api import *

import pandas as pd

# Example simulation imported from policyengine.org
# Single 40 year old parent with $100,000 income, 2 kids (10 years old), living in CA
situation = {
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

simulation = Simulation(
    situation=situation,
)

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
                return(string)

# Get the tax filing year
def get_year(situation):
    year_and_state = list(situation["households"]["your household"]["state_name"].items())
    for item in year_and_state:
        for string in item:
            if is_date(string):
                return(string)

#print(get_year(situation))
#print(get_state(situation))

# Returns the itemized_deduction function for the user's state
def state_itemized_deductions(situation):
    state = get_state(situation).lower()
    return(state + "_itemized_deductions")

# Returns the standard_deduction function for the user's state
def state_standard_deduction(situation):
    state = get_state(situation).lower()
    return(state + "_standard_deduction")

# Returns the function that computes Child and Dependent Care Credit for the user's state
def state_child_care_credit(situation):
    state = get_state(situation).lower()
    return(state + "_cdcc")

# Returns the function that computes the user's AGI based on filing state
def state_adjusted_gross_income(situation):
    state = get_state(situation).lower()
    return(state + "_agi")

# Returns the function that computes the user's state taxable income
def state_taxable_income(situation):
    state = get_state(situation).lower()
    return(state + "_taxable_income")

# Returns the function that computes state income tax
def state_income_tax(situation):
    state = get_state(situation).lower()
    return(state + "_income_tax")

# Return the function that computes total state exemptions
def state_exemptions(situation):
    state = get_state(situation).lower()
    #try to calculate state_exemption, if error, return 0 --> NEED TO ADD Feature
    return(state + "_exemptions")


# list of variables that match Taxsim output variables
variables =  ["household_net_income", "employee_payroll_tax", "taxsim_tfica", "employee_medicare_tax", "eitc"]

# Calculate the variables based on the user's information and save them to a dataframe
output = simulation.calculate_dataframe(variables, 2024)
output = pd.DataFrame(output)

#output.to_csv()
#print(output.head())