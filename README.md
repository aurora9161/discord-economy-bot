# 🤖 Discord Economy Bot

<div align="center">

![Discord.py](https://img.shields.io/badge/discord.py-2.3.0+-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A feature-rich Discord economy bot with slash commands, shop system, gambling games, and admin tools built with discord.py!

[Features](#-features) • [Installation](#-installation) • [Commands](#-commands) • [Setup](#-quick-setup)

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
- ✅ **Slash Commands Only** - Native Discord integration
- ✅ **Beautiful Embeds** - Rich, colorful command responses
- ✅ **Emoji Integration** - Visual and engaging interface
- ✅ **Error Handling** - User-friendly error messages
- ✅ **Modular Cogs** - Clean, organized code structure

---

## 📋 Requirements

- **Python 3.8+**
- **discord.py 2.3.0+**
- **aiosqlite**
- **python-dotenv**

---

## 🚀 Installation

### 1. Clone Repository
```bash
git clone https://github.com/aurora9161/discord-economy-bot.git
cd discord-economy-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create Discord Application
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and name it
3. Navigate to "Bot" tab and click "Add Bot"
4. Enable these **Privileged Gateway Intents**:
   - ✅ Server Members Intent
   - ✅ Message Content Intent
5. Click "Reset Token" and copy your bot token

### 4. Configure Environment
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your token
DISCORD_TOKEN=your_bot_token_here
```

### 5. Invite Bot to Server
1. Go to "OAuth2" → "URL Generator"
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
- Create the SQLite database
- Initialize shop items
- Sync all slash commands
- Display status when ready

---

## 📝 Commands

### 💰 Economy Commands
| Command | Description | Cooldown |
|---------|-------------|----------|
| `/balance [user]` | Check balance (wallet + bank) | None |
| `/daily` | Claim daily reward + streak bonus | 24 hours |
| `/work` | Work for money (random jobs) | 1 hour |
| `/deposit <amount>` | Deposit money to bank | None |
| `/withdraw <amount>` | Withdraw money from bank | None |
| `/leaderboard` | View top 10 richest users | None |

### 🏪 Shop Commands
| Command | Description |
|---------|-------------|
| `/shop` | View all available items |
| `/buy <item> [quantity]` | Buy item from shop |
| `/sell <item> [quantity]` | Sell item for 70% price |
| `/inventory [user]` | View inventory |

### 🎰 Gambling Commands
| Command | Description | Multiplier |
|---------|-------------|------------|
| `/coinflip <bet> <choice>` | Bet on heads or tails | 2x |
| `/slots <bet>` | Spin the slot machine | 2x-10x |
| `/dice <bet> <guess>` | Guess the dice roll | 6x |
| `/blackjack <bet>` | Play against dealer | 2x |

### ⚙️ Admin Commands (Requires Administrator)
| Command | Description |
|---------|-------------|
| `/addmoney <user> <amount>` | Add money to user wallet |
| `/removemoney <user> <amount>` | Remove money from user |
| `/resetuser <user>` | Reset user economy data |
| `/setbank <user> <limit>` | Set user bank limit |
| `/econostats` | View server statistics |
| `/help` | Show all commands |

---

## 🎮 How to Play

### Getting Started
1. Use `/work` every hour to earn money
2. Use `/daily` once per day for bigger rewards
3. Build up your daily streak for bonus money!

### Making Money
- **Work**: Earn $90-$500 per hour
- **Daily**: Base $500 + streak bonus (up to $1,000)
- **Gambling**: Risk money for big multipliers

### Managing Money
- Keep money in wallet for quick access
- Store money in bank for safety (has limits)
- Bank protects from gambling losses

### Shopping
1. Check `/shop` for available items
2. Use `/buy <item>` to purchase
3. View collection with `/inventory`
4. Sell items with `/sell <item>` for 70% back

### Competing
- Check `/leaderboard` to see rankings
- Compete with friends for #1 spot
- Track your total wealth (wallet + bank)

---

## 📁 Project Structure

```
discord-economy-bot/
├── main.py                 # Bot entry point
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
├── .gitignore            # Git ignore rules
├── README.md             # This file
│
├── cogs/                 # Command modules
│   ├── __init__.py
│   ├── economy.py        # Economy commands
│   ├── shop.py          # Shop & inventory
│   ├── gambling.py      # Gambling games
│   └── admin.py         # Admin commands
│
└── utils/               # Utilities
    ├── __init__.py
    └── database.py      # Database handler
```

---

## 🛠️ Customization

### Adding Shop Items
Edit `cogs/shop.py` → `DEFAULT_ITEMS`:
```python
DEFAULT_ITEMS = [
    ("item_name", price, "Description", "emoji"),
    ("sword", 1000, "A sharp sword ⚔️", "⚔️"),
    # Add more...
]
```

### Changing Reward Amounts
**Daily Rewards** (`cogs/economy.py`):
```python
base_reward = 500  # Change base amount
streak_bonus = min(streak * 50, 1000)  # Change bonus calculation
```

**Work Rewards** (`cogs/economy.py`):
```python
jobs = [
    ("job_name", min_earnings, max_earnings),
    # Modify existing or add new jobs
]
```

### Adjusting Bank Limits
**Default Limit** (`utils/database.py`):
```python
bank_limit INTEGER DEFAULT 5000  # Change default limit
```

**Per-User Limits**: Use `/setbank <user> <limit>` command

### Adding New Gambling Games
Create new command in `cogs/gambling.py`:
```python
@app_commands.command(name="newgame", description="Your game")
async def newgame(self, interaction: discord.Interaction, bet: int):
    # Your game logic
    pass
```

---

## 🐛 Troubleshooting

### Bot doesn't respond to slash commands
- Wait 5-10 minutes for Discord to sync commands
- Make sure bot has proper permissions
- Check that intents are enabled in Developer Portal

### "DISCORD_TOKEN not found" error
- Ensure `.env` file exists (not `.env.example`)
- Check token is correctly pasted
- No quotes needed around token

### Database errors
- Delete `economy.db` file
- Restart bot to recreate database
- Check write permissions in directory

### Commands not appearing
- Reinvite bot with `applications.commands` scope
- Wait for command sync to complete
- Check bot has proper server permissions

---

## 💡 Tips & Best Practices

### For Users
- 💾 Always keep money in bank for safety
- 🔥 Maintain daily streaks for maximum rewards
- 🎰 Don't gamble more than you can afford to lose
- 📈 Check leaderboard to track progress

### For Admins
- 📊 Use `/econostats` to monitor economy
- 🏦 Adjust bank limits for balance
- 💰 Be careful with `/addmoney` to avoid inflation
- 🔄 Use `/resetuser` sparingly

### For Developers
- 📦 Cogs are modular - easy to add/remove
- 🗄️ Database is SQLite - simple and portable
- 🎨 Embeds follow consistent color scheme
- ✅ Error handling is built-in

---

## 📊 Database Schema

### Users Table
```sql
user_id (PK)      - Discord user ID
balance           - Wallet money
bank              - Bank money
bank_limit        - Max bank capacity
daily_streak      - Consecutive daily claims
last_daily        - Last daily claim timestamp
last_work         - Last work timestamp
total_earned      - Lifetime earnings
total_spent       - Lifetime spending
```

### Inventory Table
```sql
user_id, item_name (PK) - User + item combo
quantity                - Number owned
```

### Shop Items Table
```sql
item_name (PK) - Item identifier
price          - Purchase cost
description    - Item description
emoji          - Display emoji
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests
- 📖 Improve documentation

---

## 📋 License

This project is open source and available for free use and modification.

---

## 🌟 Credits

Built with ❤️ using:
- [discord.py](https://github.com/Rapptz/discord.py)
- [aiosqlite](https://github.com/omnilib/aiosqlite)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## 📞 Support

Need help? Here's what to do:
1. ✅ Read this README carefully
2. ✅ Check the troubleshooting section
3. ✅ Verify all dependencies are installed
4. ✅ Ensure bot token and permissions are correct

---

<div align="center">

**Enjoy your economy bot!** 🎉

Made for Discord servers | Perfect for community engagement

[⬆ Back to Top](#-discord-economy-bot)

</div>
