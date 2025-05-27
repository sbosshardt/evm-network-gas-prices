#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def get_crypto_prices():
    # CoinGecko API endpoint for simple price
    url = "https://api.coingecko.com/api/v3/simple/price"
    
    # Parameters for the API request
    params = {
        "ids": "ethereum,fantom",  # xDAI is pegged to USD, so we don't need to fetch it
        "vs_currencies": "usd,usdc"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Print the results
        print(f"\nCryptocurrency Prices ({timestamp}):")
        print("-" * 40)
        print(f"ETH:  ${data['ethereum']['usd']:.2f} USD")
        print(f"FTM:  ${data['fantom']['usd']:.2f} USD")
        print(f"xDAI: $1.00 USD (pegged)")
        
        # Also show USDC prices for reference
        print("\nUSDC Prices:")
        print("-" * 40)
        print(f"ETH:  {data['ethereum']['usdc']:.2f} USDC")
        print(f"FTM:  {data['fantom']['usdc']:.2f} USDC")
        print(f"xDAI: 1.00 USDC (pegged)")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching prices: {e}")
        return None

if __name__ == "__main__":
    get_crypto_prices() 