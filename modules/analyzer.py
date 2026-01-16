"""
Analyzer module.

Originally designed for the CLI-based version of the project.
In the CLI architecture, this module handled data analysis logic such as
computing summaries and aggregations from a pandas DataFrame, while the CLI
layer handled user interaction and output.

In the current GUI-based version, most analysis is performed dynamically
through interactive filtering and visualization, so this module is not
directly used. It is kept to demonstrate modular design and future
extensibility.
"""

class Analyzer:
    def __init__(self, df):
        self.df = df

    def basic_summary(self):
        return {
            "rows": len(self.df),
            "columns": len(self.df.columns),
            "missing_values": self.df.isnull().sum().to_dict()
        }

    # Assumes a dataset with a 'location' column (e.g. country-based data)
    def top_countries(self, column, n=5):
        if column not in self.df.columns:
            return None
        return self.df.groupby("location")[column].sum().sort_values(ascending=False).head(n)