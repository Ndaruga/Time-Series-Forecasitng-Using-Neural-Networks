import csv
import os
import requests
from bs4 import BeautifulSoup


URL = "https://www.timeanddate.com/weather/uk/london/historic?month=9&year=2009"


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

# Print the results
print(f"Temperature: {temperature}")
print(f"Humidity: {humidity}")
print(f"Pressure: {pressure}")

# Save the data in a CSV file
filename = "weather_data.csv"
file_exists = os.path.isfile(filename)

with open(filename, "a", newline="") as csvfile:
    headers = ["Temperature", "Humidity", "Pressure"]
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    
    if not file_exists:
        writer.writeheader()
    
    writer.writerow({"Temperature": temperature, "Humidity": humidity, "Pressure": pressure})

print("Data saved to CSV file.")