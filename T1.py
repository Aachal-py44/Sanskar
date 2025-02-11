import webbrowser
from bs4 import BeautifulSoup
import requests
import pandas as pd


def fetch_gdp_data():
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/91.0.4472.124 Safari/537.36"}

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"class": "wikitable"})
    if not table:
        print("Table not found!")
        return

    headers = [header.text.strip() for header in table.find_all("th")]
    rows = []

    for row in table.find_all("tr")[1:]:
        cells = [cell.text.strip().replace("\n", " ") for cell in row.find_all(["td", "th"])]
        if cells:
            rows.append(cells)

    max_cols = max(len(row) for row in rows)
    headers = headers[:max_cols] + [f"Column {i}" for i in range(len(headers), max_cols)]

    df = pd.DataFrame(rows, columns=headers)
    df.to_csv("wiki.csv", index=False, encoding='utf-8-sig')
    print("CSV file saved successfully!")


if __name__ == '__main__':
    fetch_gdp_data()
