import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector, Button
from matplotlib.path import Path
import pandas as pd
import numpy as np
import os

# Sample data
data = pd.DataFrame({
    'x': np.random.rand(100),
    'y': np.random.rand(100)
})

# File to save cleaned data
output_file = "cleaned_data.csv"
data.to_csv(output_file, index=False)  # Pre-create the file

# Variables to store the remaining points
remaining_indices = list(range(len(data)))

# Function to handle selection
def onselect(verts):
    global remaining_indices
    path = Path(verts)
    selected = path.contains_points(data.loc[remaining_indices, ['x', 'y']])
    remaining_indices[:] = [remaining_indices[i] for i in range(len(remaining_indices)) if not selected[i]]
    
    # Update plot
    ax.clear()
    ax.scatter(data.loc[remaining_indices, 'x'], data.loc[remaining_indices, 'y'], c='b')
    ax.set_title("Select points to remove")
    plt.draw()
    
    # Update the CSV file
    save_cleaned_data()

# Function to save cleaned data
def save_cleaned_data():
    cleaned_data = data.iloc[remaining_indices]
    cleaned_data.to_csv(output_file, index=False)
    print(f"Updated data saved to '{output_file}'.")

# Create the figure and scatter plot
fig, ax = plt.subplots()
scatter = ax.scatter(data['x'], data['y'], c='b')
ax.set_title("Select points to remove")

# Add LassoSelector
lasso = LassoSelector(ax, onselect)

# Add button to quit
ax_quit = plt.axes([0.8, 0.01, 0.1, 0.075])
btn_quit = Button(ax_quit, 'Quit')
btn_quit.on_clicked(lambda event: plt.close(fig))

plt.show()

