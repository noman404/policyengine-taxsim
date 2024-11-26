import click
import pandas as pd
from pathlib import Path
try:
    from .core.input_mapper import generate_household
    from .core.output_mapper import export_household
except ImportError:
    from policyengine_taxsim.core.input_mapper import generate_household
    from policyengine_taxsim.core.output_mapper import export_household

@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="output.csv",
    help="Output file path",
)
@click.option('--logs', is_flag=True, help='Generate Logs')
def main(input_file, output, logs):
    """
    Process TAXSIM input file and generate PolicyEngine-compatible output.
    """
    try:
        # Read input file
        df = pd.read_csv(input_file)

        # Process each row
        results = []
        for _, row in df.iterrows():
            taxsim_input = row.to_dict()
            pe_situation = generate_household(taxsim_input)
            taxsim_output = export_household(taxsim_input, pe_situation, logs)
            results.append(taxsim_output)

        # Create output dataframe and save to csv
        output_df = pd.DataFrame(results)
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_df.to_csv(output_path, index=False)
        click.echo(f"Output saved to {output}")
    except Exception as e:
        click.echo(f"Error processing input: {str(e)}", err=True)
        raise


if __name__ == "__main__":
    main()
