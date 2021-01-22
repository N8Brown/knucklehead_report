import csv
import requests
from bs4 import BeautifulSoup as bs


# Need to write a script to scrape the main page for the player to get table data for years active
# instead of hard coding it in.
career_years = ["1992", "1993", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011"]

base_page = "https://www.baseball-reference.com/players/gl.fcgi?id=wakefti01&t=p&year="
table_id = "#pitching_gamelogs"

# See if you can come up with a loop that will pull the column headers from just the first table
# then loop through all tables and add them to a single .csv file. 

# The table header is contained in <thead> while the stats and desired data are found in <tbody>
# Any table row within <tbody> that has a class of "thead" can be excluded. The <tfoot> should 
# also be excluded from the data being sent to the .csv file.

for year in career_years:
    response = requests.get(base_page + year)
    soup = bs(response.text, "html.parser")
    table = soup.select(table_id)
    rows = table[0].findAll("tr")
    output = "twake"+year+".csv"

    with open(output, "wt+", newline="") as file:
        writer = csv.writer(file)
        for row in rows:
            csv_row = []
            for cell in row.findAll(["td", "th"]):
                csv_row.append(cell.get_text())
            writer.writerow(csv_row)
