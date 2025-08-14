import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Sample CSV reading function (replace with your actual file)
def load_csv_data():
    data = pd.DataFrame({'x': range(11), 'y': range(11)})
    return data

class InteractivePlotApp:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        
        # Create the figure and plot
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        
        self.scatter = self.ax.scatter(self.data['x'], self.data['y'], picker=True, color='blue', s=100)
        self.canvas.mpl_connect('pick_event', self.on_pick)
        
        self.redraw_plot()

    def on_pick(self, event):
        ind = event.ind[0]  # Get index of picked point
        x, y = self.data.loc[ind, ['x', 'y']]
        if messagebox.askyesno("Delete Point", f"Delete point ({x}, {y})?"):
            self.data = self.data.drop(index=ind).reset_index(drop=True)
            self.redraw_plot()
    
    def redraw_plot(self):
        self.ax.clear()
        self.ax.scatter(self.data['x'], self.data['y'], picker=True, color='blue', s=100)
        self.ax.set_title("Click a point to delete it")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Interactive Plot with Tkinter")

    # Load CSV data
    data = load_csv_data()

    app = InteractivePlotApp(root, data)
    root.mainloop()
