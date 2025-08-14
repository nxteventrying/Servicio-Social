import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector
from matplotlib.path import Path
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import time


class InteractivePlotApp:
    def __init__(self, root):
        self.root = root
        self.data = None
        self.remaining_indices = []
        self.undo_stack = []
        self.redo_stack = []
        self.filename = ""

        # Color ranges
        self.color_ranges = []

        # Create the figure and plot
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        self.lasso = None

        # Add buttons
        self.save_button = tk.Button(root, text="Save to CSV", command=self.save_to_csv)
        self.save_button.pack()

        self.load_button = tk.Button(root, text="Load Data", command=self.load_data)
        self.load_button.pack()

        self.set_colors_button = tk.Button(root, text="Set Color Ranges", command=self.set_color_ranges)
        self.set_colors_button.pack()

        self.undo_button = tk.Button(root, text="Undo (Ctrl+Z)", command=self.undo)
        self.undo_button.pack()

        self.redo_button = tk.Button(root, text="Redo (Ctrl+Y)", command=self.redo)
        self.redo_button.pack()

        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack()

        # Bind keyboard shortcuts
        root.bind("<Control-z>", lambda event: self.undo())
        root.bind("<Control-y>", lambda event: self.redo())

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
                self.filename = os.path.splitext(os.path.basename(filepath))[0]
                if filepath.endswith(".csv") or filepath.endswith(".txt"):
                    self.data = pd.read_csv(filepath, sep=None, engine='python')
                elif filepath.endswith(".xlsx"):
                    self.data = pd.read_excel(filepath)
                elif filepath.endswith(".json"):
                    self.data = pd.read_json(filepath)
                else:
                    raise ValueError("Unsupported file format")

                if self.data.shape[1] == 2:
                    if self.data.iloc[:, 0].isna().all():
                        self.data.iloc[:, 0] = range(1, len(self.data) + 1)
                    self.data.columns = ['time', 'RR']
                else:
                    raise ValueError("Dataset must have exactly two columns.")

                self.data = self.data.astype(float)
                self.remaining_indices = list(range(len(self.data)))
                self.redraw_plot()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {e}")

    def set_color_ranges(self):
        self.color_ranges = []
        while True:
            range_str = simpledialog.askstring("Input Range", "Enter range (start,end,color) or type 'done':")
            if range_str.lower() == 'done':
                break
            try:
                start, end, color = range_str.split(",")
                start, end = float(start), float(end)
                self.color_ranges.append((start, end, color.strip()))
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter the range as start,end,color")

        self.redraw_plot()

    def redraw_plot(self):
        self.ax.clear()

        # Set title and labels
        self.ax.set_title(self.filename)
        self.ax.set_xlabel("Time (seconds)")
        self.ax.set_ylabel("RR")

        # Apply color ranges
        for start, end, color in self.color_ranges:
            indices_in_range = self.data.index[
                (self.data['time'] >= start) & (self.data['time'] < end)
            ]
            self.ax.scatter(
                self.data.loc[indices_in_range, 'time'],
                self.data.loc[indices_in_range, 'RR'],
                color=color,
                label=f"{start}-{end} sec"
            )

        # Plot remaining points
        self.ax.scatter(
            self.data.loc[self.remaining_indices, 'time'],
            self.data.loc[self.remaining_indices, 'RR'],
            color='blue', label="Remaining Points"
        )

        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

        if self.lasso:
            self.lasso.disconnect_events()
        self.lasso = LassoSelector(self.ax, self.on_select)

    def on_select(self, verts):
        path = Path(verts)
        selected = path.contains_points(self.data.loc[self.remaining_indices, ['time', 'RR']])

        selected_indices = [self.remaining_indices[i] for i in range(len(self.remaining_indices)) if selected[i]]

        # Highlight selected points
        self.ax.scatter(
            self.data.loc[selected_indices, 'time'],
            self.data.loc[selected_indices, 'RR'],
            color='red'
        )
        self.canvas.draw()
        self.root.update_idletasks()
        time.sleep(1)

        # Save to undo stack and clear redo stack
        self.undo_stack.append(selected_indices)
        self.redo_stack.clear()

        # Remove points from remaining indices
        self.remaining_indices = [idx for idx in self.remaining_indices if idx not in selected_indices]

        # Update plot
        self.redraw_remaining_points()

    def redraw_remaining_points(self):
        self.redraw_plot()

    def undo(self):
        if self.undo_stack:
            last_deleted = self.undo_stack.pop()
            self.redo_stack.append(last_deleted)
            self.remaining_indices.extend(last_deleted)
            self.remaining_indices.sort()
            self.redraw_remaining_points()
        else:
            messagebox.showinfo("Undo", "No actions to undo.")

    def redo(self):
        if self.redo_stack:
            last_undone = self.redo_stack.pop()
            self.undo_stack.append(last_undone)
            self.remaining_indices = [idx for idx in self.remaining_indices if idx not in last_undone]
            self.redraw_remaining_points()
        else:
            messagebox.showinfo("Redo", "No actions to redo.")

    def save_to_csv(self):
        if self.data is not None:
            filename = filedialog.asksaveasfilename(
                title="Save CSV",
                defaultextension=".csv",
                filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
            )
            if filename:
                cleaned_data = self.data.iloc[self.remaining_indices]
                cleaned_data.to_csv(filename, index=False, header=False)
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
