import unittest
import os
import subprocess
import pandas as pd
from pathlib import Path
import platform
import sys


class E2ETest(unittest.TestCase):

    def setUp(self) -> None:
        self.project_root = Path(__file__).parent.parent
        self.taxsim_dir = self.project_root / "resources" / "taxsim35"
        self.output_dir = self.project_root / "output"
        self.output_dir.mkdir(exist_ok=True)

        # Determine the correct TAXSIM executable based on the OS
        system = platform.system().lower()
        if system == "darwin":
            self.taxsim_exe = "taxsim35-osx.exe"
        elif system == "windows":
            self.taxsim_exe = "taxsim35-windows.exe"
        elif system == "linux":
            self.taxsim_exe = "taxsim35-unix.exe"
        else:
            raise OSError(f"Unsupported operating system: {system}")

    def test_generate_taxsim_output(self):
        input_file = self.taxsim_dir / "taxsim_input.csv"
        output_file = self.output_dir / "taxsim35_output.csv"

        taxsim_path = self.taxsim_dir / self.taxsim_exe

        if platform.system().lower() != "windows":
            # Make the file executable on Unix-like systems
            os.chmod(taxsim_path, 0o755)

        cmd = f"{taxsim_path} < {input_file} > {output_file}"
        process = subprocess.run(
            cmd, shell=True, check=True, text=True, capture_output=True
        )

        if process.returncode != 0:
            raise Exception(f"cmd {cmd} failed: {process.stderr}")

        self.assertTrue(output_file.is_file())

    def test_generate_policyengine_taxsim(self):
        input_file = self.taxsim_dir / "taxsim_input.csv"
        output_file = self.output_dir / "policyengine_taxsim_output.csv"

        cmd = f"{sys.executable} {self.project_root}/policyengine_taxsim/cli.py {input_file} -o {output_file}"
        process = subprocess.run(
            cmd, shell=True, check=True, text=True, capture_output=True
        )

        if process.returncode != 0:
            raise Exception(f"cmd {cmd} failed: {process.stderr}")

        self.assertTrue(output_file.is_file())

    def test_match_both_output(self):
        taxsim35_csv = pd.read_csv(self.output_dir / "taxsim35_output.csv")
        pe_taxsim_csv = pd.read_csv(
            self.output_dir / "policyengine_taxsim_output.csv"
        )

        # Ensure both DataFrames have the same column names
        taxsim35_csv.columns = taxsim35_csv.columns.str.lower()
        pe_taxsim_csv.columns = pe_taxsim_csv.columns.str.lower()

        # Compare numeric columns with a small tolerance
        numeric_columns = taxsim35_csv.select_dtypes(
            include=["number"]
        ).columns
        is_close = np.allclose(
            taxsim35_csv[numeric_columns],
            pe_taxsim_csv[numeric_columns],
            rtol=1e-5,
            atol=1e-8,
        )

        # Compare non-numeric columns exactly
        non_numeric_columns = taxsim35_csv.select_dtypes(
            exclude=["number"]
        ).columns
        is_exact = (
            (
                taxsim35_csv[non_numeric_columns]
                == pe_taxsim_csv[non_numeric_columns]
            )
            .all()
            .all()
        )

        is_matched = is_close and is_exact

        if not is_matched:
            differences = taxsim35_csv.compare(pe_taxsim_csv)
            for column in differences.columns.levels[0]:
                print(f"Differences in {column}:")
                print(differences[column])

        self.assertTrue(is_matched)


if __name__ == "__main__":
    unittest.main()
