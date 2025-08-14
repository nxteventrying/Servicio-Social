import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector
from matplotlib.path import Path
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class InteractivePlotApp:
    def __init__(self, root):
        self.root = root
        self.data = None
        self.remaining_indices = []

        # Create the figure and plot
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        # Lasso selector and storage for selected points
        self.lasso = None

        # Add buttons
        self.save_button = tk.Button(root, text="Save to CSV", command=self.save_to_csv)
        self.save_button.pack()

        self.load_button = tk.Button(root, text="Load Data", command=self.load_data)
        self.load_button.pack()

        # Quit button
        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack()

    def load_data(self):
        filepath = filedialog.askopenfilename(
            title="Select a Data File",
            filetypes=(
                ("CSV Files", "*.csv"),
                ("Text Files", "*.txt"),
                ("Excel Files", "*.xlsx"),
                ("JSON Files", "*.json"),
                ("All Files", "*.*")
            )
        )
        if filepath:
            try:
                # Handle different file types
                if filepath.endswith(".csv") or filepath.endswith(".txt"):
                    self.data = pd.read_csv(filepath, sep=",", engine='python', header=0)  # Ensure header is explicitly loaded
                elif filepath.endswith(".xlsx"):
                    self.data = pd.read_excel(filepath)
                elif filepath.endswith(".json"):
                    self.data = pd.read_json(filepath)
                else:
                    raise ValueError("Unsupported file format")

                # Handle single-column and two-column data
                if self.data.shape[1] == 1:
                    # Single-column data (assumes it’s 'Time')
                    self.data['RtoR'] = None  # Create the second column (RtoR), can be filled with NaN
                    self.data['Time'] = pd.to_numeric(self.data[self.data.columns[0]], errors='coerce')
                    self.data['Time'] = self.data['Time'].fillna(pd.Series(range(1, len(self.data) + 1)))  # Fix chained assignment warning
                elif self.data.shape[1] == 2:
                    # Two-column data
                    self.data.columns = ['Time', 'RtoR']  # Ensure these columns are correctly named
                    self.data = self.data.apply(pd.to_numeric, errors='coerce').dropna()  # Convert values to numeric and drop NaNs
                else:
                    raise ValueError("Data must have one or two columns")

                self.remaining_indices = list(range(len(self.data)))
                self.redraw_plot()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {e}")

    def redraw_plot(self):
        self.ax.clear()
        self.ax.scatter(self.data['Time'], self.data['RtoR'], picker=True, color='blue', s=100)
        self.ax.set_title("Lasso points to delete")
        self.ax.grid(True)  # Add grid to the plot
        self.canvas.draw()

        # Attach a new LassoSelector
        if self.lasso:
            self.lasso.disconnect_events()
        self.lasso = LassoSelector(self.ax, self.on_select)

    def on_select(self, verts):
        path = Path(verts)
        selected = path.contains_points(self.data[['Time', 'RtoR']].iloc[self.remaining_indices])
        self.remaining_indices = [self.remaining_indices[i] for i in range(len(self.remaining_indices)) if not selected[i]]

        # Update plot
        self.ax.clear()
        self.ax.scatter(
            self.data.iloc[self.remaining_indices]['Time'],
            self.data.iloc[self.remaining_indices]['RtoR'],
            color='blue'
        )
        self.ax.set_title("Lasso points to delete")
        self.ax.grid(True)  # Add grid to the plot
        self.canvas.draw()

    def save_to_csv(self):
        if self.data is not None:
            filename = filedialog.asksaveasfilename(
                title="Save CSV",
                defaultextension=".csv",
                filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
            )
            if filename:
                cleaned_data = self.data.iloc[self.remaining_indices]
                cleaned_data.to_csv(filename, index=False)
                messagebox.showinfo("Success", f"Data saved to {filename}")
            else:
                messagebox.showwarning("Canceled", "Save operation canceled")
        else:
            messagebox.showerror("No Data", "No data to save. Load a dataset first.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Interactive Data Cleaner")
    app = InteractivePlotApp(root)
    root.mainloop()
