import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_csv(file_path):
    try:
        # Read the CSV file
        data = pd.read_csv(file_path, header=None)

        # Determine x and y columns
        if data.shape[1] == 2:  # Two columns
            x = data.iloc[:, 0]
            y = data.iloc[:, 1]
        elif data.shape[1] == 1:  # One column
            x = range(len(data))
            y = data.iloc[:, 0]
        else:
            raise ValueError("CSV must have 1 or 2 columns")

        # Plot the data
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, y, marker='o', linestyle='-', color='b')
        ax.set_title("CSV Plot")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        # Clear the canvas and display the new plot
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        canvas.draw()

    except Exception as e:
        status_label.config(text=f"Error: {e}")

def handle_file_drop(event):
    file_path = event.data.strip()  # Get the file path
    if file_path.endswith('.csv'):
        status_label.config(text=f"File loaded: {file_path}")
        plot_csv(file_path)
    else:
        status_label.config(text="Please drop a valid CSV file")

# Initialize TkinterDnD application
root = TkinterDnD.Tk()  # Use TkinterDnD.Tk() instead of tk.Tk()
root.title("CSV Plotter")
root.geometry("800x600")

# Drop area label
drop_label = tk.Label(root, text="Drop your CSV file here", relief="ridge", width=50, height=10)
drop_label.pack(pady=20)

# Bind file drop event
drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind('<<Drop>>', handle_file_drop)

# Frame for canvas
canvas_frame = tk.Frame(root)
canvas_frame.pack(fill="both", expand=True, pady=20)

# Status label
status_label = tk.Label(root, text="Waiting for a file...", relief="sunken", anchor="w")
status_label.pack(fill="x", side="bottom")

# Run the app
root.mainloop()
