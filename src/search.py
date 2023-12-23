from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import requests

link = "https://moseskonto.tu-berlin.de/moses/modultransfersystem/bolognamodule/"
base_url = "https://moseskonto.tu-berlin.de/moses/modultransfersystem/bolognamodule/suchen.html?semester=67&text="


# returns an array of modules [id/version, name, name, lp, verantwortliche, language, zugehörigkeit, '']
def find_modules(module):
    modules = []
    module_url = base_url + module.text
    page = requests.get(module_url)

    soup = BeautifulSoup(page.content, "html.parser")
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
        modules.append(cols)
    return modules


# takes a link to module and returns dictionary with info
def find_specific_module(link):
    info = {"titel": "", "lp": "", "modul/version": "", "verantwortliche": "", "email": "", "lernergebnisse": "", "lehrinhalte": ""}

    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    grading_key = soup.find_all("td", text="95.0")
    if len(grading_key) == 0:
        grading_key = soup.find_all("td", text="86.0")
    if len(grading_key) == 0:
        grading_key = soup.find_all("td", text="40.0")

    if len(grading_key) != 0:
        info["key"] = grading_key[0].text
    else:
        info["key"] = "0"

    titel_tag = soup.find_all("label", text="Titel des Moduls:")[0]
    info["titel"] = titel_tag.next_sibling.next_sibling.next_sibling.contents[0]
    lp_tag = soup.find_all("label", text="Leistungspunkte:")[0]
    info["lp"] = lp_tag.next_sibling.next_sibling.contents[0]
    modul_version_tag = soup.find_all("label", text="Modul / Version:")[0]
    info["modul/version"] = modul_version_tag.next_sibling.next_sibling.next_sibling.split(" ")[0] + "/" +  modul_version_tag.next_sibling.next_sibling.next_sibling.split(" ")[26]
    print(info["modul/version"])
    verantwortliche_tag = soup.find_all("label", text="Modulverantwortliche*r:")[0]
    info["verantwortliche"] = verantwortliche_tag.next_sibling.next_sibling.next_sibling
    email_tag = soup.find_all("label", text="E-Mail-Adresse:")[0]
    info["email"] = email_tag.next_sibling.next_sibling.next_sibling
    lernergebnisse = soup.find_all("h3", text="Lernergebnisse")[0].parent.next_sibling.next_sibling.contents[0].contents[0]
    info["lernergebnisse"] = lernergebnisse
    lehrinhalte = soup.find_all("h3", text="Lehrinhalte")[0].parent.next_sibling.next_sibling.contents[0].contents[0]
    info["lehrinhalte"] = lehrinhalte
    return info


print(find_specific_module("https://moseskonto.tu-berlin.de/moses/modultransfersystem/bolognamodule/beschreibung/anzeigen.html?nummer=40029&version=5&sprache=1"))