import csv
import requests
from bs4 import BeautifulSoup as bs

career_years = ["1992", "1993", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011"]

base_page = "https://www.baseball-reference.com/players/gl.fcgi?id=wakefti01&t=p&year="
table_id = "#pitching_gamelogs"

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
