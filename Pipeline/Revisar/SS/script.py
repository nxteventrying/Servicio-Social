import sys
import re
import matplotlib.pyplot as plt
import numpy as np

# Get file path from command-line argument
file_path = sys.argv[1]

# Load data from the provided file
data = np.loadtxt(file_path)

# Extract the protocol and subject acronym using regex from file name
file_name = file_path.split("\\")[-1]  # Extracts the file name from the path
name = re.search(r"([a-zA-Z]+)", file_name).group(1)
protocol = re.search(r"\d+[a-z]*([A-Z])", file_name).group(1)

print("Name:", name)
print("Protocol:", protocol)

# Timeline restrictions
Rest = 7 * 60        # 7 minutes of rest
Warming_up = 9 * 60  # 2 minutes of warming up
Exercise = 20 * 60   # 11 minutes of exercise
Recovery = 32 * 60   # 12 minutes of recovery

# Filter out zero values
filtered_data = data[data[:, 1] != 0]
hrv_data = filtered_data[:, 1]

# Function to plot the raw data and the timeline restrictions
def plot_data(file_path):
    AA = np.loadtxt(file_path)
    plt.figure(figsize=(8, 6), dpi=80)
    plt.plot(AA[:, 0], AA[:, 1], '.')
    plt.xlim(0, 32)
    plt.ylim(550, 1150)
    plt.xlabel("Time (s)")
    plt.ylabel("RR (ms)")
    plt.title("HRV Data with Timeline Restrictions")
    plt.axvline(x=Rest, color='r', linestyle='--')
    plt.axvline(x=Warming_up, color='r', linestyle='--')
    plt.axvline(x=Exercise, color='r', linestyle='--')
    plt.axvline(x=Recovery, color='r', linestyle='--')
    plt.grid(True)
    plt.show()

# Poincare plot function
def Poincare_plot(hrv_data):
    x = []
    y = []
    # Compute RR intervals and generate Poincare plot
    for i in range(len(hrv_data) - 1):
        x.append(hrv_data[i])     # RR(n)
        y.append(hrv_data[i + 1]) # RR(n+1)
    plt.figure(figsize=(8, 6), dpi=80)
    plt.plot(x, y, '.')
    plt.xlabel("RR(n)")
    plt.ylabel("RR(n+1)")
    plt.title("Poincaré Plot")
    plt.grid(True)
    plt.show()

# Call the plotting functions
plot_data(file_path)
Poincare_plot(hrv_data)
