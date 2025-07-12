import aiohttp
import asyncio
import csv
from config import COLLECTION_SYMBOL

async def fetch_all_magiceden_activities():
    url_base = f"https://api-mainnet.magiceden.dev/v2/collections/{COLLECTION_SYMBOL}/activities"
    headers = {"accept": "application/json"}
    offset = 0
    limit = 500
    all_data = []
    page = 1
    while True:
        url = f"{url_base}?offset={offset}&limit={limit}"
        print(f"Fetching data from page {page}..")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                if not data:
                    break
                all_data.extend(data)
                await asyncio.sleep(1)
        offset += limit
        page += 1
    return all_data

async def fetch_floor_price():
    print("Fetching current floor price...")
    url = f"https://api-mainnet.magiceden.dev/v2/collections/{COLLECTION_SYMBOL}/stats"
    headers = {"accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            stats = await response.json()
            floor_price = stats.get("floorPrice", 0) / 1e9  # Convert lamports to SOL
            return floor_price

async def fetch_sellers_and_stats():
    all_data = await fetch_all_magiceden_activities()
    floor_price = await fetch_floor_price()
    buy_now_items = [item for item in all_data if item.get('type') == 'buyNow']
    prices = [item.get('price', 0) for item in buy_now_items if isinstance(item.get('price', 0), (int, float))]
    total_items = len(buy_now_items)
    lowest_price = min(prices) if prices else None
    highest_price = max(prices) if prices else None
    total_sol = sum(prices)

    with open("sell_history.csv", mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Seller', 'Selling Price (SOL)', 'Gain/Loss vs Floor (SOL)'])
        for item in buy_now_items:
            seller = item.get('seller', '')
            price = item.get('price', '')
            gain_or_loss = round(price - floor_price, 6) if isinstance(price, (int, float)) else ''
            writer.writerow([seller, price, gain_or_loss])

    print(f"Total items: {total_items}")
    print(f"Lowest price: {lowest_price}")
    print(f"Highest price: {highest_price}")
    print(f"Total SOL: {total_sol}")
    print(f"Current floor price: {floor_price}")

if __name__ == "__main__":
    asyncio.run(fetch_sellers_and_stats())