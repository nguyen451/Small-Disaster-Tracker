import scrape
import clean 
import database

def data_processing():
    # data scraping
    df = scrape_disaster_data()

    # data cleaning
    df = clean_data(df)

    # data storing
    df = save_to_database()


def main():
    # data processing
    data_processing()

    # calling esential functions