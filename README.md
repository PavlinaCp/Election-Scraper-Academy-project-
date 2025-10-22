# Czech Election Data Scraper

A Python script for scraping Czech election results from [volby.cz](https://www.volby.cz/).  
The script downloads data for a specified territorial unit and saves it as a CSV file.

---

requirements.txt should contain:
requests
beautifulsoup4
lxml

Usage:
Run the script from the command line with the territorial unit name and output CSV file
python projekt_2.py "Praha" "praha_results.csv"

Example Output:
The CSV file will have a structure like this:

code;location;registered;envelopes;valid;Party A;Party B;Party C
101;Benešov;5000;4800;4700;1200;900;600
102;Another Town;3200;3100;3000;800;700;400

code – municipality code
location – municipality name
registered – number of registered voters
envelopes – number of envelopes cast
valid – number of valid votes
Party A/B/C – votes for each party

## Installation

1. Clone this repository:

```bash
git clone https://github.com/PavlinaCp/election-scraper.git
cd election-scraper

Install the required libraries:
pip install -r requirements.txt
