import click
import pandas as pd
from policyengine_taxsim.core.input_mapper import import_single_household
from policyengine_taxsim.core.output_mapper import export_single_household
import argparse
import taxsim_emulator as pe_taxsim_emulator


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="output.csv",
    help="Output file path",
)
def main(input_file, output):
    """
    Process TAXSIM input file and generate PolicyEngine-compatible output.
    """
    # Read input file
    df = pd.read_csv(input_file)

    # Process each row
    results = []
    for _, row in df.iterrows():
        taxsim_input = row.to_dict()
        pe_situation = import_single_household(taxsim_input)
        taxsim_output = export_single_household(pe_situation)
        results.append(taxsim_output)

    # Create output dataframe and save to csv
    output_df = pd.DataFrame(results)
    output_df.to_csv(output, index=False)
    click.echo(f"Output saved to {output}")


if __name__ == "__main__":
    main()
    # parser = argparse.ArgumentParser(description='Process input file and generate output.')
    # parser.add_argument('input_file', type=str, help='Path to the input CSV file')
    # args = parser.parse_args()

    # pe_taxsim_emulator.main(args.input_file)
