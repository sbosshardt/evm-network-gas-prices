from web3 import Web3
import requests
from datetime import datetime
from typing import Dict, Optional, Union
from decimal import Decimal, ROUND_DOWN

# Define RPC endpoints
RPC_ENDPOINTS = {
    "Ethereum Mainnet": "https://eth.merkle.io",
    "Arbitrum One": "https://arb1.arbitrum.io/rpc",
    "Gnosis": "https://rpc.gnosis.gateway.fm",
    "Polygon": "https://polygon-rpc.com",
    #"Fantom": "https://rpc.fantom.foundation",
    "Fantom": "https://fantom-pokt.nodies.app",
}

DEFAULT_GAS_UNITS = 1_000_000  # 1 million gas units

def wei_to_eth(wei: int) -> float:
    """Convert wei to ETH."""
    return wei / 10**18

def get_gas_prices(gas_units: float = 1.0) -> Dict[str, Dict[str, Union[float, int]]]:
    """Get gas prices for all networks.
    
    Args:
        gas_units: Number of million gas units to calculate for (default: 1.0)
    """
    actual_gas_units = int(gas_units * DEFAULT_GAS_UNITS)
    results = {}
    
    for name, url in RPC_ENDPOINTS.items():
        try:
            w3 = Web3(Web3.HTTPProvider(url))
            gas_price = w3.eth.gas_price  # in wei
            total_cost_wei = gas_price * actual_gas_units
            native_token_cost = wei_to_eth(total_cost_wei)
            
            results[name] = {
                "gas_price_gwei": float(Web3.from_wei(gas_price, 'gwei')),
                "total_cost_wei": total_cost_wei,
                "native_token_cost": native_token_cost,
                "gas_units": actual_gas_units
            }
        except Exception as e:
            results[name] = {"error": str(e)}
    
    return results

def get_crypto_prices() -> Dict[str, Dict[str, float]]:
    """Get cryptocurrency prices from CoinGecko."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "ethereum,fantom,matic-network",
        "vs_currencies": "usd,usdc"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Add xDAI (pegged to USD)
        data['xdai'] = {
            'usd': 1.00,
            'usdc': 1.00
        }
        
        return data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def calculate_gas_costs_usd(gas_units: float = 1.0) -> Dict[str, Dict[str, Union[float, str]]]:
    """Calculate gas costs in USD for all networks.
    
    Args:
        gas_units: Number of million gas units to calculate for (default: 1.0)
    """
    gas_prices = get_gas_prices(gas_units)
    crypto_prices = get_crypto_prices()
    
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
            "gas_units": gas_data["gas_units"]
        }
    
    return results 