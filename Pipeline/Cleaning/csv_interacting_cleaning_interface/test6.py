import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
except ImportError:
    messagebox.showerror("Missing Module", "Please install tkinterdnd2: pip install tkinterdnd2")
    raise

class DragAndDropPlotter:
    def __init__(self, root):
        self.root = root
        self.root.title("Drag and Drop CSV Plotter")
        
        # Instruction label
        self.label = tk.Label(root, text="Drop CSV file here", bg="lightgray", fg="black", width=40, height=10)
        self.label.pack(pady=20)
        
        # Enable drag-and-drop
        root.drop_target_register(DND_FILES)
        root.dnd_bind('<<Drop>>', self.on_drop)
        
        # Canvas for plotting
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def on_drop(self, event):
        filepath = event.data.strip()
        if filepath.endswith('.csv'):
            try:
                data = pd.read_csv(filepath)
                if 'x' in data.columns and 'y' in data.columns:
                    self.plot_data(data)
                else:
                    messagebox.showerror("Invalid Data", "CSV must contain 'x' and 'y' columns.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV: {e}")
        else:
            messagebox.showerror("Invalid File", "Only CSV files are supported.")
    
    def plot_data(self, data):
        self.ax.clear()
        self.ax.plot(data['x'], data['y'], marker='o', linestyle='-', color='blue')
        self.ax.set_title("CSV Data Plot")
        self.canvas.draw()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = DragAndDropPlotter(root)
    root.mainloop()
