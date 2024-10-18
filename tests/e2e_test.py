# import unittest
# import os
# import subprocess
# import pandas


# class E2ETest(unittest.TestCase):

#     def setUp(self) -> None:
#         self.taxsim_dir = "taxsim35/"

#     def test_generate_taxsim_output(self):

#         cmd = "taxsim35.exe < taxsim_input.csv"
#         process = subprocess.Popen(
#             cmd,
#             shell=True,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             cwd=self.taxsim_dir,
#         )

#         std_output, std_error = process.communicate()

#         output = std_output.decode("utf-8").strip()
#         error = process.returncode

#         print("error:", error, error is None)

#         if error != 0:
#             raise Exception(f"cmd {cmd} failed, see above for details")

#         with open(f"{self.taxsim_dir}output.csv", "w", newline="") as file:
#             file.write(output)
#         file.close()

#         self.assertTrue(os.path.isfile(f"{self.taxsim_dir}output.csv"))

#     def test_generate_policyengine_taxsim(self):

#         cmd = "python taxsim_emulator.py taxsim_input.csv"
#         result = []
#         process = subprocess.Popen(
#             cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
#         )

#         for line in process.stdout:
#             result.append(line)

#         error_code = process.returncode

#         for line in result:
#             print(line)

#         if error_code is not None:
#             raise Exception(f"cmd {cmd} failed, see above for details")

#         self.assertTrue(os.path.isfile("output.csv"))

#     def test_match_both_output(self):

#         taxsim35_csv = pandas.read_csv(f"{self.taxsim_dir}output.csv")
#         pe_taxsim_csv = pandas.read_csv("output.csv")
#         is_matched = taxsim35_csv.equals(pe_taxsim_csv)
#         if is_matched:
#             self.assertTrue(is_matched)
#         else:
#             differences = taxsim35_csv.compare(pe_taxsim_csv)
#             # print(differences)
#             for column in differences.columns.levels[0]:
#                 print(f"Differences in {column}:")
#                 print(differences[column])
