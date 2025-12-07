"""Network-related utilities for the EVM gas price monitor."""

from typing import Dict, List, TypedDict
import random

class NetworkInfo(TypedDict):
    """Type definition for network information."""
    name: str
    native_token: str
    native_token_symbol: str
    coingecko_id: str

# Define network information
NETWORKS: Dict[str, NetworkInfo] = {
    "Ethereum Mainnet": {
        "name": "Ethereum",
        "native_token": "Ether",
        "native_token_symbol": "ETH",
        "coingecko_id": "ethereum"
    },
    "Arbitrum One": {
        "name": "Arbitrum",
        "native_token": "Ether",
        "native_token_symbol": "ETH",
        "coingecko_id": "ethereum"
    },
    "Optimism": {
        "name": "Optimism",
        "native_token": "Ether",
        "native_token_symbol": "ETH",
        "coingecko_id": "ethereum"
    },
    "Base": {
        "name": "Base",
        "native_token": "Ether",
        "native_token_symbol": "ETH",
        "coingecko_id": "ethereum"
    },
    "Gnosis": {
        "name": "Gnosis",
        "native_token": "xDai",
        "native_token_symbol": "xDAI",
        "coingecko_id": "xdai"
    },
    "Polygon": {
        "name": "Polygon",
        "native_token": "Polygon",
        "native_token_symbol": "POL",
        "coingecko_id": "polygon-ecosystem-token"
    },
    "Avalanche": {
        "name": "Avalanche",
        "native_token": "Avalanche",
        "native_token_symbol": "AVAX",
        "coingecko_id": "avalanche-2"
    },
    "BSC": {
        "name": "Binance Smart Chain",
        "native_token": "Binance Coin",
        "native_token_symbol": "BNB",
        "coingecko_id": "binancecoin"
    },
    "Fantom": {
        "name": "Fantom",
        "native_token": "Fantom",
        "native_token_symbol": "FTM",
        "coingecko_id": "fantom"
    },
    "Linea": {
        "name": "Linea",
        "native_token": "Ether",
        "native_token_symbol": "ETH",
        "coingecko_id": "ethereum"
    }
}

# Define RPC endpoints with fallbacks
RPC_ENDPOINTS: Dict[str, List[str]] = {
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
    "Optimism": [
        "https://mainnet.optimism.io",
        "https://optimism.public.blastapi.io",
        "https://optimism.llamarpc.com"
    ],
    "Base": [
        "https://mainnet.base.org",
        "https://base.public.blastapi.io",
        "https://base.llamarpc.com"
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
    "Avalanche": [
        "https://api.avax.network/ext/bc/C/rpc",
        "https://avalanche.public.blastapi.io",
        "https://avalanche.llamarpc.com"
    ],
    "BSC": [
        "https://bsc-dataseed.binance.org",
        "https://bsc.public.blastapi.io",
        "https://bsc.llamarpc.com"
    ],
    "Fantom": [
        "https://fantom-pokt.nodies.app",
        "https://fantom.public.blastapi.io",
        "https://fantom.llamarpc.com"
    ],
    "Linea": [
        "https://rpc.linea.build",
        "https://linea.public.blastapi.io",
        "https://linea.llamarpc.com"
    ]
}

# Track last used endpoint for each network
last_used_endpoints = {network: None for network in RPC_ENDPOINTS.keys()}

# Map networks to their native tokens
TOKEN_MAP = {
    "Ethereum Mainnet": "ethereum",
    "Arbitrum One": "ethereum",
    "Optimism": "ethereum",
    "Base": "ethereum",
    "Fantom": "fantom",
    "Gnosis": "xdai",
    "Polygon": "polygon-ecosystem-token",
    "Avalanche": "avalanche-2",
    "BSC": "binancecoin",
    "Linea": "ethereum"
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

def format_network_help() -> str:
    """Format the network help text for CLI output."""
    lines = []
    for network, info in NETWORKS.items():
        lines.append(f"  - {network:<20} ({info['native_token']}, {info['native_token_symbol']})")
    return "\n".join(lines)

def get_network_info(network: str) -> NetworkInfo:
    """Get information about a network."""
    return NETWORKS.get(network, {
        "name": network,
        "native_token": "Unknown",
        "native_token_symbol": "???",
        "coingecko_id": "unknown"
    }) 