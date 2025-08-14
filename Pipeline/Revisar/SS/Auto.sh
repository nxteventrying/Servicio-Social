#!/bin/bash

# Define the folder path where your HRV text files are located
folder_path="/path/to/your/HRV/files"

# Loop through all .txt files in the folder
for file in "$folder_path"/*.txt; do
    # Call the Python script and pass the file as an argument
    python3 your_python_script.py "$file"
done
