# UV-Vis Plotter from CSV

A Python script that batch processes UV-Vis absorbance spectra from CSV files and saves individual plots as high-resolution PNG images.

## Author

**Nitish Kapur**<br>
GitHub: [github.com/nitish-kapur](https://github.com/nitish-kapur)

## Expected Input Format

The script expects CSV files exported from a UV-Vis spectrophotometer. Each file must contain an `XYDATA` marker line, after which the spectral data begins in two comma-separated columns:
```
... (metadata — instrument name, date, settings, etc.) ...
XYDATA
400.0, 0.523
401.0, 0.511
402.0, 0.498
...
```

| Element | Description |
|---|---|
| Metadata lines | Any number of lines before `XYDATA` — automatically ignored by the parser |
| `XYDATA` marker | Signals the end of metadata; data parsing begins on the next line |
| Column 1 | Wavelength (nm) — must be a numeric float |
| Column 2 | Absorbance (A) — must be a numeric float |
| Separator | Comma (`,`) |
| Empty lines | Skipped automatically |
| Malformed lines | Lines with fewer or more than two values are skipped with a console warning |

## Requirements

pip install pandas matplotlib

## Configuration

The input and output folder paths are hard-coded at the top of the script. Update these to match your directory structure:

    input_folder  = os.path.join(desktop_path, "raw")   # Folder containing CSV files
    output_folder = os.path.join(desktop_path, "nk")    # Folder to save PNG plots

## Usage

1. Place all UV-Vis CSV files in the input folder
2. Run:

    python uv-vis-csv-multiple-save.py

Plots are saved automatically to the output folder with a timestamp appended to each filename.

## Output

| File | Description |
|---|---|
| `<filename>_<timestamp>_Absorbance.png` | High-resolution plot (300 dpi) saved in the output folder |

## Notes

- Files that do not contain an `XYDATA` marker or have no valid spectral data are skipped automatically.
- The X-axis is inverted as per UV-Vis spectroscopy convention.
- Output folder is created automatically if it does not exist.
- Each plot is saved and closed immediately to conserve memory when processing large batches.
