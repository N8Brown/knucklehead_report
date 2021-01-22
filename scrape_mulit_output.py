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
    header = table[0].findAll("thead")
    header_rows = header[0].findAll("tr")
    body = table[0].findAll("tbody")
    body_rows = body[0].findAll("tr")

    with open("pitch_data/wakefti"+year+".csv", "wt+", newline="") as file:
        writer = csv.writer(file)
        if year == career_years[0]:
            for row in header_rows:
                csv_row = [cell.get_text() for cell in row.findAll(["td", "th"])]

                writer.writerow(csv_row)

        for row in body_rows:
            if "class" in row.attrs:
                if "thead" in row.attrs["class"]:
                    continue
            csv_row = [cell.get_text() for cell in row.findAll(["td", "th"])]
            writer.writerow(csv_row)
