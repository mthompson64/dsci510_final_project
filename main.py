import argparse
import sqlite3
import create_data_tables
import zip_codes_scraper
import charge_locations_api
import yelp_api


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="This is parser for the main code for my project")
    parser.add_argument("--source",
                        choices=["remote", "local"],
                        required=True,
                        type=str,
                        help="Choose to retrieve the data locally (stored on disk) or remotely (run scrapers/ API crawlers on your device).")
    parser.add_argument("--grade",
                        default=3,
                        required=False,
                        type=int,
                        help="Choose how many web scraper/ API calls to make. Takes an integer input.")
    
    args = parser.parse_args()
    source = args.source
    if args.grade is not None:
        calls = args.grade


    if source == "remote":
        create_data_tables.main()
        if calls is not None:
            zip_codes_scraper.main(calls)
            charge_locations_api.main(calls)
            yelp_api.main(calls)
            print(f"Successfully made {calls} calls to the data and stored it in final_project.db")
        else:
            zip_codes_scraper.main()
            charge_locations_api.main()
            yelp_api.main()    
            print("Successfully collected the data and stored it in final_project.db")
    elif source == "local":
        conn = sqlite3.connect('final_project.db')
        print("Connected to SQLite database")
        conn.close()


if __name__ == "__main__":
    main()