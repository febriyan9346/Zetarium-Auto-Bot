# Zetarium Auto Bot

Automated bot for Zetarium Airdrop platform with daily check-in, faucet claiming, and prediction market trading features.

🔗 **Register Here**: [https://airdrop.zetarium.world/?ref=3e8f482b](https://airdrop.zetarium.world/?ref=3e8f482b)

## Features

- ✅ **Daily Check-in (GM Claim)** - Automatically claim daily points
- 💰 **Faucet Claiming** - Auto claim testnet USDC from faucet
- 🎯 **Prediction Market Trading** - Smart automated betting on prediction markets
- 🔄 **Multi-Account Support** - Process multiple accounts in sequence
- 🌐 **Proxy Support** - Optional proxy rotation for each account
- 📊 **Smart Betting Strategy** - Follows majority pool positions
- ⏰ **24-Hour Cycle** - Automatic daily execution

## Requirements

- Python 3.8 or higher
- BSC Testnet BNB (for gas fees)
- Zetarium account token
- Private key for wallet operations

## Installation

1. Clone this repository:
```bash
git clone https://github.com/febriyan9346/Zetarium-Auto-Bot.git
cd Zetarium-Auto-Bot
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### 1. Setup accounts.txt

Create a file named `accounts.txt` in the root directory with the following format:

```
token=your_bearer_token_here
private_key=your_wallet_private_key_here

token=another_bearer_token
private_key=another_private_key
```

**How to get your token:**
1. Login to [Zetarium Airdrop](https://airdrop.zetarium.world/?ref=3e8f482b)
2. Open Browser Developer Tools (F12)
3. Go to Network tab
4. Refresh the page
5. Find any request to `airdrop-data.zetarium.world`
6. Copy the `authorization` header value (it starts with `Bearer`)

### 2. Setup proxy.txt (Optional)

If you want to use proxies, create `proxy.txt`:

```
http://username:password@ip:port
http://username:password@ip:port
socks5://username:password@ip:port
```

## Usage

Run the bot:
```bash
python bot.py
```

### Menu Options

**Proxy Mode:**
- Option 1: Run with proxy (requires proxy.txt)
- Option 2: Run without proxy

**Action Mode:**
- Option 1: Run Daily Check-in only
- Option 2: Run All features (Check-in + Faucet + Trading)
  - You'll be asked how many trades to execute per account

## Features Breakdown

### Daily GM Claim
- Claims daily points through signature verification
- Automatically detects if already claimed today
- Awards points to your Zetarium account

### Faucet Claiming
- Claims testnet USDC tokens from the Zetarium faucet
- Can be claimed once per day per wallet
- Provides tokens needed for prediction market trading

### Prediction Market Trading
- Fetches all active prediction markets
- Implements smart betting strategy:
  - Follows the majority pool (Yes or No)
  - Random selection when pools are equal
- Customizable number of trades per account
- Random bet amounts between 50-100 USDC
- Automatic USDC approval for trading contract

## Smart Contracts

The bot interacts with the following BSC Testnet contracts:

- **USDC Token**: `0x2186fc0e8404eCF9F63cCBf1C75d5fAF6B843786`
- **Prediction Market**: `0x852a5C778034e0776181955536528347Aa901d24`
- **Faucet Contract**: `0xc9e16209Ed6B2A4f41b751788FE74F5c0B7F8E1c`

## Important Notes

⚠️ **Security Warning:**
- Never share your private keys
- Use testnet wallets only for testing
- This bot is for educational purposes

⚠️ **Rate Limiting:**
- The bot includes random delays to avoid rate limiting
- Daily cycle runs every 24 hours automatically

⚠️ **Gas Fees:**
- Ensure your wallet has BSC Testnet BNB for gas fees
- Get testnet BNB from [BSC Faucet](https://testnet.bnbchain.org/faucet-smart)

## Troubleshooting

**"Login Failed / Token Expired"**
- Your bearer token has expired
- Get a new token from the browser developer tools

**"Insufficient USDC Balance"**
- Run the faucet claim first
- Wait for faucet to be available (24h cooldown)

**"Transaction Failed on Blockchain"**
- Check if you have enough testnet BNB for gas
- Market might be closed or betting deadline passed

## Donations

If this bot helped you, consider supporting the developer:

### Support Us with Cryptocurrency

You can make a contribution using any of the following blockchain networks:

| Network | Wallet Address |
|---------|---------------|
| **EVM** | `0x216e9b3a5428543c31e659eb8fea3b4bf770bdfd` |
| **TON** | `UQCEzXLDalfKKySAHuCtBZBARCYnMc0QsTYwN4qda3fE6tto` |
| **SOL** | `9XgbPg8fndBquuYXkGpNYKHHhymdmVhmF6nMkPxhXTki` |
| **SUI** | `0x8c3632ddd46c984571bf28f784f7c7aeca3b8371f146c4024f01add025f993bf` |

## Disclaimer

This bot is provided for educational purposes only. Use at your own risk. The author is not responsible for any losses or damages that may occur from using this software.

## License

MIT License - feel free to modify and distribute

## Author

Created by **FEBRIYAN**

---

⭐ If you find this bot useful, please star this repository!

📢 Join the community and share your experience!