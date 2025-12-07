"""Core utilities for the EVM gas price monitor."""

from web3 import Web3
import asyncio
import aiohttp
from datetime import datetime
import time
from typing import Dict, Union, List
from decimal import Decimal, ROUND_DOWN

from networks import RPC_ENDPOINTS, get_network_info
from currencies import (
    SUPPORTED_CURRENCIES,
    get_currency_symbol, get_currency_name, get_all_currencies,
    normalize_currency, get_locale_currency
)

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

async def fetch_network_data(network: str, gas_units: int, timestamps: Dict[str, Union[int, str]]) -> Dict:
    """Fetch data for a single network, retrying with different endpoints if one fails."""
    endpoints = RPC_ENDPOINTS[network]
    errors = []
    
    # Try each endpoint until one succeeds
    for endpoint in endpoints:
        try:
            w3 = Web3(Web3.HTTPProvider(endpoint))
            
            # Get fee history with percentiles
            fee_history = w3.eth.fee_history(
                block_count=5,
                newest_block='latest',
                reward_percentiles=[10, 50, 90]
            )
            
            # Calculate gas prices for each percentile
            gas_prices_gwei = {}
            native_token_costs = {}
            
            for i, percentile in enumerate([10, 50, 90]):
                # Calculate total gas price (base fee + priority fee)
                base_fee = fee_history['baseFeePerGas'][-1]  # Use the latest base fee
                priority_fee = fee_history['reward'][-1][i]  # Get priority fee for this percentile
                total_gas_price = base_fee + priority_fee
                
                # Convert to gwei and calculate costs
                gas_price_gwei = float(Web3.from_wei(total_gas_price, 'gwei'))
                total_cost_wei = total_gas_price * gas_units
                native_token_cost = wei_to_eth(total_cost_wei)
                
                gas_prices_gwei[str(percentile)] = gas_price_gwei
                native_token_costs[str(percentile)] = native_token_cost
            
            block_number = w3.eth.block_number
            network_info = get_network_info(network)
            
            return {
                "gas_prices_gwei": gas_prices_gwei,
                "native_token_costs": native_token_costs,
                "native_token": network_info["native_token"],
                "native_token_symbol": network_info["native_token_symbol"],
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

async def get_crypto_prices_async(currencies: List[str] = None) -> Dict[str, Dict[str, Union[float, int, str]]]:
    """Get cryptocurrency prices from CoinGecko asynchronously."""
    if currencies is None:
        currencies = [get_locale_currency()]
    elif "all" in currencies:
        currencies = get_all_currencies()
    
    # Convert currencies to lowercase for API call
    api_currencies = [c.lower() for c in currencies]
    
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "ethereum,fantom,polygon-ecosystem-token,xdai,avalanche-2,binancecoin,optimism,base",
        "vs_currencies": ",".join(api_currencies)
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

def get_crypto_prices(currencies: List[str] = None) -> Dict[str, Dict[str, Union[float, int, str]]]:
    """Get cryptocurrency prices."""
    return asyncio.run(get_crypto_prices_async(currencies))

async def calculate_gas_costs_async(gas_units: float = 1.0, currencies: List[str] = None) -> Dict[str, Dict[str, Union[float, int, str]]]:
    """Calculate gas costs in specified currencies for all networks asynchronously."""
    if currencies is None:
        currencies = [get_locale_currency()]
    elif "all" in currencies:
        currencies = get_all_currencies()
    
    # Normalize currencies to uppercase for display
    currencies = [normalize_currency(c) for c in currencies]
    
    # Fetch gas prices and crypto prices concurrently
    gas_prices_task = get_gas_prices_async(gas_units)
    crypto_prices_task = get_crypto_prices_async(currencies)
    
    gas_prices, crypto_prices = await asyncio.gather(gas_prices_task, crypto_prices_task)
    
    if "error" in crypto_prices:
        return {"error": crypto_prices["error"]}
    
    results = {}
    for network, gas_data in gas_prices.items():
        if "error" in gas_data:
            results[network] = {"error": gas_data["error"]}
            continue
            
        network_info = get_network_info(network)
        token = network_info["coingecko_id"]
        
        # Calculate costs in each currency for each percentile
        costs = {}
        token_prices = {}
        for currency in currencies:
            # Use lowercase for API data lookup
            token_data = crypto_prices.get(token, {})
            if not token_data or currency.lower() not in token_data:
                # Skip this currency/token combination if price data is unavailable
                continue

            token_price = token_data[currency.lower()]
            token_price_decimal = Decimal(str(token_price)).quantize(Decimal('0.00000001'), rounding=ROUND_DOWN)
            token_prices[currency] = float(token_price_decimal)

            # Calculate costs for each percentile
            costs[currency] = {}
            for percentile in ["10", "50", "90"]:
                native_token_cost = gas_data["native_token_costs"][percentile]
                cost = native_token_cost * token_price
                cost_decimal = Decimal(str(cost)).quantize(Decimal('0.00000001'), rounding=ROUND_DOWN)
                costs[currency][percentile] = float(cost_decimal)
        
        results[network] = {
            "gas_prices_gwei": gas_data["gas_prices_gwei"],
            "native_token_costs": gas_data["native_token_costs"],
            "native_token": gas_data["native_token"],
            "native_token_symbol": gas_data["native_token_symbol"],
            "gas_units": gas_data["gas_units"],
            "block_number": gas_data["block_number"],
            "timestamp": gas_data["timestamp"],
            "datetime": gas_data["datetime"],
            "rpc_url": gas_data["rpc_url"],
            "costs": costs,
            "token_prices": token_prices
        }
    
    return results

def calculate_gas_costs(gas_units: float = 1.0, currencies: List[str] = None) -> Dict[str, Dict[str, Union[float, int, str]]]:
    """Calculate gas costs in specified currencies for all networks."""
    return asyncio.run(calculate_gas_costs_async(gas_units, currencies)) 