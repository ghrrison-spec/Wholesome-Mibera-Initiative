"""
Script to fetch NFT metadata from Mibera Maker collection on Berachain
Contract: 0x6666397dfe9a8c469bf65dc744cb1c733416c420
"""

import requests
import json
from typing import Optional, Dict, List

# Berachain RPC endpoints
BERACHAIN_RPC = "https://rpc.berachain.com"  # Main RPC
BERACHAIN_ARTIO_RPC = "https://artio.rpc.berachain.com"  # Testnet

# Contract address
MIBERA_CONTRACT = "0x6666397dfe9a8c469bf65dc744cb1c733416c420"

# Standard ERC-721 ABI for tokenURI function
ERC721_ABI = [
    {
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "tokenURI",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    }
]

def eth_call(rpc_url: str, to_address: str, data: str) -> Optional[str]:
    """Make an eth_call to read contract data"""
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{
            "to": to_address,
            "data": data
        }, "latest"],
        "id": 1
    }
    
    try:
        response = requests.post(rpc_url, json=payload, timeout=10)
        result = response.json()
        if "result" in result:
            return result["result"]
        else:
            print(f"Error in response: {result}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def decode_string(hex_data: str) -> str:
    """Decode a string from hex response"""
    if not hex_data or hex_data == "0x":
        return ""
    
    # Remove 0x prefix
    hex_data = hex_data[2:]
    
    # Skip first 64 chars (offset pointer)
    # Next 64 chars is the length
    # Rest is the actual string data
    if len(hex_data) > 128:
        string_data = hex_data[128:]
        # Convert hex to bytes and decode
        bytes_data = bytes.fromhex(string_data)
        # Remove null bytes and decode
        return bytes_data.rstrip(b'\x00').decode('utf-8', errors='ignore')
    return ""

def get_token_uri(token_id: int, rpc_url: str = BERACHAIN_RPC) -> Optional[str]:
    """Get the tokenURI for a specific token ID"""
    # Encode the function call for tokenURI(uint256)
    # Function signature: tokenURI(uint256) = 0xc87b56dd
    function_sig = "0xc87b56dd"
    # Pad token_id to 32 bytes (64 hex chars)
    token_id_hex = format(token_id, '064x')
    data = function_sig + token_id_hex
    
    result = eth_call(rpc_url, MIBERA_CONTRACT, data)
    if result:
        return decode_string(result)
    return None

def fetch_metadata_from_uri(uri: str) -> Optional[Dict]:
    """Fetch the actual JSON metadata from the URI"""
    # Handle IPFS URIs
    if uri.startswith("ipfs://"):
        # Convert to HTTP gateway
        ipfs_hash = uri.replace("ipfs://", "")
        uri = f"https://ipfs.io/ipfs/{ipfs_hash}"
    
    try:
        response = requests.get(uri, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch metadata: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        return None

def get_collection_name(rpc_url: str = BERACHAIN_RPC) -> Optional[str]:
    """Get the collection name"""
    # Function signature: name() = 0x06fdde03
    data = "0x06fdde03"
    
    result = eth_call(rpc_url, MIBERA_CONTRACT, data)
    if result:
        return decode_string(result)
    return None

def analyze_metadata(metadata: Dict) -> None:
    """Print analysis of NFT metadata"""
    print("\n" + "="*60)
    print("METADATA ANALYSIS")
    print("="*60)
    
    if "name" in metadata:
        print(f"\nName: {metadata['name']}")
    
    if "description" in metadata:
        print(f"\nDescription: {metadata['description']}")
    
    if "image" in metadata:
        image_url = metadata['image']
        if image_url.startswith("ipfs://"):
            image_url = f"https://ipfs.io/ipfs/{image_url.replace('ipfs://', '')}"
        print(f"\nImage URL: {image_url}")
    
    if "attributes" in metadata:
        print(f"\nAttributes/Traits ({len(metadata['attributes'])} total):")
        print("-" * 60)
        for attr in metadata['attributes']:
            trait_type = attr.get('trait_type', 'Unknown')
            value = attr.get('value', 'N/A')
            print(f"  • {trait_type}: {value}")
    
    # Show any other fields
    other_fields = {k: v for k, v in metadata.items() 
                   if k not in ['name', 'description', 'image', 'attributes']}
    if other_fields:
        print(f"\nOther Fields:")
        for key, value in other_fields.items():
            print(f"  • {key}: {value}")

def main():
    print("="*60)
    print("MIBERA MAKER METADATA FETCHER")
    print("="*60)
    print(f"Contract: {MIBERA_CONTRACT}")
    print(f"Chain: Berachain")
    
    # Try to get collection name
    print("\nFetching collection info...")
    collection_name = get_collection_name()
    if collection_name:
        print(f"Collection Name: {collection_name}")
    
    # Fetch metadata for token ID 1 as an example
    token_id = 1
    print(f"\nFetching metadata for Token ID #{token_id}...")
    
    token_uri = get_token_uri(token_id)
    if token_uri:
        print(f"Token URI: {token_uri}")
        
        print("\nFetching metadata JSON...")
        metadata = fetch_metadata_from_uri(token_uri)
        
        if metadata:
            analyze_metadata(metadata)
            
            # Save to file
            output_file = f"mibera_token_{token_id}_metadata.json"
            with open(output_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            print(f"\n✓ Full metadata saved to: {output_file}")
        else:
            print("Failed to fetch metadata JSON")
    else:
        print("Failed to fetch token URI")
    
    print("\n" + "="*60)
    print("\nTo fetch other tokens, modify the token_id variable")
    print("Or use this as a library in your own scripts")

if __name__ == "__main__":
    main()
