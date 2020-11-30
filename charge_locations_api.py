import urllib.request, urllib.parse, urllib.error
import json
import random
import requests
import sqlite3

# Choose a random user agent
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

# Get electric vehicle charging information by ZIP code, latitude, and longitude
def get_locations(ZIP, lat, long):
    params = dict()
    params['output'] = 'json'
    params['countrycode'] = 'US'
    params['maxresults'] = '20'
    params['latitude'] = lat
    params['longitude'] = long
    params['key'] = '3ebc9c55-6ee7-411d-b2ac-daec0d4551e2'
    serviceurl = 'https://api.openchargemap.io/v3/poi/?'
    url = serviceurl + urllib.parse.urlencode(params)
    response = requests.get(
        url,
        headers = {'User-Agent': select_user()}
    )
    # Data that I want is stored in the ['AddressInfo'] key of the JSON
    location = []
    if len(response.json()) > 0:
        for item in response.json():
            # Identify each of the items I want to keep and append to my database
            ID = item['AddressInfo']['ID']
            Title = item['AddressInfo']['Title']
            AddressLine1 = item['AddressInfo']['AddressLine1']
            AddressLine2 = item['AddressInfo']['AddressLine2']
            # Include the second address line if it has it
            Address = "{Line1}{Line2}".format(Line1=AddressLine1, Line2=" "+ AddressLine2 if AddressLine2 is not None else "")
            Town = item['AddressInfo']['Town']
            # I was having some problems where a 'Postcode' value wasn't numeric, so I just want the program to skip over that
            try:
                ZIPCode = int(item['AddressInfo']['Postcode'])
            except:
                continue
            # Only include charging locations unique to the ZIP code you are querying
            if ZIPCode == ZIP:
                location.append([ID, ZIPCode, Title, Address, Town])
            else:
                continue
        insert_into_db(location)
        print(f"Successfully inserted records for {ZIP}")

def insert_into_db(list_of_lists):
    conn = sqlite3.connect('final_project.db')
    cur = conn.cursor()
    for item in list_of_lists:
        # 1st element of item is ZIP code. Convert ZIP code to zip_id from zipcode_table
        cur.execute(f'SELECT zip_id FROM zipcode_table WHERE zipcode = {item[1]}')
        zip_id = cur.fetchone()[0]
        item[1] = zip_id
    list_of_tuples = [tuple(x) for x in list_of_lists]
    try:
        cur.executemany("""INSERT INTO charging_locations_table
        (charger_id, zip_id, name, address, city)
        VALUES (?, ?, ?, ?, ?)
        """, list_of_tuples)
        conn.commit()
        conn.close()
    except:
        conn.close()


def main(calls=None):
    conn = sqlite3.connect('final_project.db')
    cur = conn.cursor()
    print("Connected to SQLite database")
    
    if calls == None:
        cur.execute('SELECT zipcode, lat, long FROM zipcode_table')
    else:
        cur.execute(f'SELECT zipcode, lat, long FROM zipcode_table LIMIT {calls}')

    try:
        zips = cur.fetchall()
    except:
        print("Issue fetching charging location data")

    for item in zips:
        # The data is in a tuple and I don't know how else to extract the items from the tuple
        get_locations(item[0], item[1], item[2])
    print("All done!")