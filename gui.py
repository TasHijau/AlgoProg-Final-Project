"""
GUI-based Data Visualization Dashboard.

This module provides a graphical user interface that allows users to:
- upload arbitrary CSV files,
- dynamically select categorical and numeric columns,
- filter data by category values,
- visualize time-series data using line plots.

The GUI version serves as the main entry point of the project and replaces
the CLI-based dashboard by using an event-driven interface.
"""

import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from tkinter import filedialog  # Provides native OS file selection dialogs
from modules.data_loader import DataLoader

csv_path = None  # Stores the path of the selected CSV file
df = None        # Stores the pandas DataFrame loaded from the CSV

# Create the main application window
root = tk.Tk()

# Frame to hold all control widgets (labels, dropdowns, buttons)
controls_frame = tk.Frame(root)
controls_frame.pack(pady=20)

# Tkinter variable that stores the currently selected numeric column
selected_column = tk.StringVar(root)
selected_column.set("")  # Initialize with an empty value

# Tkinter variable that stores the selected categorical column name
selected_category_column = tk.StringVar(root)
selected_category_column.set("")

# When the category column changes, refresh available category values
selected_category_column.trace_add(
    "write",
    lambda *args: update_category_values()
)

# Tkinter variable that stores the currently selected categorical value (e.g. country, city, driver)
selected_category_value = tk.StringVar(root)
selected_category_value.set("")

# Set the window title
root.title("Data Visualization Dashboard")

# Set the window size (width x height)
root.geometry("400x400")

# Callback function for the "Load CSV" button
def load_csv():
    global csv_path, df  # Modify variables defined outside this function

    file_path = filedialog.askopenfilename(  # Open file picker dialog
        title="Select a CSV file",
        filetypes=[("CSV files", "*.csv")]  # Restrict selection to .csv files
    )

    if not file_path:
        return  # User cancelled the file selection

    csv_path = file_path  # Store selected file path
    loader = DataLoader(csv_path)  # Create a DataLoader for the selected CSV
    df = loader.load()  # Attempt to load CSV into a DataFrame

    # Check whether loading was successful
    if df is None:
        print("Failed to load CSV.")
    else:
        print(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        print("Columns:", list(df.columns))

        # Get categorical columns by selecting non-numeric columns
        # and excluding the date column (dates are used for the x-axis, not grouping)
        categorical_columns = [
            col for col in df.select_dtypes(exclude="number").columns
            if col.lower() != "date"
        ]

        if not categorical_columns:
            print("No categorical columns found.")
            return
        
        # Set default categorical column
        selected_category_column.set(categorical_columns[0])

        # Populate category-column dropdown
        menu_cat_col = category_column_menu["menu"]
        menu_cat_col.delete(0, "end")  # Remove old dropdown items when a new CSV is loaded

        for col in categorical_columns:
            menu_cat_col.add_command(
                label=col,
                command=lambda value=col: selected_category_column.set(value)  
                # Update selected_category_column when this option is chosen
            )

        print ("Categorical columns:", categorical_columns)

        # Extract numeric columns only (required for plotting)
        numeric_columns = df.select_dtypes(include="number").columns.tolist()

        if not numeric_columns:
            print("No numeric columns found.")
            return

        # Set default dropdown selection
        selected_column.set(numeric_columns[0])

        # Clear old dropdown items when a new CSV is loaded
        menu = column_menu["menu"]
        menu.delete(0, "end")

        # Add new dropdown options dynamically
        for col in numeric_columns:
            menu.add_command(
                label=col,
                command=lambda value=col: selected_column.set(value)  
                # Update selected_column when this option is chosen
            )

        print("Numeric columns:", numeric_columns)

        update_category_values()

# Populate category values based on the selected category column
def update_category_values():
    # Get the currently selected category column (e.g. location, city, driver)
    col = selected_category_column.get()

    # Exit if no column is selected or data is not loaded
    if not col or df is None:
        return

    # Extract all unique, non-empty values from the selected category column
    values = df[col].dropna().unique().tolist()
    if not values:
        print("No values found for selected category column.")
        return

    # Set the first value as the default selection
    selected_category_value.set(values[0])

    # Clear previous options from the category-value dropdown
    menu_val = category_menu["menu"]
    menu_val.delete(0, "end")

    # Add new dropdown options dynamically
    for v in values:
        menu_val.add_command(
            label=v,
            command=lambda value=v: selected_category_value.set(value)
            # Update selected_category_value when this option is chosen
        )

# Callback function for the "Plot" button
def plot_column():
    # Prevent plotting if no CSV has been loaded
    if df is None:
        print("No data loaded.")
        return

    # Get the selected numeric column, category column, and category value
    column = selected_column.get()
    category_col = selected_category_column.get()
    category_val = selected_category_value.get()

    # Ensure all required selections are made before plotting
    if not column or not category_col or not category_val:
        print("Column or category not selected.")
        return
    
    # Ensure the dataset contains a date column for time-series plotting
    if "date" not in df.columns:
        print("No date column found.")
        return

    # Filter rows that match the selected category value
    filtered = df[df[category_col] == category_val]

    # Group data by date and sum the selected numeric column
    grouped = (
        filtered
        .groupby("date")[column]   
        .sum()                     
        .sort_index()              # Ensure dates are in chronological order
    )

    # Create a new matplotlib figure
    plt.figure()

    # Plot date on x-axis and aggregated values on y-axis
    plt.plot(grouped.index, grouped.values)

    # Disable scientific notation on the y-axis for readability
    plt.ticklabel_format(style="plain", axis="y")

    # Set plot title and axis labels for clarity
    plt.title(f"{column} over time for {category_val}")
    plt.xlabel("Date")
    plt.ylabel(column)

    # Rotate x-axis labels and adjust layout to improve readability
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Format y-axis values with commas
    plt.gca().yaxis.set_major_formatter(
        mtick.StrMethodFormatter('{x:,.0f}')
    )

    # Display the plot window
    plt.show()

# Create the "Load CSV" button
load_button = tk.Button(
    controls_frame,
    text="Load CSV",
    command=load_csv  # Function executed when the button is clicked
)
load_button.pack(pady=20)  # Add vertical spacing around the button

# Create the label for category column
tk.Label(
    controls_frame, 
    text="Group by (category column):"
).pack()

# Create the dropdown menu for category column
category_column_menu = tk.OptionMenu(
    controls_frame, 
    selected_category_column, 
    ""
)
category_column_menu.pack(pady=5)

# Create the label for category value
tk.Label(
    controls_frame,
    text="Select category value:"
).pack()

# Create the dropdown menu for category value
category_menu = tk.OptionMenu(
    controls_frame, 
    selected_category_value, 
    ""
)
category_menu.pack(pady=5)

# Create the label for numeric columns menu
tk.Label(
    controls_frame, 
    text="Select numeric column to plot:"
).pack()

# Create the dropdown menu for numeric columns
column_menu = tk.OptionMenu(
    controls_frame,
    selected_column,
    ""
)
column_menu.pack(pady=5)

# Create the "Plot" button
plot_button = tk.Button(
    controls_frame,
    text="Plot",
    command=plot_column
)
plot_button.pack(pady=15)

# Start the GUI event loop
root.mainloop()