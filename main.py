import discord
from discord.ext import commands
import asyncio

# ============================================
# BOT CONFIGURATION - EDIT THESE VALUES
# ============================================

class Config:
    """Bot configuration - Edit these values before running"""
    
    # Discord Bot Token (Get from: https://discord.com/developers/applications)
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    
    # Bot Status Settings
    STATUS_TYPE = discord.ActivityType.watching  # watching, playing, listening, streaming
    STATUS_MESSAGE = "your economy | /help"
    
    # Database Settings
    DATABASE_NAME = "economy.db"
    
    # Default Economy Settings
    DEFAULT_BANK_LIMIT = 5000
    DAILY_BASE_REWARD = 500
    DAILY_STREAK_BONUS = 50  # Bonus per streak day
    MAX_STREAK_BONUS = 1000
    
    # Work Command Settings
    WORK_COOLDOWN_HOURS = 1
    WORK_MIN_EARNINGS = 90
    WORK_MAX_EARNINGS = 500
    
    # Shop Settings - Items format: (name, price, description, emoji)
    SHOP_ITEMS = [
        ("cookie", 50, "A delicious cookie 🍪", "🍪"),
        ("pizza", 150, "A hot slice of pizza 🍕", "🍕"),
        ("laptop", 5000, "A powerful laptop 💻", "💻"),
        ("car", 50000, "A fancy car 🚗", "🚗"),
        ("house", 500000, "Your dream house 🏠", "🏠"),
        ("trophy", 10000, "A shiny trophy 🏆", "🏆"),
        ("gem", 25000, "A rare gemstone 💎", "💎"),
        ("crown", 100000, "A royal crown 👑", "👑"),
    ]
    
    # Sell Price Multiplier (0.7 = 70% of original price)
    SELL_PRICE_MULTIPLIER = 0.7

# ============================================
# BOT CLASS - DO NOT EDIT BELOW UNLESS YOU KNOW WHAT YOU'RE DOING
# ============================================

class EconomyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(command_prefix="$", intents=intents, help_command=None)
        
        # Store config for access by cogs
        self.config = Config
        
    async def setup_hook(self):
        """Load all cogs"""
        cogs = [
            'cogs.economy',
            'cogs.shop',
            'cogs.gambling',
            'cogs.admin'
        ]
        
        for cog in cogs:
            try:
                await self.load_extension(cog)
                print(f"✅ Loaded {cog}")
            except Exception as e:
                print(f"❌ Failed to load {cog}: {e}")
        
        # Sync slash commands with Discord
        print("\n⏳ Syncing slash commands with Discord...")
        await self.tree.sync()
        print("✅ All slash commands synced!\n")
    
    async def on_ready(self):
        print(f"\n{'='*50}")
        print(f"✅ Bot is ready! Logged in as {self.user}")
        print(f"🆔 Bot ID: {self.user.id}")
        print(f"📁 Servers: {len(self.guilds)}")
        print(f"{'='*50}\n")
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=Config.STATUS_TYPE,
                name=Config.STATUS_MESSAGE
            )
        )
    
    async def on_command(self, ctx):
        """Block all prefix commands"""
        pass
    
    async def on_message(self, message):
        """Disable prefix command processing"""
        # Don't process any prefix commands
        pass

async def main():
    """Main bot startup function"""
    print("🤖 Discord Economy Bot Starting...\n")
    
    # Validate token
    if Config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or not Config.BOT_TOKEN:
        print("❌ ERROR: Bot token not configured!")
        print("⚠️  Please edit main.py and set your BOT_TOKEN in the Config class.")
        print("🔑 Get your token from: https://discord.com/developers/applications\n")
        return
    
    bot = EconomyBot()
    
    try:
        async with bot:
            await bot.start(Config.BOT_TOKEN)
    except discord.LoginFailure:
        print("❌ ERROR: Invalid bot token!")
        print("⚠️  Please check your BOT_TOKEN in the Config class.\n")
    except Exception as e:
        print(f"❌ ERROR: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())
