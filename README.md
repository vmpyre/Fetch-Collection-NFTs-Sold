# Fetch Sellers NFT Script

This script fetches all 'buyNow' activities for a Magic Eden NFT collection, calculates seller stats, and outputs them to a CSV file.

## Setup

1. **Install Python 3.8+**
2. **Install dependencies:**
   ```bash
   pip install aiohttp
   ```
3. **Configure the collection:**
   - Edit `config.py` and set `COLLECTION_SYMBOL` to your desired collection (default is `steakers`).

## Usage

1. Run the script:
   ```bash
   python fetch_sellers.py
   ```

2. The script will:
   - Fetch all activities in batches.
   - Print progress (e.g., "Page 1 fetched").
   - Fetch the current floor price.
   - Write seller, price, and gain/loss vs. floor to `sell_history.csv`.
   - Print summary stats in the console.

## Output
- `sell_history.csv` will contain:
  - Seller
  - Price
  - Gain or loss vs. current floor price

## Notes
- Each run overwrites `sell_history.csv`.
- You can change the collection by editing `config.py`.
