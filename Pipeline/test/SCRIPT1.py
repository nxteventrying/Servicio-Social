import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector
from matplotlib.path import Path
import pandas as pd
import numpy as np

# Sample data
data = pd.DataFrame({
    'x': np.random.rand(100),
    'y': np.random.rand(100)
})

# Variables to store selected points
selected_indices = []

# Function to collect selected points
def onselect(verts):
    global selected_indices
    path = Path(verts)
    selected_indices = np.nonzero(path.contains_points(data[['x', 'y']]))[0]

# Create the figure and scatter plot
fig, ax = plt.subplots()
scatter = ax.scatter(data['x'], data['y'], c='b', picker=True)
lasso = LassoSelector(ax, onselect)

# Button to finalize and save
def save_cleaned_data(event):
    global selected_indices
    cleaned_data = data.iloc[selected_indices]
    cleaned_data.to_csv('cleaned_data.csv', index=False)
    print("Cleaned data saved to 'cleaned_data.csv'")
    plt.close(fig)

# Add button to save the cleaned dataset
from matplotlib.widgets import Button
ax_save = plt.axes([0.8, 0.01, 0.1, 0.075])
btn_save = Button(ax_save, 'Save')
btn_save.on_clicked(save_cleaned_data)

plt.show()

