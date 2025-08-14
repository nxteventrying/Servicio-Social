import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector
from matplotlib.path import Path
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class InteractivePlotApp:
    def __init__(self, root):
        self.root = root
        self.data = None
        self.remaining_indices = []
        self.x_col = None
        self.y_col = None

        # Create the figure and plot
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        # Lasso selector
        self.lasso = None

        # Add buttons
        self.load_button = tk.Button(root, text="Load Data", command=self.load_data)
        self.load_button.pack()

        self.column_select_button = tk.Button(root, text="Select Columns", command=self.select_columns, state=tk.DISABLED)
        self.column_select_button.pack()

        self.save_button = tk.Button(root, text="Save to CSV", command=self.save_to_csv, state=tk.DISABLED)
        self.save_button.pack()

        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack()

    def load_data(self):
        filepath = filedialog.askopenfilename(
            title="Select a Data File",
            filetypes=(("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if filepath:
            try:
                if filepath.endswith(".csv"):
                    self.data = pd.read_csv(filepath)
                elif filepath.endswith(".txt"):
                    self.data = pd.read_csv(filepath, delim_whitespace=True)
                else:
                    raise ValueError("Unsupported file format")

                if len(self.data.columns) < 2:
                    messagebox.showerror("Insufficient Columns", "The file must contain at least two columns for plotting.")
                    self.data = None
                else:
                    self.column_select_button.config(state=tk.NORMAL)
                    self.save_button.config(state=tk.NORMAL)
                    messagebox.showinfo("Data Loaded", f"File loaded successfully with {len(self.data.columns)} columns.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {e}")

    def select_columns(self):
        if self.data is not None:
            columns = self.data.columns.tolist()

            # Ask for x-axis column
            self.x_col = simpledialog.askstring("Select X Column", f"Available columns: {columns}\nEnter column name for X-axis:")
            if self.x_col not in columns:
                messagebox.showerror("Invalid Column", "Selected column for X-axis is invalid.")
                return

            # Ask for y-axis column
            self.y_col = simpledialog.askstring("Select Y Column", f"Available columns: {columns}\nEnter column name for Y-axis:")
            if self.y_col not in columns:
                messagebox.showerror("Invalid Column", "Selected column for Y-axis is invalid.")
                return

            self.remaining_indices = list(range(len(self.data)))
            self.redraw_plot()
        else:
            messagebox.showerror("No Data", "No data loaded. Load a dataset first.")

    def redraw_plot(self):
        self.ax.clear()
        self.ax.scatter(self.data[self.x_col], self.data[self.y_col], picker=True, color='blue', s=100)
        self.ax.set_title(f"Plotting '{self.x_col}' vs '{self.y_col}'. Lasso to remove points.")
        self.canvas.draw()

        # Attach a new LassoSelector
        if self.lasso:
            self.lasso.disconnect_events()
        self.lasso = LassoSelector(self.ax, self.on_select)

    def on_select(self, verts):
        if self.data is not None and self.x_col and self.y_col:
            path = Path(verts)
            points = self.data.loc[self.remaining_indices, [self.x_col, self.y_col]].values
            selected = path.contains_points(points)
            self.remaining_indices = [self.remaining_indices[i] for i in range(len(self.remaining_indices)) if not selected[i]]

            # Update plot
            self.ax.clear()
            self.ax.scatter(
                self.data.loc[self.remaining_indices, self.x_col],
                self.data.loc[self.remaining_indices, self.y_col],
                color='blue'
            )
            self.ax.set_title(f"Plotting '{self.x_col}' vs '{self.y_col}'. Lasso to remove points.")
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
