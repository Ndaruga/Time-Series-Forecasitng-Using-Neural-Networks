import csv
import os
import requests
from bs4 import BeautifulSoup
from datetime import date

# Save the data in a CSV file
filename = os.path.join("Data","weather_data.csv")
file_exists = os.path.isfile(filename)

today = date.today()
current_year = today.year
current_month = today.month

with open(filename, "a", newline="") as csvfile:
    headers = ["Month", "Year","Temperature", "Humidity", "Pressure"]
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    
    if not file_exists:
        writer.writeheader()
    for year in range(2009, current_year+1):
        try:
            for month in range(1, 13):
                # check for current year and month
                if ((year == current_year) & (month == current_month)):
                    break
                else:
                    URL = f"https://www.timeanddate.com/weather/uk/london/historic?month={month}&year={year}"

                    # Make a request to the URL
                    response = requests.get(URL)

                    # Parse the HTML content using Beautiful Soup
                    soup = BeautifulSoup(response.content, "html.parser")

                    # Find the table row with class="sep-t"
                    sep_t = soup.find("tr", class_="sep-t")

                    # Find the temperature and humidity values
                    temperature = sep_t.find("td").get_text()
                    humidity = sep_t.find_all("td")[1].get_text()

                    # Find the pressure value
                    pressure = sep_t.find_all("td")[2].get_text()

                    writer.writerow({"Month":month, "Year": year, "Temperature": temperature, "Humidity": humidity, "Pressure": pressure})

        except:
            print(f"No data found for {month}, {year}")

print("Data saved to CSV file.")