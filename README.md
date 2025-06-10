# CSV Cleaner 🧹📊

A desktop application built with **Python** and **Tkinter** to clean, reformat, and organize messy CSV and Excel (`.xlsx`) files. Ideal for data processors working with repetitive file structures, such as mailing lists or print logistics.

## 🔍 Overview

The app simplifies the process of transforming unstructured data into clean, organized CSVs. Users can view header changes, fix formatting, parse incomplete address fields, and maintain a history of recently cleaned files.

---

## ✨ Features

- **Supports `.csv` and `.xlsx` files**
- **Always uses comma `,` as delimiter** for output consistency
- **Header Cleaner**: Standardizes and sanitizes headers
- **Header Editor**: Manually rename headers with UI assistance
- **Address Parser**: Separates full addresses into `Street`, `City`, `State`, and `ZIP`, even when poorly formatted
- **Recent History**: View the latest files and transformations
- **Custom Drop Column**: Automatically adds a `DROP` column if needed
- **MOJO Job Splitter** (optional): Sorts and splits files by ZIP and CRRT (Carrier Route) with intelligent cut points

---

## 🛠 Tech Stack

- **Python 3**
- **Tkinter** for GUI
- **pandas** for data manipulation
- **openpyxl** for Excel file support
- **regex** for address parsing

---

## 🚀 Getting Started

1. **Clone the repo:**

**bash**

git clone https://github.com/Lenin-Miranda/csv-cleaner
cd csv-cleaner

2. **install dependencies**
   pip install pandas openpyxl

3. **run the app**

python app.py
