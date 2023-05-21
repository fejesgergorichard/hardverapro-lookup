import requests
import telegram
import asyncio
import csv
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from string_extensions import transform_to_search_text
from AdInfo import AdInfo, ad_info_factory

SEARCH_TEXT = 'mario odyssey'

# Set up Telegram bot
load_dotenv()
bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

# Construct the path to the .csv file
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "ad_database.csv")

# Check if the file exists and create it with headers
if not os.path.exists(csv_path):
    with open(csv_path, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['id', 'title', 'seller'])

# URL of the search page
url = f'https://hardverapro.hu/aprok/keres.php?stext={transform_to_search_text(SEARCH_TEXT)}&stcid_text=&stcid=&stmid_text=&stmid=&minprice=&maxprice=&cmpid_text=&cmpid=&usrid_text=&usrid=&__buying=0&__buying=1&stext_none='


def save_to_csv(ad: AdInfo):
    with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([ad.id, ad.title, ad.seller])


def ad_exists_in_database(ad: AdInfo):
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row and row[0] == ad.id and row[1] == ad.title and row[2] == ad.seller:
                return True
    return False


async def send_message(ad: AdInfo):
    bot = telegram.Bot(token=bot_token)
    message = f"New ad!\n{ad.title}\nPrice: {ad.price}\nSeller: {ad.seller}\n{ad.url}"
    await bot.send_message(chat_id=chat_id, text=message)


async def process_ad(ad):
    ad_info = ad_info_factory(ad)
    if not ad_exists_in_database(ad_info):
        await send_message(ad_info)
        save_to_csv(ad_info)


async def main():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    ad_listings = soup.find_all('li', class_='media')
    for ad in ad_listings:
        await process_ad(ad)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
