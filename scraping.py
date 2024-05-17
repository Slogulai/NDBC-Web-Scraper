from bs4 import BeautifulSoup
import requests 
import xlsxwriter

# 1. Retrieve HTML and create BeautifulSoup object
response = requests.get("https://www.ndbc.noaa.gov/station_page.php?station=46267")
soup = BeautifulSoup(response.text, "html.parser")
# 2. Find the table and extract headers and rows:
section = soup.find('section', {"id": "wavedata"})
table = section.find('table', {"id": "currentobs"})
header = []
rows = []
for i, row in enumerate(table.find_all('tr')):
    if i == 0:
        header = [el.text.strip() for el in row.find_all('th')]
    else:
        row_data = [el.text.strip() for el in row.find_all('td')]
        # Split the text at the first occurrence of ':' and take the second part
        row_data = [text.split(':', 1)[-1].strip() if ':' in text else text for text in row_data]
        rows.append(row_data)
# 3. save to it a XLSX file:
workbook = xlsxwriter.Workbook('wavedata.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write_row(0, 0, header)
for i, row in enumerate(rows):
    worksheet.write_row(i+1, 0, row)
workbook.close()
