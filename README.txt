# Zetarium Auto Bot

🌐 **[Join Zetarium Airdrop](https://airdrop.zetarium.world/?ref=3e8f482b)**

An automated bot for claiming daily GM points on Zetarium platform.

## Features

- ✅ Auto claim daily GM points
- ✅ Multi-account support
- ✅ Proxy support
- ✅ Automatic wallet signing
- ✅ Real-time logging with colors
- ✅ Auto-retry mechanism
- ✅ 24-hour cycle automation

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/febriyan9346/Zetarium-Auto-Bot.git
cd Zetarium-Auto-Bot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

### Setting up accounts.txt

Create an `accounts.txt` file in the root directory with the following format:

```
token=your_bearer_token_here
private_key=your_private_key_here

token=another_token
private_key=another_private_key
```

**How to get your token:**
1. Open [Zetarium Airdrop](https://airdrop.zetarium.world/?ref=3e8f482b)
2. Open Developer Tools (F12)
3. Go to Network tab
4. Look for requests to `airdrop-data.zetarium.world`
5. Find the Authorization header (Bearer token)

**Private Key:**
- Use your Ethereum wallet private key
- This is needed for signing GM claim messages
- Keep it secure and never share it

### Setting up proxy.txt (Optional)

If you want to use proxies, create a `proxy.txt` file:

```
http://username:password@proxy1:port
http://username:password@proxy2:port
socks5://username:password@proxy3:port
```

## Usage

Run the bot:
```bash
python bot.py
```

Select your preferred mode:
- **1**: Run with proxy
- **2**: Run without proxy

The bot will:
1. Load all accounts from `accounts.txt`
2. Process each account sequentially
3. Claim daily GM points if available
4. Display current points, streak, and statistics
5. Wait 24 hours before the next cycle

## Features Explanation

### Daily GM Claim
- Claims daily points with streak multiplier
- Shows points earned, total points, and streak days
- Automatically handles "already claimed" status

### Multi-Account Support
- Process unlimited accounts
- Each account processed independently
- Continues even if one account fails

### Proxy Rotation
- Automatically rotates proxies for each account
- Supports HTTP and SOCKS5 proxies
- Falls back to no proxy if proxy fails

### Smart Logging
- Color-coded messages for easy monitoring
- Real-time timestamps (WIB timezone)
- Detailed success/error reporting

## Output Example

```
[12:34:56] [INFO] Account #1/3
[12:34:56] [INFO] Proxy: http://proxy1:port
[12:34:59] [SUCCESS] Login successful! Username: YourUsername
[12:35:02] [INFO] Wallet: 0x1234...5678
[12:35:02] [INFO] Checking Daily GM Status...
[12:35:05] [SUCCESS] Daily GM Claimed Successfully! ✓
------------------------------------------------------------
Status           : Claim Success
Points Earned    : +150 Points (Multiplier: x3)
Total Points     : 5,420 Points
Streak Days      : 7 days
GM Count         : 15 times
Last GM Time     : 2026-01-08T12:35:05Z
```

## Error Handling

The bot handles various scenarios:
- Invalid tokens
- Network errors
- Already claimed GM
- Invalid private keys
- Proxy failures

## Security Notes

⚠️ **Important Security Information:**
- Never share your `accounts.txt` file
- Keep your private keys secure
- Use `.gitignore` to prevent committing sensitive files
- Consider using test accounts for initial setup

## Troubleshooting

### "No accounts found"
- Check if `accounts.txt` exists in the same directory as `bot.py`
- Verify the format is correct (token= and private_key=)

### "Failed to get user info"
- Token might be expired, get a new one
- Check your internet connection
- Verify proxy settings if using proxy mode

### "Invalid private key"
- Ensure private key is in correct format (0x prefix optional)
- Check for extra spaces or characters

## Disclaimer

This bot is for educational purposes only. Use at your own risk. The author is not responsible for any consequences resulting from the use of this bot.

## License

MIT License - See [LICENSE](LICENSE) file for details

## Contact

- GitHub: [@febriyan9346](https://github.com/febriyan9346)
- Issues: [GitHub Issues](https://github.com/febriyan9346/Zetarium-Auto-Bot/issues)

---

## Support Us with Cryptocurrency

You can make a contribution using any of the following blockchain networks:

| Network | Wallet Address |
|---------|----------------|
| **EVM** | `0x216e9b3a5428543c31e659eb8fea3b4bf770bdfd` |
| **TON** | `UQCEzXLDalfKKySAHuCtBZBARCYnMc0QsTYwN4qda3fE6tto` |
| **SOL** | `9XgbPg8fndBquuYXkGpNYKHHhymdmVhmF6nMkPxhXTki` |
| **SUI** | `0x8c3632ddd46c984571bf28f784f7c7aeca3b8371f146c4024f01add025f993bf` |

Your support helps maintain and improve this project! 💖