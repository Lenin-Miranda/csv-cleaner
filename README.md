# CSV Cleaner

A Python/Tkinter desktop tool for cleaning CSV and Excel files used in mailing-list workflows. It normalizes column headers, separates address fields, exports CSV files and records recently processed paths.

## Features

- Load `.csv` and `.xlsx` files with pandas.
- Normalize headers and inspect the before/after names.
- Edit column names through a desktop dialog.
- Parse an address column into address, city, state and ZIP fields.
- Run the integrated MOJO processing workflow and maintain recent-file history.

## Install and run

Requires Python 3 with Tkinter and a graphical desktop.

```bash
git clone https://github.com/Lenin-Miranda/csv-cleaner.git
cd csv-cleaner
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pandas openpyxl
python main.py
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.
Check Tkinter with `python -m tkinter`; if unavailable, install the Tk support provided by your Python distribution.

## Workflow and output

1. Select a CSV or Excel file.
2. Review the cleaned headers and any address-column selection.
3. Inspect the generated file beside the input: `original_name_limpio.csv`.
4. Use the header editor to adjust names and save again.

The export uses comma-separated CSV without the pandas row index. Reprocessing the same input replaces its existing `_limpio.csv` output. Keep source files and inspect output before using it downstream.

## Code map

| File | Purpose |
| --- | --- |
| [main.py](main.py) | Desktop interface, loading, normalization and export |
| [address_parser.py](address_parser.py) | Address parsing |
| [mojo.py](mojo.py) and [mojo_util.py](mojo_util.py) | Mailing-job processing helpers |
| [historial.py](historial.py) | Recent-file history |

## Current limitations

Address parsing assumes mailing-address patterns and may need manual correction. The history window opens files with `os.startfile`, which is Windows-specific; that action is not portable to macOS/Linux. There is no automated test suite or dependency lockfile. Validate changes using small, non-sensitive sample files.
