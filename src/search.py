from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import requests

link = "https://moseskonto.tu-berlin.de/moses/modultransfersystem/bolognamodule/"
base_url = "https://moseskonto.tu-berlin.de/moses/modultransfersystem/bolognamodule/suchen.html?semester=67&text="

# returns an array of modules‘ names
def find_modules(module):
    modules = []
    module_url = base_url + module
    page = requests.get(module_url)

    soup = BeautifulSoup(page.content, "html.parser")
    #results = soup.find(id="j_idt114:ergebnisliste")
    table = soup.find('table', attrs={'class': 'table'})
    table_body = table.find('tbody')

    data = []
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        print(cols)
        print("\n")
        data.append([ele for ele in cols if ele])  # Get rid of empty values
        modules.append(cols[2])
    return modules