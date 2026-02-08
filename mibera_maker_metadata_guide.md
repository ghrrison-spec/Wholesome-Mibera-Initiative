# Mibera Maker NFT Metadata Access Guide

## Collection Information

**Contract Address:** `0x6666397dfe9a8c469bf65dc744cb1c733416c420`  
**Blockchain:** Berachain Mainnet  
**Collection Size:** ~10,000 NFTs (9,989 on OpenSea)  
**Type:** Generative dNFTs (dynamic NFTs)  
**Aesthetic:** Neochibi style with rave culture cosmetics  

### Key Stats
- **Floor Price:** ~34.94 BERA
- **Total Volume:** 596K+ BERA
- **Unique Owners:** 2,906 (29.1% ownership rate)
- **Listed:** 0.9%

## Collection Background

Mibera Maker is described as an "anti-derivative" of Milady Maker, created by janitooor and connected to The Honey Jar (THJ) ecosystem on Berachain. The collection features:

- **Advanced trait layering** with rarity for hats, molecules, and synergy
- **Birth data and location** assigned during mint
- **Custom scores** for each token
- **dNFT daemon architecture** - tokens can interact with code on-chain even when owner is offline
- **Potential DeFi composability** built into the design

The project sits at the intersection of rave culture subculture and on-chain innovation.

## Methods to Access Metadata

### Option 1: Using Python Script (Direct RPC)

The script I created (`fetch_mibera_metadata.py`) allows you to fetch metadata directly from the Berachain blockchain. However, you'll need to use a working RPC endpoint.

#### Available RPC Endpoints:

**Free Public RPCs:**
- Chainstack: 3M requests/month free tier
- dRPC: Has free tier available
- Public testnet: `https://bartio.rpc.berachain.com/` (testnet only)

**Paid RPC Providers (with free tiers):**
- Alchemy: `https://berachain-mainnet.g.alchemy.com/v2/<api-key>`
- QuickNode: Offers Berachain RPC
- Nirvana Labs: Berachain support
- Tatum: `berachain-mainnet.gateway.tatum.io`
- Dwellir: `https://api-berachain-mainnet.n.dwellir.com/<api-key>`

**Rate Limits (Public Berachain RPC):**
- 50 requests per second
- 2,000 requests per minute
- 100,000 requests per day

#### Usage:

```python
# Modify the script to use a working RPC endpoint
BERACHAIN_RPC = "https://your-rpc-endpoint-here"

# Then run:
python3 fetch_mibera_metadata.py
```

### Option 2: Using NFT APIs

Several providers offer dedicated NFT APIs that are easier to use:

#### Reservoir API
Base URL: `https://api-berachain-testnet.reservoir.tools/`

```bash
curl --location 'https://api-berachain-testnet.reservoir.tools/users/0xWALLET_ADDRESS/tokens/v6' \
  --header 'x-api-key: <YOUR-RESERVOIR-API-KEY>'
```

#### Routescan API
Get NFT holdings by wallet address:

```bash
curl --location 'https://api.routescan.io/v2/network/testnet/evm/80084/address/0xWALLET_ADDRESS/erc721-holdings'
```

### Option 3: Block Explorers

**Beratrail (Official Explorer):**
- Website: https://bartio.beratrail.io/
- API Documentation: https://bartio.beratrail.io/documentation/api-swagger

You can search for the contract address and browse individual tokens with their metadata.

### Option 4: Marketplace APIs

#### OpenSea
The collection is available on OpenSea:
- URL: https://opensea.io/collection/mibera333
- OpenSea has APIs to fetch collection and individual NFT data

#### Magic Eden
The collection is also on Magic Eden:
- URL: https://magiceden.us/collections/berachain/0x6666397dfe9a8c469bf65dc744cb1c733416c420

## Expected Metadata Structure

Based on the collection description, Mibera Maker NFTs likely have metadata structured like:

```json
{
  "name": "Mibera Maker #1",
  "description": "A generative dNFT in neochibi aesthetic...",
  "image": "ipfs://...",
  "attributes": [
    {
      "trait_type": "Hat",
      "value": "Rave Cap"
    },
    {
      "trait_type": "Molecule",
      "value": "Serotonin"
    },
    {
      "trait_type": "Synergy",
      "value": "High"
    },
    {
      "trait_type": "Birth Location",
      "value": "Tokyo"
    },
    {
      "trait_type": "Birth Date",
      "value": "2025-01-15"
    },
    {
      "trait_type": "Custom Score",
      "value": "850"
    },
    {
      "trait_type": "Cosmetic Style",
      "value": "90s Techno"
    }
    // ... more traits
  ],
  "properties": {
    "daemon_enabled": true,
    "onchain_interactions": true
  }
}
```

## Advanced: Using Web3 Libraries

### JavaScript/TypeScript (ethers.js)

```javascript
import { ethers } from 'ethers';

// Connect to Berachain
const provider = new ethers.JsonRpcProvider('YOUR_RPC_ENDPOINT');

// Contract ABI (minimal)
const abi = [
  "function tokenURI(uint256 tokenId) view returns (string)"
];

const contract = new ethers.Contract(
  '0x6666397dfe9a8c469bf65dc744cb1c733416c420',
  abi,
  provider
);

// Get token URI
const tokenURI = await contract.tokenURI(1);
console.log(tokenURI);

// Fetch metadata
const response = await fetch(tokenURI);
const metadata = await response.json();
console.log(metadata);
```

### Python (web3.py)

```python
from web3 import Web3

# Connect to Berachain
w3 = Web3(Web3.HTTPProvider('YOUR_RPC_ENDPOINT'))

# Contract ABI
abi = [{
    "inputs": [{"name": "tokenId", "type": "uint256"}],
    "name": "tokenURI",
    "outputs": [{"name": "", "type": "string"}],
    "stateMutability": "view",
    "type": "function"
}]

# Create contract instance
contract = w3.eth.contract(
    address='0x6666397dfe9a8c469bf65dc744cb1c733416c420',
    abi=abi
)

# Get token URI
token_uri = contract.functions.tokenURI(1).call()
print(f"Token URI: {token_uri}")

# Fetch metadata from URI
import requests
metadata = requests.get(token_uri).json()
print(metadata)
```

## Trait Categories (Expected)

Based on the collection description, Mibera Maker likely includes these trait categories:

1. **Hats/Headwear** - Rave-inspired accessories
2. **Molecules** - Chemical/drug references (thematic to rave culture)
3. **Synergy** - Interaction quality metrics
4. **Cosmetics** - Visual styling elements
5. **Era/Style** - Different rave culture time periods
6. **Birth Data** - Mint timestamp or assigned date
7. **Location** - Geographic or virtual location
8. **Custom Score** - Rarity or performance metric
9. **Daemon Status** - On-chain interaction capabilities

## Next Steps

1. **Get an RPC API Key:** Sign up for Alchemy, QuickNode, or Chainstack for free tier access
2. **Update the Script:** Replace the RPC endpoint in `fetch_mibera_metadata.py`
3. **Run the Script:** Fetch metadata for specific token IDs
4. **Analyze Traits:** Use the metadata to understand rarity and distribution
5. **Build Tools:** Create custom analytics or trading tools based on the metadata

## Resources

- **Berachain Docs:** https://docs.berachain.com/
- **RPC Guide:** https://blog.berachain.com/blog/your-berachain-rpc-guide
- **OpenSea Collection:** https://opensea.io/collection/mibera333
- **Magic Eden:** https://magiceden.us/collections/berachain/0x6666397dfe9a8c469bf65dc744cb1c733416c420
- **Berachain Explorer:** https://berascan.com/

## Important Notes

- Mibera Maker uses **dNFT (dynamic NFT)** technology, meaning metadata can change over time
- The collection has **on-chain daemon architecture**, enabling autonomous interactions
- Check the specific RPC provider's documentation for authentication methods
- Always respect rate limits to avoid being blocked
- IPFS URIs may need to be converted to HTTP gateway URLs (e.g., `https://ipfs.io/ipfs/...`)

## Support

If you run into issues:
- Berachain Discord: Check official server for developer support
- Berachain Telegram: Community help available
- The Honey Jar: Connect with the Mibera team and community
