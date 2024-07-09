import pandas as pd

class InputReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self.read_csv()
        self.situations = self.get_situations()
    
    def read_csv(self):
        df = pd.read_csv(self.file_path, index_col=False)  # Read CSV without using the first column as index

        return df
    
    def get_filing_status(self, mstat):
        if mstat == 1 or mstat.lower() == "single":
            return "single"
        elif mstat == 2 or mstat.lower() == "married, jointly":
            return "married_jointly"
        elif mstat == 6 or mstat.lower() == "married, separately":
            return "married_separately"
        elif mstat == 8 or mstat.lower() == "dependent child":
            return "dependent_child"
        elif mstat == 1 or mstat.lower() == "head of household":
            return "head_of_household"
        else:
            raise ValueError(f"Unknown filing status: {mstat}")
    
    def get_state_code(self, state_number):
        # Mapping of state numbers to SOI state codes
        state_mapping = {
            1: "AL", 2: "AK", 3: "AZ", 4: "AR", 5: "CA",
            6: "CO", 7: "CT", 8: "DE", 9: "DC", 10: "FL",
            11: "GA", 12: "HI", 13: "ID", 14: "IL", 15: "IN",
            16: "IA", 17: "KS", 18: "KY", 19: "LA", 20: "ME",
            21: "MD", 22: "MA", 23: "MI", 24: "MN", 25: "MS",
            26: "MO", 27: "MT", 28: "NE", 29: "NV", 30: "NH",
            31: "NJ", 32: "NM", 33: "NY", 34: "NC", 35: "ND",
            36: "OH", 37: "OK", 38: "OR", 39: "PA", 40: "RI",
            41: "SC", 42: "SD", 43: "TN", 44: "TX", 45: "UT",
            46: "VT", 47: "VA", 48: "WA", 49: "WV", 50: "WI",
            51: "WY"
        }

        # Return the state code if the number is valid, otherwise return an error message
        return state_mapping.get(state_number, "Invalid state number")

    def create_situation(self, row):
        year = str(row['year'])  
        mstat = row['mstat']
        state = self.get_state_code(row['state'])
        


        # Initialize the situation dictionary
        situation = {
            "people": {},
            "families": {},
            "marital_units": {},
            "tax_units": {},
            "spm_units": {},
            "households": {}
        }

        # Add the primary taxpayer
        main_person_id = "you"
        situation["people"][main_person_id] = {
            "age": {year: int(row.get('page', 0))},  # Convert to int
            "employment_income": {year: int(row.get('pwages', 0))}  # Convert to int
        }

        members = [main_person_id]

        # Add the spouse if present
        marital_unit_members = [main_person_id]
        if pd.notna(row.get('sage')) and pd.notna(row.get('swages')):
            spouse_id = "your partner"
            situation["people"][spouse_id] = {
                "age": {year: int(row['sage'])},  # Convert to int
                "employment_income": {year: int(row['swages'])}  # Convert to int
            }
            members.append(spouse_id)
            marital_unit_members.append(spouse_id)

        # Populate the families, marital_units, tax_units, spm_units, and households
        family_id = "your family"
        situation["families"][family_id] = {"members": members}

        marital_unit_id = "your marital unit"
        situation["marital_units"][marital_unit_id] = {"members": marital_unit_members}

        tax_unit_id = "your tax unit"
        situation["tax_units"][tax_unit_id] = {"members": members}

        spm_unit_id = "your household"
        situation["spm_units"][spm_unit_id] = {"members": members}

        household_id = "your household"
        situation["households"][household_id] = {
            "members": members,
            "state_name": {year: str(state)} 
        }

        return situation
    
    def get_situations(self):
        situations = []
        
        for index, row in self.df.iterrows():

            situation = self.create_situation(row)
            situations.append(situation)
       
        
        return situations
