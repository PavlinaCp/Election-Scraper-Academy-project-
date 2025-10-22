"""
projekt_3.py: druhý projekt do Engeto Online Python Akademie
author: Pavlína Čepcová
email: cepcovap@gmail.com
"""
import requests
import bs4
import argparse
import csv
import sys

def get_user_input() -> list[str]:
    parser = argparse.ArgumentParser(
        description="script for scraping election data"
        )
    parser.add_argument(
        "territorial_unit", help="Name of territorial unit (e.g. Benešov)"
        )
    parser.add_argument(
        "file_name", help="Name of the output folder with CSV data"
        )
    args = parser.parse_args()
    territorial_unit = args.territorial_unit
    file_name = args.file_name
    if not args.territorial_unit or not args.file_name:
        print(
            "Error: You must provide both arguments " \
            "- the name of the territorial unit and the name of the CSV file."
            )
        print("Correct usage: python projekt_2.py 'Benesov' 'output.csv")
        sys.exit()
    if not file_name.lower().endswith(".csv"):
        print(
            "Error: The second argument must be the name of " \
            "a CSV file (e.g. 'results.csv')."
            )
        print("Correct usage: python projekt_2.py 'Benesov' 'results.csv'")
        sys.exit()
    if territorial_unit.lower().endswith(".csv"):
        print(
            "Error: The first argument cannot be a file name. " \
            "You entered the arguments in the wrong order."
            )
        print("Correct usage: python projekt_2.py 'Benesov' 'results.csv'")
        sys.exit()

    return [territorial_unit, file_name]

def link_to_unit_page(choosed_unit: str) -> str:
    url = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    answer_serv = requests.get(url)
    if answer_serv.status_code != 200:
        raise ConnectionError(f"Page loading Error {answer_serv.status_code}")
    soup = bs4.BeautifulSoup(answer_serv.text, "lxml")
    tables = soup.find_all("table", {"class": "table"})
    for table in tables:
        for row in table.find_all("tr"):
            name_unit = row.find("td", string=choosed_unit)
            if name_unit:
                link = row.find("td", {"class":"center"})
                if link:
                    link_tag = link.find("a")["href"]
                full_link = f"https://www.volby.cz/pls/ps2017nss/{link_tag}"
                return full_link

def data_scraping_code_name(link_unit_part: str):
    res = requests.get(link_unit_part)
    if res.status_code != 200:
        raise ConnectionError(f"Page loading Error {res.status_code}")
    soup = bs4.BeautifulSoup(res.text, "lxml")
    codes_names = []
    for row in soup.select("table.table tr"):
        num_cell = row.find("td", {"class": "cislo"})
        names_cell = row.find("td", {"class": "text"})
        if num_cell and names_cell:
            a_tag = num_cell.find("a")
            if a_tag:
                num = a_tag.text.strip()
                name = names_cell.text.strip()
                code_name = {
                    "code": num,
                    "location": name
                             }
                codes_names.append(code_name)
    return codes_names

def municipality_info_link(link_unit_part: str):
    all_links_unit_parts =[]
    answer_serv = requests.get(link_unit_part)
    if answer_serv.status_code != 200:
        raise ConnectionError(f"Page loading Error {answer_serv.status_code}")
    soup = bs4.BeautifulSoup(answer_serv.text, "lxml")
    tables = soup.find_all("table", {"class": "table"})
    for table in tables:
        for row in table.find_all("tr"):
            a_tag = row.find("a")
            if a_tag and "href" in a_tag.attrs:
                link_tag = a_tag["href"]
                full_link = (f"https://www.volby.cz/pls/ps2017nss/{link_tag}")
                all_links_unit_parts.append(full_link)
    return all_links_unit_parts

def scraping_detail_data(municipality_links: list[dict]):
    municipality_data = []
    for municipality_link in municipality_links:
        parties = {}
        answer_serv = requests.get(municipality_link)
        if answer_serv.status_code != 200:
            raise ConnectionError(f"Page loading Error {answer_serv.status_code}")
        soup = bs4.BeautifulSoup(answer_serv.text, "lxml")

        reg_table = soup.find("table", {"id": "ps311_t1"})
        registered = (
            reg_table.find("td", {"headers": "sa2"})
            .get_text(strip=True)
            .replace("\xa0", "")
            .replace(" ", "")
        )
        envelopes = (
            reg_table.find("td", {"headers": "sa3"})
            .get_text(strip=True)
            .replace("\xa0", "")
            .replace(" ", "")
        )
        valid = (
            reg_table.find("td", {"headers": "sa6"})
            .get_text(strip=True)
            .replace("\xa0", "")
            .replace(" ", "")
        )
        municipality = {
            "registered": registered,
            "envelopes": envelopes,
            "valid": valid
        }
        for table in soup.find_all("table",{"class":"table"}):
            for td in table.find_all("tr"):
                name_cel = td.find("td", {"class":"overflow_name"})
                vote_cel = td.find("td",{"headers":"t1sa2 t1sb3"})
                if name_cel and vote_cel:
                    name = name_cel.text
                    vote = (
                        vote_cel.get_text(strip=True)
                        .replace("\xa0", "")
                        .replace(" ", "")
                    )
                    parties[name] = vote
        municipality.update(parties)
        municipality_data.append(municipality)         
    return municipality_data


def convert_to_csv(file_name: str, data: list[dict]):
    with open(file_name, "w",newline="", encoding="utf-8-sig") as p:
        writer = csv.DictWriter(p ,fieldnames = data[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(data)


def main():
    territorial_unit, file_name = get_user_input()
    url_unit = link_to_unit_page(territorial_unit)
    url_municipality = municipality_info_link(url_unit)
    main_data = data_scraping_code_name(url_unit)
    detail_data = scraping_detail_data(url_municipality)
    all_data = [
        {**m, **d} for m, d in zip(main_data, detail_data)
    ]
    convert_to_csv(file_name, all_data)

if __name__ == "__main__":
    main()
