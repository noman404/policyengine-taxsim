from .utils import (
    load_variable_mappings,
    get_state_number, to_roundedup_number,
)
from policyengine_us import Simulation


def generate_non_description_output(taxsim_output, mappings, year, state_name, simulation, output_type):
    for key, value in mappings.items():
        if value['implemented']:
            if key == "year":
                taxsim_output[key] = int(year)
            elif key == "state":
                taxsim_output[key] = get_state_number(state_name)
            elif key == "fica":
                pe_variables = value['variables']
                taxsim_output[key] = simulate_multiple(simulation, pe_variables, year)
            else:
                pe_variable = value['variable']

                if "state" in pe_variable:
                    pe_variable = pe_variable.replace("state", state_name).lower()

                for entry in value['idtl']:
                    if output_type in entry.values():
                        taxsim_output[key] = simulate(simulation, pe_variable, year)

    return taxsim_output


def generate_text_description_output(taxsim_output, mappings, year, state_name, simulation):
    groups = {}
    group_orders = {}

    for var_name, var_info in mappings.items():
        if (
                "full_text_group" in var_info
                and "text_description" in var_info
                and "implemented" in var_info
                and var_info["implemented"] is True
                and any(item.get("full_text", 0) == 5 for item in var_info["idtl"])
        ):
            group = var_info["full_text_group"]
            group_order = var_info["group_order"]

            if group not in groups:
                groups[group] = []
                group_orders[group] = group_order

            groups[group].append((var_info["text_description"], var_name, var_info))

    lines = [""]

    # Configuration for tab space
    LEFT_MARGIN = 4
    LABEL_INDENT = 4
    LABEL_WIDTH = 45
    VALUE_WIDTH = 12

    sorted_groups = sorted(groups.keys(), key=lambda x: group_orders[x])

    for group_name in sorted_groups:
        variables = groups[group_name]
        if variables:

            lines.append(f"{'' * LEFT_MARGIN}{group_name}:")

            for desc, var_name, each_variable in sorted(variables, key=lambda x: x[0]):

                variable = each_variable['variable']

                if "state" in variable:
                    variable = variable.replace("state", state_name).lower()

                if var_name == "year":
                    value = year
                elif var_name == "state":
                    value = f"{get_state_number(state_name)}{' ' * LEFT_MARGIN}{state_name}"
                elif var_name == "fica":
                    value = simulate_multiple(simulation, each_variable['variables'], year)
                else:
                    value = simulate(simulation, variable, year)

                if isinstance(value, (int, float)):
                    formatted_value = f"{value:>8.2f}"
                else:
                    formatted_value = str(value)

                desc_lines = desc.split('\n')
                for i, desc_line in enumerate(desc_lines):

                    indent = LEFT_MARGIN + LABEL_INDENT

                    if i == 0:
                        padded_desc = f"{' ' * indent}{desc_line}"
                        lines.append(f"{padded_desc:<{LABEL_WIDTH + indent}}{formatted_value:>{VALUE_WIDTH}}")
                    else:
                        padded_desc = f"{' ' * indent}{desc_line}"
                        lines.append(f"{padded_desc:<{LABEL_WIDTH + indent}}")

            lines.append("")

    return "\n".join(lines)


def generate_text_description_output2(taxsim_output, mappings, year, state_name, simulation):
    groups = {}
    group_orders = {}

    # Sort variables into groups
    for var_name, var_info in mappings.items():
        if (
                "full_text_group" in var_info
                and "text_description" in var_info
                and "implemented" in var_info
                and var_info["implemented"] is True
                and any(item.get("full_text", 0) == 5 for item in var_info["idtl"])
        ):
            group = var_info["full_text_group"]
            group_order = var_info["group_order"]

            if group not in groups:
                groups[group] = []
                group_orders[group] = group_order

            groups[group].append((var_info["text_description"], var_name, var_info))

    # Configuration for formatting
    LEFT_MARGIN = 4
    LABEL_INDENT = 4
    LABEL_WIDTH = 45
    VALUE_WIDTH = 15
    SECOND_VALUE_WIDTH = 12

    lines = [""]
    sorted_groups = sorted(groups.keys(), key=lambda x: group_orders[x])

    for group_name in sorted_groups:
        variables = groups[group_name]
        if variables:
            # Check if this group has any variables with group_column = 2
            has_second_column = any(var_info.get('group_column', 1) == 2 for _, _, var_info in variables)

            if has_second_column:
                # Calculate spacing similar to text_description lines
                indent = LEFT_MARGIN + LABEL_INDENT
                line = f"{' ' * (LEFT_MARGIN + 3)}{group_name}:"
                padding = ' ' * (LABEL_WIDTH - len(group_name))
                # Format Base and +$1 like the values below
                base_text = f"{'Base':>8}"
                plus_one_text = f"{'+$1':>8}"
                lines.append(f"{line}{padding}{base_text:>{VALUE_WIDTH}}{plus_one_text:>{SECOND_VALUE_WIDTH}}")
            else:
                # Add just the group name
                lines.append(f"{' ' * LEFT_MARGIN}{group_name}:")

            for desc, var_name, each_variable in sorted(variables, key=lambda x: x[0]):
                variable = each_variable['variable']
                needs_second_column = each_variable.get('group_column', 1) == 2

                if "state" in variable:
                    variable = variable.replace("state", state_name).lower()

                if var_name == "year":
                    value = year
                elif var_name == "state":
                    value = f"{get_state_number(state_name)}{' ' * LEFT_MARGIN}{state_name}"
                elif var_name == "fica":
                    value = simulate_multiple(simulation, each_variable['variables'], year)
                else:
                    value = simulate(simulation, variable, year)

                # Format the base value
                if isinstance(value, (int, float)):
                    formatted_value = f"{value:>8.1f}"
                else:
                    formatted_value = str(value)

                # Format second column value if needed
                if needs_second_column:
                    if isinstance(value, (int, float)):
                        second_value = value + 1
                        formatted_second_value = f"{second_value:>8.1f}"
                    else:
                        formatted_second_value = str(value)

                # Handle multi-line descriptions
                desc_lines = desc.split('\n')
                for desc_line_index, desc_line in enumerate(desc_lines):
                    indent = LEFT_MARGIN + LABEL_INDENT
                    if needs_second_column:
                        line = f"{' ' * indent}{desc_line:<{LABEL_WIDTH}}{formatted_value:>{VALUE_WIDTH}}"
                        if desc_line_index == 0:  # Only add second value on first line
                            line += f"{formatted_second_value:>{SECOND_VALUE_WIDTH}}"
                    else:
                        line = f"{' ' * indent}{desc_line:<{LABEL_WIDTH}}{formatted_value:>{VALUE_WIDTH}}"
                    lines.append(line)

            lines.append("")

    return "\n".join(lines)


def export_household(taxsim_input, policyengine_situation):
    """
    Convert a PolicyEngine situation to TAXSIM output variables.

    Args:
        policyengine_situation (dict): PolicyEngine situation dictionary

    Returns:
        dict: Dictionary of TAXSIM output variables
    """
    mappings = load_variable_mappings()["policyengine_to_taxsim"]
    print(policyengine_situation)
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

    if int(output_type) in [0, 2]:
        taxsim_output = generate_non_description_output(taxsim_output, mappings, year, state_name, simulation,
                                                        output_type)
    else:
        taxsim_output = generate_text_description_output2(taxsim_output, mappings, year, state_name, simulation)

        with open("taxsim_output.txt", "w") as f:
            f.write(taxsim_output)
    return taxsim_output


def simulate(simulation, variable, year):
    try:
        output = to_roundedup_number(simulation.calculate(variable, period=year))
        print(variable, output)
        return output
    except Exception as error:
        return 0.00


def simulate_multiple(simulation, variables, year):
    try:
        total = sum(to_roundedup_number(simulation.calculate(variable, period=year)) for variable in variables)
    except Exception as error:
        total = 0.00
    return to_roundedup_number(total)
