import csv
import requests
from bs4 import BeautifulSoup as bs

# This script will combine scraped data for each year listed in the 
# career_years variable into a single output .csv file. This will also
# clean up the output to only include a single header row of column names
# instead of one for each year. It will also remove sub-header rows that
# the data tables contain to group the data into specific months of each
# year. This script will also omit the cumulative data for each column
# that is found in the table footer tag.

career_years = ["1992", "1993", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011"]

base_page = "https://www.baseball-reference.com/players/gl.fcgi?id=wakefti01&t=p&year="
table_id = "#pitching_gamelogs"


with open("pitch_data/wakefti_games.csv", "wt+", newline="") as file:
    writer = csv.writer(file)

    for year in career_years:
        response = requests.get(base_page + year)
        soup = bs(response.text, "html.parser")
        table = soup.select(table_id)
        header = table[0].findAll("thead")
        header_rows = header[0].findAll("tr")
        body = table[0].findAll("tbody")
        body_rows = body[0].findAll("tr")

        # Only gets the table header row with the column names
        # if it is the first iteration through the list of years

        if year == career_years[0]:
            for row in header_rows:
                csv_row = [cell.get_text() for cell in row.findAll(["td", "th"])]

                # Above is the list comprehension version of the following
                # for loop:
                #
                # csv_row = []
                # for cell in row.findAll(["td", "th"]):
                #     csv_row.append(cell.get_text())

                writer.writerow(csv_row)

        for row in body_rows:

            # Checks if the row contains a class of "thead"
            # and is so, it skips that row and doesn't add it
            # to the .csv file

            if "class" in row.attrs:
                if "thead" in row.attrs["class"]:
                    continue
            csv_row = [cell.get_text() for cell in row.findAll(["td", "th"])]

            # Above is the list comprehension version of the following
            # for loop:
            #
            # csv_row = []
            # for cell in row.findAll(["td", "th"]):
            #     csv_row.append(cell.get_text())
            
            writer.writerow(csv_row)
