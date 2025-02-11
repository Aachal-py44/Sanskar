from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def initialize_driver(driver_path):
    service = Service(driver_path)
    driver = webdriver.Edge(service=service)
    return driver


def wait_for_element(driver, xpath, timeout=10):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))


def get_table_headers(driver, xpath):
    return driver.find_elements(By.XPATH, xpath)


def is_column_sorted(driver, table_xpath, column_index, order="ascending"):
    rows = driver.find_elements(By.XPATH, f"{table_xpath}/tbody/tr")
    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) > column_index:
            cell_text = cells[column_index].text.strip().replace(",", "")
            try:
                data.append(int(cell_text))
            except ValueError:
                data.append(cell_text)

    try:
        if order == "ascending":
            return data == sorted(data, key=lambda x: (isinstance(x, str), x))
        elif order == "descending":
            return data == sorted(data, key=lambda x: (isinstance(x, str), x), reverse=True)
    except TypeError:
        return False

    return False


def sort_table_columns(driver, headers, table_xpath):
    for index, header in enumerate(headers):
        if header.get_attribute("role") == "columnheader button":
            print(f"Sorting column {index + 1} in ascending order...")
            header.click()
            if is_column_sorted(driver, table_xpath, index, order="ascending"):
                print(f"Column {index + 1} is sorted in ascending order.")
            else:
                print(f"Column {index + 1} is NOT sorted in ascending order.")
            print(f"Sorting column {index + 1} in descending order...")
            header.click()
            if is_column_sorted(driver, table_xpath, index, order="descending"):
                print(f"Column {index + 1} is sorted in descending order.")
            else:
                print(f"Column {index + 1} is NOT sorted in descending order.")


def main():
    driver_path = r"C:\users\91992\Downloads\edgedriver_win32\msedgedriver.exe"
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
    table_xpath = "//*[@id='mw-content-text']/div[1]/table[2]"
    header_xpath = ".//*[@id='mw-content-text']/div[1]/table[2]/thead//th"

    driver = initialize_driver(driver_path)
    driver.get(url)
    wait_for_element(driver, table_xpath)
    headers = get_table_headers(driver, header_xpath)
    sort_table_columns(driver, headers, table_xpath)
    driver.quit()


if __name__ == "__main__":
    main()
