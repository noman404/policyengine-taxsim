import pytest

from policyengine_taxsim import generate_household, export_household


@pytest.fixture
def sample_taxsim_input():
    return {
        "year": 2021,
        "state": 3,
        "page": 35,
        "pwages": 50000,
        "taxsimid": 11,
        "idtl": 0
    }


@pytest.fixture
def sample_taxsim_input_without_state():
    return {
        "year": 2021,
        "page": 35,
        "pwages": 50000,
        "taxsimid": 11,
        "idtl": 0
    }


@pytest.fixture
def sample_taxsim_input_with_state_eq_0():
    return {
        "year": 2021,
        "page": 35,
        "state": 0,
        "pwages": 50000,
        "taxsimid": 11,
        "idtl": 0
    }


def test_import_single_household(sample_taxsim_input):
    expected_output = {
        "families": {
            "your family": {
                "members": [
                    "you"
                ]
            }
        },
        "households": {
            "your household": {
                "members": [
                    "you"
                ],
                "state_name": {
                    "2021": "AZ"
                }
            }
        },
        "marital_units": {
            "your marital unit": {
                "members": [
                    "you"
                ]
            }
        },
        "people": {
            "you": {
                "age": {
                    "2021": 35
                },
                "employment_income": {
                    "2021": 50000
                }
            }
        },
        "spm_units": {
            "your household": {
                "members": [
                    "you"
                ]
            }
        },
        "tax_units": {
            "your tax unit": {
                "members": [
                    "you"
                ]
            }
        }
    }

    result = generate_household(sample_taxsim_input)
    assert result == expected_output


def test_import_single_household_without_state(sample_taxsim_input_without_state):
    expected_output = {
        "families": {
            "your family": {
                "members": [
                    "you"
                ]
            }
        },
        "households": {
            "your household": {
                "members": [
                    "you"
                ],
                "state_name": {
                    "2021": "TX"
                }
            }
        },
        "marital_units": {
            "your marital unit": {
                "members": [
                    "you"
                ]
            }
        },
        "people": {
            "you": {
                "age": {
                    "2021": 35
                },
                "employment_income": {
                    "2021": 50000
                }
            }
        },
        "spm_units": {
            "your household": {
                "members": [
                    "you"
                ]
            }
        },
        "tax_units": {
            "your tax unit": {
                "members": [
                    "you"
                ]
            }
        }
    }

    result = generate_household(sample_taxsim_input_without_state)
    assert result == expected_output


def test_import_single_household_with_state_eq_0(sample_taxsim_input_with_state_eq_0):
    expected_output = {
        "families": {
            "your family": {
                "members": [
                    "you"
                ]
            }
        },
        "households": {
            "your household": {
                "members": [
                    "you"
                ],
                "state_name": {
                    "2021": "TX"
                }
            }
        },
        "marital_units": {
            "your marital unit": {
                "members": [
                    "you"
                ]
            }
        },
        "people": {
            "you": {
                "age": {
                    "2021": 35
                },
                "employment_income": {
                    "2021": 50000
                }
            }
        },
        "spm_units": {
            "your household": {
                "members": [
                    "you"
                ]
            }
        },
        "tax_units": {
            "your tax unit": {
                "members": [
                    "you"
                ]
            }
        }
    }

    result = generate_household(sample_taxsim_input_with_state_eq_0)
    assert result == expected_output


def test_export_single_household(sample_taxsim_input):
    policyengine_single_household_situation = {
        "families": {
            "your family": {
                "members": [
                    "you"
                ]
            }
        },
        "households": {
            "your household": {
                "members": [
                    "you"
                ],
                "state_name": {
                    "2021": "AZ"
                }
            }
        },
        "marital_units": {
            "your marital unit": {
                "members": [
                    "you"
                ]
            }
        },
        "people": {
            "you": {
                "age": {
                    "2021": 35
                },
                "employment_income": {
                    "2021": 50000
                }
            }
        },
        "spm_units": {
            "your household": {
                "members": [
                    "you"
                ]
            }
        },
        "tax_units": {
            "your tax unit": {
                "members": [
                    "you"
                ]
            }
        }
    }

    result = export_household(sample_taxsim_input, policyengine_single_household_situation)
    print(result)
    assert result["year"] == 2021
    assert result["state"] == 3
    assert "fiitax" in result
    assert "siitax" in result
    # Note: We can't easily predict the exact tax values without mocking the PolicyEngine simulation,
    # so we're just checking that these keys exist in the output.


def test_roundtrip(sample_taxsim_input):
    # Import TAXSIM input to PolicyEngine situation
    pe_situation = generate_household(sample_taxsim_input)

    # Export PolicyEngine situation back to TAXSIM output
    taxsim_output = export_household(sample_taxsim_input, pe_situation)

    # Check that key information is preserved
    assert taxsim_output["year"] == sample_taxsim_input["year"]
    assert taxsim_output["state"] == sample_taxsim_input["state"]
    # Again, we can't easily check the exact tax values, but we can ensure they exist
    assert "fiitax" in taxsim_output
    assert "siitax" in taxsim_output
