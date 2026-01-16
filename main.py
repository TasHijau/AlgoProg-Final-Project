"""
Main entry point for the CLI-based version of the project.

This script initializes the data loader, analyzer, visualizer,
and dashboard components, then starts an interactive text-based
menu for exploring the dataset.

The current GUI-based version uses gui.py as the main entry point,
so this file is kept for architectural completeness and reference.
"""

from modules.data_loader import DataLoader
from modules.analyzer import Analyzer
from modules.visualizer import Visualizer
from modules.dashboard import Dashboard

def main():
    loader = DataLoader("data/covid.csv")
    df = loader.load()

    if df is None:
        print("Failed to load dataset.")
        return

    analyzer = Analyzer(df)
    visualizer = Visualizer()
    dashboard = Dashboard(analyzer, visualizer)

    dashboard.menu()

if __name__ == "__main__":
    main()