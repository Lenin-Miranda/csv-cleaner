# 🧹 CSV/XLSX Data Cleaner

## A lightweight desktop app built with Python, Tkinter, and Pandas to help clean and standardize datasets in .csv or .xlsx format. It supports automatic header cleanup, optional manual editing, and even extracts structured address fields from a single column.

---

# ✅ Features

- 📁 Load .csv or .xlsx files.

- ✨ Automatically clean and standardize headers.

- ✏️ Manually edit headers before saving.

- 🧩 Extract address components (street, city, state, ZIP) from messy full addresses.

- 💾 Save cleaned data as .csv.

## 🧰 Tecnologies

- Python 3
- Tkinter (interfaz gráfica)
- Pandas (manipulación de datos)
- Regex (expresiones regulares para direcciones)

---

# 🛠️ Installation

## Clone the repository:

1. **bash**

- Copy
- Edit
- [git clone](https://github.com/Lenin-Miranda/csv-cleaner.git)
- cd csv-cleaner
- Install required dependencies:

2. **bash**

- Copy
- Edit
- pip install -r requirements.txt

# 📦 Requirements

- pandas
- openpyxl
- tkinter (comes pre-installed with Python)
- re (standard Python library)

# 🚀 How to Run

- bash
- Copy
- Edit
- python main.py

# 🧩 Address Parsing

## If your dataset has a column like MailingAddress with values like:

- 123 Main St, Los Angeles, CA 90001
- It will automatically extract:
- address → 123 Main St
- city → Los Angeles
- state → CA
- zip → 90001
- You can customize the regex logic in address_parser.py.

## 📁 Output

- The cleaned .csv will be saved in the same folder as the original file with the suffix \_limpio.csv.
