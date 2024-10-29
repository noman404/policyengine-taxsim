import unittest
import os
import subprocess
import pandas as pd
import numpy as np
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

        self.input_file = self.taxsim_dir / "taxsim_input.csv"

    def test_generate_policyengine_taxsim(self):
        output_file = self.output_dir / "policyengine_taxsim_output.csv"

        cmd = f"{sys.executable} {self.project_root}/policyengine_taxsim/cli.py {self.input_file} -o {output_file}"
        process = subprocess.run(
            cmd, shell=True, capture_output=True, text=True
        )

        print(f"PolicyEngine TAXSIM CLI output:\n{process.stdout}")
        if process.returncode != 0:
            print(
                f"PolicyEngine TAXSIM CLI failed with error:\n{process.stderr}"
            )
            raise Exception(
                f"PolicyEngine TAXSIM CLI failed: {process.returncode}"
            )

        self.assertTrue(output_file.is_file())
        print(f"Content of {output_file}:")
        with open(output_file, "r") as f:
            print(f.read())

    def test_generate_taxsim_output(self):
        output_file = self.output_dir / "taxsim35_output.csv"

        taxsim_path = self.taxsim_dir / self.taxsim_exe

        if platform.system().lower() != "windows":
            # Make the file executable on Unix-like systems
            os.chmod(taxsim_path, 0o755)

        cmd = f"{taxsim_path} < {self.input_file} > {output_file}"
        process = subprocess.run(
            cmd, shell=True, capture_output=True, text=True
        )

        print(f"TAXSIM35 output:\n{process.stdout}")
        if process.returncode != 0:
            print(f"TAXSIM35 failed with error:\n{process.stderr}")
            raise Exception(f"TAXSIM35 failed: {process.returncode}")

        self.assertTrue(output_file.is_file())
        print(f"Content of {output_file}:")
        with open(output_file, "r") as f:
            print(f.read())

    def test_match_both_output(self):
        taxsim35_csv = pd.read_csv(self.output_dir / "taxsim35_output.csv")
        pe_taxsim_csv = pd.read_csv(
            self.output_dir / "policyengine_taxsim_output.csv"
        )
        input_csv = pd.read_csv(self.input_file)

        print("Input CSV:")
        print(input_csv)
        print("\nTAXSIM35 output:")
        print(taxsim35_csv)
        print("\nPolicyEngine TAXSIM output:")
        print(pe_taxsim_csv)

        # Ensure both DataFrames have the same columns
        common_columns = set(taxsim35_csv.columns) & set(pe_taxsim_csv.columns)
        taxsim35_csv = taxsim35_csv[list(common_columns)]
        pe_taxsim_csv = pe_taxsim_csv[list(common_columns)]

        # Ensure both DataFrames have the same column names
        taxsim35_csv.columns = taxsim35_csv.columns.str.lower()
        pe_taxsim_csv.columns = pe_taxsim_csv.columns.str.lower()

        # Sort both DataFrames by taxsimid to ensure rows are in the same order
        taxsim35_csv = taxsim35_csv.sort_values("taxsimid").reset_index(
            drop=True
        )
        pe_taxsim_csv = pe_taxsim_csv.sort_values("taxsimid").reset_index(
            drop=True
        )
        input_csv = input_csv.sort_values("taxsimid").reset_index(
            drop=True
        )

        # Convert numeric columns to float
        numeric_columns = taxsim35_csv.select_dtypes(
            include=["number"]
        ).columns
        for col in numeric_columns:
            taxsim35_csv[col] = pd.to_numeric(
                taxsim35_csv[col], errors="coerce"
            )
            pe_taxsim_csv[col] = pd.to_numeric(
                pe_taxsim_csv[col], errors="coerce"
            )

        # Compare
        standard_output_cols = ["year", "fiitax", "siitax"]
        full_output_cols = standard_output_cols + [
            "tfica"
            "v10",  # state_agi
            "v13",
            "v18",
            "v19",
            "v26",
            "v28",
            "v34",
            "v45",
        ]

        # Determine which columns to check based on idtl value
        columns_to_check = full_output_cols if (input_csv["idtl"] == 2).any() else standard_output_cols

        # Compare all relevant columns at once
        comparison_results = {}
        for col in columns_to_check:
            if col in common_columns:
                matches = (taxsim35_csv[col] == pe_taxsim_csv[col]).all()
                comparison_results[col] = matches
                if not matches:
                    print(f"Mismatch in column {col}:")
                    print(f"TAXSIM35 values: {taxsim35_csv[col].values}")
                    print(f"PolicyEngine values: {pe_taxsim_csv[col].values}")

        # Assert all columns match
        all_matched = all(comparison_results.values())
        self.assertTrue(all_matched, f"Columns with missmatches: {[col for col, matched in comparison_results.items() if not matched]}")

if __name__ == "__main__":
    unittest.main()
