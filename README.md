# 🤖 Discord Economy Bot

<div align="center">

![Discord.py](https://img.shields.io/badge/discord.py-2.3.0+-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A feature-rich Discord economy bot with **slash commands only**, shop system, gambling games, and admin tools!

[Features](#-features) • [Quick Setup](#-quick-setup) • [Commands](#-commands) • [Customization](#%EF%B8%8F-customization)

</div>

---

## ✨ Features

### 💰 Complete Economy System
- **Balance Management** - Separate wallet and bank with limits
- **Daily Rewards** - Claim daily rewards with streak bonuses (up to $1,500)
- **Work Command** - 10 different jobs earning $90-$500 per hour
- **Banking System** - Secure money storage with customizable limits
- **Leaderboard** - Competitive rankings for richest users

### 🏪 Shop & Inventory
- **8 Default Items** - From cookies ($50) to houses ($500,000)
- **Buy System** - Purchase items with earned money
- **Sell System** - Sell items back for 70% of purchase price
- **Inventory Management** - Track all owned items
- **Customizable Shop** - Easy to add custom items

### 🎰 Gambling Games
- **Coinflip** - 50/50 chance, 2x multiplier
- **Slot Machine** - Match 3 symbols for up to 10x jackpot
- **Dice Game** - Guess the roll (1-6) for 6x multiplier
- **Blackjack** - Play against dealer for 2x multiplier

### ⚙️ Admin Tools
- **Money Management** - Add/remove money from users
- **User Reset** - Reset individual user data
- **Bank Limits** - Set custom bank limits per user
- **Economy Stats** - View server-wide statistics
- **Help Command** - Comprehensive command reference

### 🎨 Modern Design
- ✅ **Slash Commands ONLY** - No prefix commands at all
- ✅ **All Config in main.py** - No .env files needed
- ✅ **Beautiful Embeds** - Rich, colorful command responses
- ✅ **Emoji Integration** - Visual and engaging interface
- ✅ **Modular Cogs** - Clean, organized code structure

---

## 🚀 Quick Setup

### 1. Clone Repository
```bash
git clone https://github.com/aurora9161/discord-economy-bot.git
cd discord-economy-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and name it
3. Navigate to "Bot" tab and click "Add Bot"
4. Enable these **Privileged Gateway Intents**:
   - ✅ Server Members Intent
   - ✅ Message Content Intent
5. Click "Reset Token" and copy your bot token

### 4. Configure Bot
Open `main.py` and edit the Config class at the top:

```python
class Config:
    # REQUIRED: Add your bot token here
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    
    # Optional: Customize these settings
    STATUS_MESSAGE = "your economy | /help"
    DEFAULT_BANK_LIMIT = 5000
    DAILY_BASE_REWARD = 500
    # ... more settings
```

### 5. Invite Bot to Server
1. Go to "OAuth2" → "URL Generator" in Developer Portal
2. Select scopes: `bot` + `applications.commands`
3. Select permissions:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
   - ✅ Use Slash Commands
4. Copy URL and invite bot to your server

### 6. Run the Bot
```bash
python main.py
```

**The bot will automatically:**
- Validate your configuration
- Create the SQLite database
- Initialize shop items
- Sync all slash commands
- Display ready status

---

## 📝 Commands

### 💰 Economy Commands (6)
| Command | Description | Cooldown |
|---------|-------------|----------|
| `/balance [user]` | Check balance (wallet + bank) | None |
| `/daily` | Claim daily reward + streak bonus | 24 hours |
| `/work` | Work for money (random jobs) | 1 hour |
| `/deposit <amount>` | Deposit money to bank | None |
| `/withdraw <amount>` | Withdraw money from bank | None |
| `/leaderboard` | View top 10 richest users | None |

### 🏪 Shop Commands (4)
| Command | Description |
|---------|-------------|
| `/shop` | View all available items |
| `/buy <item> [quantity]` | Buy item from shop |
| `/sell <item> [quantity]` | Sell item for 70% price |
| `/inventory [user]` | View inventory |

### 🎰 Gambling Commands (4)
| Command | Description | Multiplier |
|---------|-------------|------------|
| `/coinflip <bet> <choice>` | Bet on heads or tails | 2x |
| `/slots <bet>` | Spin the slot machine | 2x-10x |
| `/dice <bet> <guess>` | Guess the dice roll | 6x |
| `/blackjack <bet>` | Play against dealer | 2x |

### ⚙️ Admin Commands (6) - Requires Administrator
| Command | Description |
|---------|-------------|
| `/addmoney <user> <amount>` | Add money to user wallet |
| `/removemoney <user> <amount>` | Remove money from user |
| `/resetuser <user>` | Reset user economy data |
| `/setbank <user> <limit>` | Set user bank limit |
| `/econostats` | View server statistics |
| `/help` | Show all commands |

**Total: 20 slash commands** - Zero prefix commands!

---

## 🛠️ Customization

All configuration is in `main.py` in the `Config` class at the top of the file!

### Bot Token & Status
```python
BOT_TOKEN = "your_token_here"
STATUS_TYPE = discord.ActivityType.watching
STATUS_MESSAGE = "your economy | /help"
```

### Economy Settings
```python
DEFAULT_BANK_LIMIT = 5000
DAILY_BASE_REWARD = 500
DAILY_STREAK_BONUS = 50
MAX_STREAK_BONUS = 1000
WORK_COOLDOWN_HOURS = 1
WORK_MIN_EARNINGS = 90
WORK_MAX_EARNINGS = 500
```

### Shop Items
```python
SHOP_ITEMS = [
    ("item_name", price, "description", "emoji"),
    ("sword", 1000, "A sharp sword ⚔️", "⚔️"),
    # Add more items here!
]
```

### Sell Price
```python
SELL_PRICE_MULTIPLIER = 0.7  # 70% of original price
```

---

## 📁 Project Structure

```
discord-economy-bot/
├── main.py                 # Bot + Config (edit this!)
├── requirements.txt        # Dependencies
├── .gitignore             # Git ignore rules
├── README.md              # This file
│
├── cogs/                  # Command modules
│   ├── __init__.py
│   ├── economy.py         # Economy commands
│   ├── shop.py            # Shop & inventory
│   ├── gambling.py        # Gambling games
│   └── admin.py           # Admin commands
│
└── utils/                 # Utilities
    ├── __init__.py
    └── database.py        # Database handler
```

---

## 🎮 How to Play

### Getting Started
1. Use `/work` every hour to earn money ($90-$500)
2. Use `/daily` once per day for bigger rewards ($500+)
3. Build up your daily streak for bonus money (up to $1,000)!

### Managing Money
- Keep money in **wallet** for quick access
- Store money in **bank** for safety (protected from gambling losses)
- Bank has limits - use `/deposit` and `/withdraw`

### Shopping
1. Check `/shop` to see all items
2. Use `/buy <item>` to purchase
3. Use `/inventory` to see what you own
4. Sell items with `/sell <item>` for 70% back

### Gambling
- Risk your money for big multipliers!
- **Coinflip**: 50/50 chance, 2x payout
- **Slots**: Match 3 for up to 10x jackpot
- **Dice**: Guess right for 6x payout
- **Blackjack**: Beat the dealer for 2x

### Competing
- Check `/leaderboard` to see who's richest
- Your rank is based on total wealth (wallet + bank)
- Compete with friends for #1!

---

## 🐛 Troubleshooting

### Bot doesn't start
- Check that `BOT_TOKEN` is set correctly in `main.py`
- Make sure you're using a valid bot token
- Verify all dependencies are installed

### Slash commands don't appear
- Wait 5-10 minutes for Discord to sync commands
- Reinvite bot with `applications.commands` scope
- Check bot has proper server permissions
- Verify intents are enabled in Developer Portal

### Database errors
- Delete `economy.db` file and restart bot
- Check write permissions in directory
- Make sure aiosqlite is installed

---

## 💡 Tips & Best Practices

### For Users
- 💾 Always keep money in bank for safety
- 🔥 Maintain daily streaks for maximum rewards
- 🎰 Don't gamble more than you can afford to lose
- 📈 Check leaderboard to track progress

### For Admins
- 📊 Use `/econostats` to monitor economy health
- 🏦 Adjust bank limits in Config for balance
- 💰 Be careful with `/addmoney` to avoid inflation
- 🔄 Use `/resetuser` sparingly

### For Developers
- 📦 All config is in main.py Config class
- 🗄️ Database is SQLite - simple and portable
- 🎨 Embeds follow consistent color scheme
- ✅ No prefix commands - slash only!
- 🔧 Cogs are modular - easy to modify

---

## 📊 Key Features

✅ **Slash Commands Only** - No prefix command processing  
✅ **Config in main.py** - No .env files needed  
✅ **Modular Cogs** - Easy to extend and customize  
✅ **SQLite Database** - Persistent data storage  
✅ **Beautiful Embeds** - Rich Discord UI  
✅ **Cooldown System** - Prevents spam  
✅ **Permission Checks** - Admin commands protected  
✅ **Error Handling** - User-friendly messages  

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests
- 📖 Improve documentation

---

## 📋 License

This project is open source and free to use/modify.

---

## 🌟 Credits

Built with ❤️ using:
- [discord.py](https://github.com/Rapptz/discord.py)
- [aiosqlite](https://github.com/omnilib/aiosqlite)

---

<div align="center">

**Enjoy your economy bot!** 🎉

**Slash Commands Only** | **Config in main.py** | **No .env Required**

[⬆ Back to Top](#-discord-economy-bot)

</div>
