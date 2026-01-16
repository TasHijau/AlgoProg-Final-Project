"""
Visualizer module.

Originally designed for non-GUI plotting logic.
GUI version currently handles plotting directly.
"""

import matplotlib.pyplot as plt

class Visualizer:
    def plot_top_countries(self, series, title):
        series.plot(kind="bar")
        plt.title(title)
        plt.xlabel("Category")
        plt.ylabel("Value")
        plt.tight_layout()
        plt.show()