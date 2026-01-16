"""
Dashboard module.

Originally designed as the main controller for the CLI-based version
of the project. It coordinated user input, analysis, and visualization
through a text-based menu.

In the current GUI-based version, this role is handled directly by
the GUI, so this module is not actively used.
"""

class Dashboard:
    def __init__(self, analyzer, visualizer):
        self.analyzer = analyzer
        self.visualizer = visualizer

    def menu(self):
        while True:
            print("\n==== COVID DATA DASHBOARD ====")
            print("1. Show data summary")
            print("2. Show top 5 countries by total cases")
            print("3. Exit")

            choice = input("Choose: ")

            if choice == "1":
                summary = self.analyzer.basic_summary()
                print(summary)

            elif choice == "2":
                series = self.analyzer.top_countries("total_cases", 5)
                if series is not None:
                    self.visualizer.plot_top_countries(series, "Top 5 Countries by Total Cases")
                else:
                    print("Column 'total_cases' not found.")

            elif choice == "3":
                print("Exiting...")
                break

            else:
                print("Invalid choice.")