"""
DataLoader module.

Responsible for loading CSV files into pandas DataFrames.
This module abstracts file input logic so that data loading
is separated from GUI and visualization code.
"""

import pandas as pd 

class DataLoader:  # Handles loading CSV files into DataFrames
    def __init__(self, path):
        self.path = path  # Store CSV file path

    def load(self):  # Load CSV and return a DataFrame
        try:
            df = pd.read_csv(self.path)  # Read CSV into pandas DataFrame
            return df
        except Exception as e:  # Catch file or syntax errors
            print("Error loading CSV:", e)
            return None  # Return None so the GUI can handle failure safely