from bs4 import BeautifulSoup
import random
import requests
import re
import sqlite3

# Select a random user agent
def select_user():
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',	
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.0; rv:83.0) Gecko/20100101 Firefox/83.0',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/29.0 Mobile/15E148 Safari/605.1.15',
        'Mozilla/5.0 (iPad; CPU OS 11_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/29.0 Mobile/15E148 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    ]
    return random.choice(user_agents)

def insert_into_db(list_of_tuple):
    conn = sqlite3.connect('final_project.db')
    cur = conn.cursor()
    print("Connected to SQLite database")
    cur.executemany("""INSERT INTO zipcode_table
    (zipcode, zipcode_url, lat, long, current_pop, median_income)
    VALUES (?, ?, ?, ?, ?, ?)
    """, list_of_tuple)
    conn.commit()
    conn.close()

def get_income(state, zipcode):
    url = f"https://www.incomebyzipcode.com/{state}/{zipcode}"
    page = requests.get(
        url,
        headers = {'User-Agent': select_user()}
    )
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('div', {'class': 'table-responsive'})
    # Data that I want is stored in a table in the <div> tag where class="table-responsive"
    if table:
        for row in table.find_all('tr'):
            if row.find('th').string == str(zipcode):
                income_row = row.find_next('td', {'class': 'hilite'})
                # Median income data is stored in <td> where class="hilite"
                med_income = income_row.string.replace("$","").replace(",","")
                return int(med_income)
                # Remove dollar sign ($) and commas (,) from income figure and turn it into an integer
            else:
                print(f"Error validating income at {zipcode}")
                return None
    else:
        print(f"Error validating income at {zipcode}")
        return None

def get_zip_data(state, start, end):
    # Input two-digit state code only
    if len(state) > 2:
        print('Enter two-digit state code only')
    state = state.lower()
    zip_list = []
    main_url = "https://www.zip-codes.com"
    append_url = f"/state/{state}.asp"
    # Access URL using one of the randomly chosen user agents
    page = requests.get(
        main_url + append_url,
        headers = {'User-Agent': select_user()}
    )
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', {'class': 'statTable'})
    # Setting which values of the table I want to parse through (I did it in sections because I update to the SQL DB at the end of the code.
    if end == 'end':
        indices = table.find_all('tr')[start:]
    else:
        indices = table.find_all('tr')[start:end]
    for row in indices:
        if row.find('a'):
            table_data = row.find_all('td')
            # Check that ZIP code is not a P.O. Box and continue
            if table_data[-1].string.lower() == "standard":
                zip_id = row.find('a', {'title': re.compile("ZIP Code ")})
                zip_code = int(zip_id.string.split()[-1])
                zip_url = main_url + zip_id.get('href')
                # Go to the URL specific to that ZIP code to check for latitude, longitude, and population data
                zc = requests.get(
                    zip_url,
                    headers = {'User-Agent': select_user()}
                )
                zsoup = BeautifulSoup(zc.content, 'html.parser')
                tables = zsoup.find_all('table', {'class': 'statTable'})
                for table in tables:
                    for data in table.find_all('td'):
                        if data.string == 'Latitude:':
                            latitude = float(data.next_sibling.string)
                        if data.string == 'Longitude:':
                            longitude = float(data.next_sibling.string)
                        if data.string == 'Current Population:':
                            population = int(data.next_sibling.string.replace(",",""))
                # If the ZIP code has a nonzero population, find the median income at that zip code
                if population > 0:
                    income = get_income('california', str(zip_code))
                else:
                    income = None
                try:
                    zip_list.append((zip_code, zip_url, latitude, longitude, population, income))
                    print(f"Successfully appended data for {zip_code}")
                except:
                    print(f"Issue appending data for {zip_code}")
    insert_into_db(zip_list)               


def main(calls=None):
    if calls == None:
        get_zip_data('CA',1,500)
        get_zip_data('CA',500,1000)
        get_zip_data('CA',1000,1500)
        get_zip_data('CA',1500,2000)
        get_zip_data('CA',2000,'end')
    else:
        calls += 1
        get_zip_data('CA', 1, calls)