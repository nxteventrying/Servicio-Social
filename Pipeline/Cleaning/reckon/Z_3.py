import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector
from matplotlib.path import Path
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time


class InteractivePlotApp:
    def __init__(self, root):
        self.root = root
        self.data = None
        self.remaining_indices = []
        self.undo_stack = []  # To track deletions for undo
        self.redo_stack = []  # To track re-deletions for redo

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

        # Undo and Redo buttons
        self.undo_button = tk.Button(root, text="Undo (Ctrl+Z)", command=self.undo)
        self.undo_button.pack()

        self.redo_button = tk.Button(root, text="Redo (Ctrl+Y)", command=self.redo)
        self.redo_button.pack()

        # Quit button
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
                if filepath.endswith(".csv") or filepath.endswith(".txt"):
                    self.data = pd.read_csv(filepath, sep=None, engine='python')  # Auto-detect delimiter
                elif filepath.endswith(".xlsx"):
                    self.data = pd.read_excel(filepath)
                elif filepath.endswith(".json"):
                    self.data = pd.read_json(filepath)
                else:
                    raise ValueError("Unsupported file format")

                if self.data.shape[1] == 2:
                    if self.data.iloc[:, 0].isna().all():
                        self.data.iloc[:, 0] = range(1, len(self.data) + 1)
                    self.data.columns = ['x', 'y']
                else:
                    raise ValueError("Dataset must have exactly two columns.")

                self.data = self.data.astype(float)
                self.remaining_indices = list(range(len(self.data)))
                self.redraw_plot()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {e}")

    def redraw_plot(self):
        self.ax.clear()
        self.ax.scatter(self.data['x'], self.data['y'], picker=True, color='blue', s=5)
        self.ax.set_title("Lasso points to delete")
        self.ax.grid(True)
        self.canvas.draw()

        if self.lasso:
            self.lasso.disconnect_events()
        self.lasso = LassoSelector(self.ax, self.on_select)

    def on_select(self, verts):
        path = Path(verts)
        selected = path.contains_points(self.data.loc[self.remaining_indices, ['x', 'y']])

        selected_indices = [self.remaining_indices[i] for i in range(len(self.remaining_indices)) if selected[i]]

        # Highlight selected points
        self.ax.scatter(
            self.data.loc[selected_indices, 'x'],
            self.data.loc[selected_indices, 'y'],
            color='red',
            s=5
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
        self.ax.clear()
        self.ax.scatter(
            self.data.loc[self.remaining_indices, 'x'],
            self.data.loc[self.remaining_indices, 'y'],
            color='blue',
            s=5
        )
        self.ax.set_title("Lasso points to delete")
        self.ax.grid(True)
        self.canvas.draw()

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
