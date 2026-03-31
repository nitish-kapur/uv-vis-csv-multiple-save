"""
UV-Vis Plotter from CSV
Copyright (C) 2026 Nitish Kapur
GitHub: github.com/nitish-kapur
Licensed under GNU GPLv3

    This script was made as a part of a biofuel research project.

    1.  Scans the input folder for all CSV files exported from a UV-Vis
        spectrophotometer. Update the input_folder and output_folder paths
        at the top of the script to match your directory structure.

    2.  For each CSV file, reads all lines and locates the XYDATA marker
        to identify where the spectral data begins. All metadata lines
        above XYDATA (instrument name, date, settings, etc.) are
        automatically ignored. Files without an XYDATA marker are skipped.

    3.  Expected data format after the XYDATA marker:

            ... (metadata — instrument name, date, settings, etc.) ...
            XYDATA
            400.0, 0.523
            401.0, 0.511
            402.0, 0.498
            ...     ...
            ...     ...

            i.e.,
                Element         Description
                -----------     --------------------------------------------------
                Column 1        Wavelength (nm) — numeric float
                Column 2        Absorbance (A) — numeric float
                Separator       Comma (,)
                Empty lines     Skipped automatically
                Malformed lines Skipped with a console warning

    4.  Loads the parsed data into a pandas DataFrame and generates a
        matplotlib line plot with:
            - X-axis: Wavelength (nm), inverted as per UV-Vis convention
            - Y-axis: Absorbance (A)
            - Title: derived from the CSV filename

    5.  Saves each plot as a timestamped high-resolution PNG (300 dpi)
        in the output folder. The output folder is created automatically
        if it does not exist.

    6.  Reports the number of successfully processed files to the console
        upon completion.

"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- Paths ---
desktop_path = r"F:\nk"
input_folder = os.path.join(desktop_path, "raw")
output_folder = os.path.join(desktop_path, "nk")  # or any folder you want
os.makedirs(output_folder, exist_ok=True)

# --- Timestamp for filenames ---
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

files_processed = 0

for filename in sorted(os.listdir(input_folder)):
    if filename.lower().endswith(".csv"):
        print(f"Processing file: {filename}")
        file_path = os.path.join(input_folder, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        data_start_index = None
        for i, line in enumerate(lines):
            if "XYDATA" in line.upper():
                data_start_index = i + 1
                break

        if data_start_index is None:
            print(f"No data section found in {filename}, skipping.")
            continue

        data_lines = lines[data_start_index:]

        parsed_data = []
        for line in data_lines:
            line = line.strip()
            if not line:  # skip empty lines
                continue
            parts = line.split(',')
            if len(parts) == 2:
                try:
                    wavelength = float(parts[0].strip())
                    absorbance = float(parts[1].strip())
                    parsed_data.append([wavelength, absorbance])
                except ValueError:
                    print(f"Skipping non-numeric line in {filename}: {line}")
            else:
                print(f"Skipping malformed line in {filename}: {line}")

        if not parsed_data:
            print(f"No valid spectral data in {filename}, skipping.")
            continue

        files_processed += 1
        df = pd.DataFrame(parsed_data, columns=["Wavelength", "Absorbance"])
        title = os.path.splitext(filename)[0]

        plt.figure(figsize=(10, 5))
        plt.plot(df["Wavelength"], df["Absorbance"], color='green', linewidth=1)
        plt.gca().invert_xaxis()
        plt.title(f"{title} - UV-Vis Absorbance")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Absorbance (A)")
        plt.grid(True)
        plt.tight_layout()

        # Save plot as PNG file with timestamp
        save_filename = f"{title}_{timestamp}_Absorbance.png"
        save_path = os.path.join(output_folder, save_filename)
        plt.savefig(save_path, dpi=300)
        plt.close()  # Close the figure after saving

        print(f"Saved plot for {filename} as {save_filename}")

if files_processed == 0:
    print("No CSV files found or no valid data processed.")
else:
    print(f"Processed and saved plots for {files_processed} files.")
