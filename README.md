# DSCI510 Final Project
## Project Goals:
In this project, I want to be able to see if there is a relationship between the median income in a neighborhood (quantified by zip code) and the amount of electric vehicle charging locations and vegan/ vegetarian restaurants. Hopefully I will be able to see a distinct pattern in this data, and it would be ideal if I could extend this project to different parts of the country to see how this trend holds up in, for example, the Midwest. It would also be very interesting to see how the introduction of electric vehicle charging stations and vegan/vegetarian restaurants affects a community, and if I could possibly quantify gentrification of a neighborhood using these things as metrics. Personally, I grew up in Orange County, CA, I drive a hybrid, and I’m a vegan, so I know these things are all correlated but would love to be able to explore the actual data on this topic.

## Data Sources:
1. Open Charge Map API
  - API: `https://api.openchargemap.io/v3/`
  - Documentation: https://openchargemap.org/site/develop/api 
  - This is a global public registry of electric vehicle charging locations. You can make an API call using location information and the API will return charging location information in JSON format.

2. California Zip Codes (Website)
  - URL: https://www.zip-codes.com
  - This website lists all of the zipcodes in California and relevant information about the zipcodes. You can scrape the list of zipcodes from the site and get the href for each zip code, which links to more information about the zip code.

3. Median Household Income (Website)
  - URL: https://www.incomebyzipcode.com/ 
  - This website has information on median income by zip code for the US. You can search the URL as `https://www.incomebyzipcode.com/{state}/{zipcode}` and will get a webpage with different income statistics that you can then scrape for median income and store in a database.

4. Yelp Fusion API
  - API: `https://api.yelp.com/v3`
  - Documentation: https://www.yelp.com/developers/documentation/v3/get_started
  - This API allows you to query Yelp's database for businesses, and in the case of this project, vegan and vegetarian restaurants. You can make an API call using location and keyword parameters and the API will return restaurant information in JSON format.

## To-Do:
- [ ] Create data model
  - [X] Create SQLite database with appropriate tables.
  - [ ] Set up main script to take `source=remote` or `source=local` and read in the scrapers/ API crawlers or open database.
- [X] Get data
  - [X] Scrape List of ZIP codes in California and their relevant information and update the database.
  - [X] Scrape median household income for each zipcode and update the database.
  - [X] Scrape the electric vehicle charging locations and update the database.
  - [X] Scrape the Yelp API and update the database. 
- [ ] Analyze the data.
