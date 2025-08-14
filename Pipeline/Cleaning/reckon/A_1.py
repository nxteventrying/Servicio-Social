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
                    self.data = pd.read_csv(filepath, sep=None, engine='python')  # Auto-detect delimiter
                elif filepath.endswith(".xlsx"):
                    self.data = pd.read_excel(filepath)
                elif filepath.endswith(".json"):
                    self.data = pd.read_json(filepath)
                else:
                    raise ValueError("Unsupported file format")

                # Handle columns
                if self.data.shape[1] == 1:
                    print('nop')
                    
                    #selected_columns = self.prompt_user_for_columns()
                    #self.data = self.data[selected_columns]
                #elif
                elif self.data.shape[1] == 2:
                    self.data.columns = ['x', 'y']
                    #self.data.columns = ['y']
                    #self.data['x'] = range(len(self.data))
                else:
                    #self.data.columns = ['x', 'y']
                    print('sorry bro, i havent been able to add that')

                # Ensure numeric values
                self.data = self.data.astype(float)

                self.remaining_indices = list(range(len(self.data)))
                self.redraw_plot()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {e}")

    def prompt_user_for_columns(self):
        """
        Allows the user to select columns from the dataset if there are more than 2.
        Returns a list of selected column names.
        """
        selected_columns = []

        # Use a dialog box to let the user choose columns
        def select_columns():
            nonlocal selected_columns
            selected_columns = [listbox.get(idx) for idx in listbox.curselection()]
            column_selector.destroy()

        column_selector = tk.Toplevel(self.root)
        column_selector.title("Select Columns")
        tk.Label(column_selector, text="Select two columns to use:").pack()
        listbox = tk.Listbox(column_selector, selectmode=tk.MULTIPLE)
        listbox.pack(fill=tk.BOTH, expand=1)

        for col in self.data.columns:
            listbox.insert(tk.END, col)

        tk.Button(column_selector, text="OK", command=select_columns).pack()
        column_selector.wait_window()  # Pause execution until selection is made

        if len(selected_columns) != 2:
            raise ValueError("You must select exactly two columns.")
        return selected_columns

    def redraw_plot(self):
        self.ax.clear()
        self.ax.scatter(self.data['x'], self.data['y'], picker=True, color='blue', s=100)
        self.ax.set_title("Lasso points to delete")
        self.ax.grid(True)  # Add grid to the plot
        self.canvas.draw()

        # Attach a new LassoSelector
        if self.lasso:
            self.lasso.disconnect_events()
        self.lasso = LassoSelector(self.ax, self.on_select)

    def on_select(self, verts):
        path = Path(verts)
        selected = path.contains_points(self.data.loc[self.remaining_indices, ['x', 'y']])
        self.remaining_indices = [self.remaining_indices[i] for i in range(len(self.remaining_indices)) if not selected[i]]

        # Update plot
        self.ax.clear()
        self.ax.scatter(
            self.data.loc[self.remaining_indices, 'x'],
            self.data.loc[self.remaining_indices, 'y'],
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
