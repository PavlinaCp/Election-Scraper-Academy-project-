# Czech Election Data Scraper

A Python script for scraping Czech election results from [volby.cz](https://www.volby.cz/).  
The script downloads data for a specified territorial unit and saves it as a CSV file.

Installation:
Clone this repository:
```bash
git clone https://github.com/your_username/election-scraper.git
cd election-scraper

Install the required libraries:
pip install -r requirements.txt

requirements.txt should contain:
requests
beautifulsoup4
lxml

Usage:
Run the script from the command line with the territorial unit name and output CSV file

Example:
python projekt_3.py "Praha" "praha_results.csv"
A sample output is attached
