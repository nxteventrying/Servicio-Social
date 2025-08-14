import os
import re
import glob
import numpy as np
import matplotlib.pyplot as plt
import csv
from collections import defaultdict
# Function to calculate SD1 and SD2
def calculate_sd1_sd2(series):
    n = len(series)
    mean_rr = np.mean(series)
    
    # Calculate SD1
    diff_rr = np.diff(series) / np.sqrt(2)
    sd1 = np.sqrt(np.sum(diff_rr**2) / (n - 1))
    
    # Calculate SD2
    sd2_term = (series[:-1] + series[1:] - 2 * mean_rr) / np.sqrt(2)
    sd2 = np.sqrt(np.sum(sd2_term**2) / (n - 1))
    
    return sd1, sd2

# Function to calculate RR mean, SD1, SD2, and standard deviation for each interval
def calculate_interval_statistics(time_data, hrv_data):
    intervals = {
        'Rest': (1, 6),
        'Exercise': (14, 19),
        'Recovery': (25, 30)
    }
    
    stats = {}
    
    for interval, (start, end) in intervals.items():
        mask = (time_data >= start) & (time_data < end)
        interval_data = hrv_data[mask]
        
        if len(interval_data) > 1:  # Ensure there's enough data for SD calculation
            rr_mean = np.mean(interval_data)
            sd1, sd2 = calculate_sd1_sd2(interval_data)
            rr_std = np.std(interval_data)  # Calculate standard deviation
            stats[interval] = {
                'Mean': rr_mean,
                'Standard Deviation': rr_std,
                'SD1': sd1,
                'SD2': sd2
            }
    
    return stats


def plot_data(ax, time_data, hrv_data, filename, stats):
    # Define timeline markers
    Rest = 7
    Exercise = 20
    Recovery = 32

    colors = {'Rest': 'blue', 'Exercise': 'orange', 'Recovery': 'purple'}
    
    # Plot each point with color-coded intervals
    for i in range(len(time_data)):
        if time_data[i] < Rest:
            color = colors['Rest']
        elif time_data[i] < Exercise:
            color = colors['Exercise']
        elif time_data[i] < Recovery:
            color = colors['Recovery']
        else:
            continue
        ax.plot(time_data[i], hrv_data[i], '.', color=color)
    
    # Plot green vertical lines to mark intervals
    ax.axhline(y= hrv_data.min(), color='r', linestyle='-')

    ax.axvline(x=1, color='g', linestyle='-')
    ax.axvline(x=6, color='g', linestyle='-')
    ax.axvline(x=14, color='g', linestyle='--')
    ax.axvline(x=19, color='g', linestyle='--')
    ax.axvline(x=25, color='g', linestyle='-')
    ax.axvline(x=30, color='g', linestyle='-')
    
    # Modify the region texts dynamically based on calculated stats
    region_positions = {'Rest': 3.5,
                        'Exercise': 16.5,
                        'Recovery': 27.5
                       }

    # Loop over regions and stats
    for region, x_pos in region_positions.items():
        if region in stats:  # Check if stats for the region exist
            rr_mean = stats[region]['Mean']
            rr_std = stats[region]['Standard Deviation']
            text_str = f"Mean RR: {rr_mean:.2f} ms\nSTD RR: {rr_std:.2f} ms"
            # Add the text for each region at the corresponding position
            ax.text(x_pos, hrv_data.max() + 10, text_str, fontsize=10, 
                    verticalalignment='top', horizontalalignment='center',
                    bbox=dict(facecolor='white', alpha=0.8))

    # Set axis limits, title, labels, and grid
    ax.set_ylim(hrv_data.min() - 50, hrv_data.max() + 50)
    ax.set_title(f"RR {filename}")  # Include filename in title
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("RR (ms)")
    ax.grid(True)


# Poincare plot function with color coding and filename in title
def poincare_plot(ax, hrv_data, time_data, filename):
    x = []
    y = []
    colors = {'Rest': 'blue', 'Exercise': 'orange', 'Recovery': 'purple'}
    color_x = []

    Rest = 7
    Exercise = 20
    Recovery = 32

    for i in range(len(hrv_data) - 1):
        x.append(hrv_data[i])     # RR(n)
        y.append(hrv_data[i + 1]) # RR(n+1)
        # Determine color based on the time of RR(n) and RR(n+1)
        if time_data[i] < Rest:
            color_x.append(colors['Rest'])
        elif time_data[i] < Exercise:
            color_x.append(colors['Exercise'])
        elif time_data[i] < Recovery:
            color_x.append(colors['Recovery'])
        else:
            continue

    ax.scatter(x, y, c=color_x, s=10)  # Use c=color_x directly
    ax.set_title(f"Poincaré {filename}")  # Include filename in title
    ax.set_xlabel("RR(n)")
    ax.set_ylabel("RR(n+1)")
    ax.grid(True)

# Main pipeline function with error handling for file processing
def process_files(data_folder, output_folder, csv_filename):
    txt_files = glob.glob(os.path.join(data_folder, "*.txt"))
    
    # List all .txt files in the folder
    filenames = os.listdir(data_folder)
    
    # Group files by prefix up to the first number
    file_groups = defaultdict(list)
    pattern = re.compile(r"([a-zA-Z]+)(\d+)")  # Regex to extract the prefix and number
    
    # Process each filename
    for filename in filenames:
        match = pattern.match(filename)
        if match:
            prefix = match.group(1)
            number = int(match.group(2))  # Extract the number
            file_groups[prefix].append((filename, number))

    # Sort each group by the number part
    sorted_filenames = []
    for prefix, files in file_groups.items():
        sorted_files = sorted(files, key=lambda x: x[1])  # Sort by the number
        sorted_filenames.extend([file[0] for file in sorted_files])  # Add sorted filenames to the list
    
    # Prepare CSV file for writing
    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write a single header row
        header = ['Filename', 
              'Rest Mean', 'Rest Std', 'Rest SD1', 'Rest SD2', 
              'Exercise Mean', 'Exercise Std', 'Exercise SD1', 'Exercise SD2', 
              'Recovery Mean', 'Recovery Std', 'Recovery SD1', 'Recovery SD2']
        writer.writerow(header)
        
        # List to track problematic files
        failed_files = []
        
        # Loop through each sorted file and process
        for filename in sorted_filenames:
            file_path = os.path.join(data_folder, filename)  # Get the full path of the file
            try:
                # Try loading the file, catching any errors in the process
                data = np.loadtxt(file_path)
                filtered_data = data[data[:, 1] != 0]  # Filter out zero values
                time_data = filtered_data[:, 0]
                hrv_data = filtered_data[:, 1]
                
                # Calculate statistics
                stats = calculate_interval_statistics(time_data, hrv_data)
                
                # Collect data for all regions (Rest, Exercise, Recovery)
                row = [os.path.basename(file_path)]

                # Append SD1 and SD2 for each region
                for region in ['Rest', 'Exercise', 'Recovery']:
                    if region in stats:
                        row.extend([
                            stats[region]['Mean'],
                            stats[region]['Standard Deviation'],
                            stats[region]['SD1'], 
                            stats[region]['SD2']
                        ])
                    else:
                        row.extend([None, None])  # If not enough data for the region, append Nones
                
                # Write the collected row for this file
                writer.writerow(row)
                
                # Create a subplot for side-by-side plots
                fig, axes = plt.subplots(1, 2, figsize=(30, 8))  # 1 row, 2 columns
                
                # Extract the filename without extension
                filename_without_extension = os.path.splitext(os.path.basename(file_path))[0]
                
                # Plot data and Poincare plot side by side with filename in title
                plot_data(axes[0], time_data, hrv_data, filename_without_extension, stats)  # HRV data on the left
                poincare_plot(axes[1], hrv_data, time_data, filename_without_extension)  # Poincare plot on the right
                
                # Adjust layout and save the plot
                plt.subplots_adjust(wspace=1)
                plot_filename = os.path.join(output_folder, filename_without_extension + '_subplot.png')
                plt.savefig(plot_filename)
                plt.close()
            
            except ValueError as ve:
                print(f"ValueError for file {file_path}: {ve}")
                failed_files.append(file_path)  # Add file to failed list
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                failed_files.append(file_path)  # Add file to failed list

    # Print the list of files that couldn't be processed
    if failed_files:
        print("\nThe following files could not be processed:")
        for failed_file in failed_files:
            print(failed_file)
    else:
        print("\nAll files processed successfully!")

if __name__ == "__main__":
    # Define folder paths
    data_folder = "Lazy"  # Folder with .txt files
    output_folder = "Plots_Lazy"       # Folder to save plots
    csv_filename = "Lazy.csv"   # Output CSV file
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process the files and generate output
    process_files(data_folder, output_folder, csv_filename)

