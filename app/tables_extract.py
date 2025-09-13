# src/tables_extract.py
import pandas as pd
from pathlib import Path


def extract_tables(path):
    path = Path(path)
    # pandas will use lxml or html5lib behind the scenes
    tables = pd.read_html(str(path), flavor=["lxml", "bs4"])
    return tables


# quick example:
if __name__ == "__main__":
    tables = extract_tables("data/GOOGLE-2023.htm")
    print(f"Found {len(tables)} tables")
    print(tables[50])
