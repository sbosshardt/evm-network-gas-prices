from web3 import Web3
import requests
from datetime import datetime
import time
import random
import asyncio
import aiohttp
from typing import Dict, Union
from decimal import Decimal, ROUND_DOWN

# Define RPC endpoints with fallbacks
RPC_ENDPOINTS = {
    "Ethereum Mainnet": [
        "https://eth.merkle.io",
        "https://eth-mainnet.public.blastapi.io",
        "https://ethereum.publicnode.com"
    ],
    "Arbitrum One": [
        "https://arb1.arbitrum.io/rpc",
        "https://arbitrum-one.public.blastapi.io",
        "https://arbitrum.llamarpc.com"
    ],
    "Gnosis": [
        "https://rpc.gnosis.gateway.fm",
        "https://gnosis.public.blastapi.io",
        "https://gnosis.llamarpc.com"
    ],
    "Polygon": [
        "https://polygon-rpc.com",
        "https://polygon.public.blastapi.io",
        "https://polygon.llamarpc.com"
    ],
    "Fantom": [
        "https://fantom-pokt.nodies.app",
        "https://fantom.public.blastapi.io",
        "https://fantom.llamarpc.com"
    ]
}

# Track last used endpoint for each network
last_used_endpoints = {network: None for network in RPC_ENDPOINTS.keys()}

DEFAULT_GAS_UNITS = 1_000_000  # 1 million gas units

def wei_to_eth(wei: int) -> float:
    """Convert wei to ETH."""
    return wei / 10**18

def get_current_timestamps() -> Dict[str, Union[int, str]]:
    """Get current Unix timestamp and formatted datetime with timezone."""
    now = datetime.now().astimezone()  # Makes it timezone-aware using the local time zone
    return {
        "timestamp": int(time.time()),
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S %Z")
    }

def get_random_endpoint(network: str) -> str:
    """Get a random endpoint for a network, avoiding the last used one if possible."""
    endpoints = RPC_ENDPOINTS[network]
    if len(endpoints) == 1:
        return endpoints[0]
    
    available_endpoints = [ep for ep in endpoints if ep != last_used_endpoints[network]]
    if not available_endpoints:
        available_endpoints = endpoints
    
    endpoint = random.choice(available_endpoints)
    last_used_endpoints[network] = endpoint
    return endpoint

async def fetch_network_data(network: str, gas_units: int, timestamps: Dict[str, Union[int, str]]) -> Dict:
    """Fetch data for a single network, retrying with different endpoints if one fails."""
    endpoints = RPC_ENDPOINTS[network]
    errors = []
    
    # Try each endpoint until one succeeds
    for endpoint in endpoints:
        try:
            w3 = Web3(Web3.HTTPProvider(endpoint))
            gas_price = w3.eth.gas_price
            block_number = w3.eth.block_number
            total_cost_wei = gas_price * gas_units
            native_token_cost = wei_to_eth(total_cost_wei)
            
            # Update last used endpoint only on success
            last_used_endpoints[network] = endpoint
            
            return {
                "gas_price_gwei": float(Web3.from_wei(gas_price, 'gwei')),
                "total_cost_wei": total_cost_wei,
                "native_token_cost": native_token_cost,
                "gas_units": gas_units,
                "block_number": block_number,
                "timestamp": timestamps["timestamp"],
                "datetime": timestamps["datetime"],
                "rpc_url": endpoint
            }
        except Exception as e:
            errors.append(f"{endpoint}: {str(e)}")
            continue
    
    # If all endpoints failed, return error with details
    return {"error": f"All endpoints failed: {'; '.join(errors)}"}

async def get_gas_prices_async(gas_units: float = 1.0) -> Dict[str, Dict[str, Union[float, int, str]]]:
    """Get gas prices for all networks asynchronously."""
    actual_gas_units = int(gas_units * DEFAULT_GAS_UNITS)
    timestamps = get_current_timestamps()
    
    # Create tasks for all networks
    tasks = [
        fetch_network_data(network, actual_gas_units, timestamps)
        for network in RPC_ENDPOINTS.keys()
    ]
    
    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)
    
    # Combine results with network names
    return dict(zip(RPC_ENDPOINTS.keys(), results))

def get_gas_prices(gas_units: float = 1.0) -> Dict[str, Dict[str, Union[float, int, str]]]:
    """Get gas prices for all networks."""
    return asyncio.run(get_gas_prices_async(gas_units))

async def get_crypto_prices_async() -> Dict[str, Dict[str, Union[float, int, str]]]:
    """Get cryptocurrency prices from CoinGecko asynchronously."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "ethereum,fantom,matic-network,xdai",
        "vs_currencies": "usd"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()

                # Add timestamps
                timestamps = get_current_timestamps()
                data['timestamp'] = timestamps["timestamp"]
                data['datetime'] = timestamps["datetime"]
                
                return data
    except Exception as e:
        return {"error": str(e)}

def get_crypto_prices() -> Dict[str, Dict[str, Union[float, int, str]]]:
    """Get cryptocurrency prices."""
    return asyncio.run(get_crypto_prices_async())

async def calculate_gas_costs_usd_async(gas_units: float = 1.0) -> Dict[str, Dict[str, Union[float, int, str]]]:
    """Calculate gas costs in USD for all networks asynchronously."""
    # Fetch gas prices and crypto prices concurrently
    gas_prices_task = get_gas_prices_async(gas_units)
    crypto_prices_task = get_crypto_prices_async()
    
    gas_prices, crypto_prices = await asyncio.gather(gas_prices_task, crypto_prices_task)
    
    if "error" in crypto_prices:
        return {"error": crypto_prices["error"]}
    
    results = {}
    for network, gas_data in gas_prices.items():
        if "error" in gas_data:
            results[network] = {"error": gas_data["error"]}
            continue
            
        # Map networks to their native tokens
        token_map = {
            "Ethereum Mainnet": "ethereum",
            "Fantom": "fantom",
            "Gnosis": "xdai",
            "Polygon": "matic-network",
            "Arbitrum One": "ethereum"
        }
        
        token = token_map.get(network)
        if not token:
            results[network] = {"error": "Unknown token mapping"}
            continue
            
        token_price = crypto_prices[token]["usd"]
        usd_cost = gas_data["native_token_cost"] * token_price
        
        # Use Decimal for more precise calculations
        usd_cost_decimal = Decimal(str(usd_cost)).quantize(Decimal('0.00000001'), rounding=ROUND_DOWN)
        
        results[network] = {
            "gas_price_gwei": gas_data["gas_price_gwei"],
            "native_token_cost": gas_data["native_token_cost"],
            "usd_cost": float(usd_cost_decimal),
            "token_price_usd": token_price,
            "gas_units": gas_data["gas_units"],
            "block_number": gas_data["block_number"],
            "timestamp": gas_data["timestamp"],
            "datetime": gas_data["datetime"],
            "rpc_url": gas_data["rpc_url"]
        }
    
    return results

def calculate_gas_costs_usd(gas_units: float = 1.0) -> Dict[str, Dict[str, Union[float, int, str]]]:
    """Calculate gas costs in USD for all networks."""
    return asyncio.run(calculate_gas_costs_usd_async(gas_units)) 