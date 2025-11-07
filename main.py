import discord
from discord.ext import commands
import asyncio
import logging
from typing import Optional

# ============================================
# ENTERPRISE BOT CONFIGURATION
# ============================================

class Config:
    """Enterprise-level bot configuration - Edit these values"""
    
    # ========== CORE SETTINGS ==========
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    BOT_PREFIX = "$"  # Fallback only, slash commands are primary
    
    # Bot Status
    STATUS_TYPE = discord.ActivityType.watching
    STATUS_MESSAGE = "your economy | /help"
    
    # Logging Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    LOG_LEVEL = logging.INFO
    
    # ========== DATABASE SETTINGS ==========
    DATABASE_NAME = "economy.db"
    AUTO_BACKUP = True
    BACKUP_INTERVAL_HOURS = 24
    
    # ========== ECONOMY SETTINGS ==========
    STARTING_WALLET_BALANCE = 0
    STARTING_BANK_BALANCE = 0
    DEFAULT_BANK_LIMIT = 10000
    
    DAILY_BASE_REWARD = 500
    DAILY_STREAK_BONUS = 50  # Per day
    MAX_STREAK_BONUS = 2000
    DAILY_COOLDOWN_HOURS = 24
    
    WORK_COOLDOWN_HOURS = 1
    WORK_MIN_EARNINGS = 100
    WORK_MAX_EARNINGS = 500
    PASSIVE_INCOME_ENABLED = False
    PASSIVE_INCOME_RATE = 0.001  # 0.1% per hour of bank balance
    TAX_ENABLED = False
    TRANSACTION_TAX_RATE = 0.02
    
    # ========== SHOP SETTINGS ==========
    SHOP_CATEGORIES = {
        "food": {"emoji": "🍔", "description": "Delicious food items"},
        "vehicles": {"emoji": "🚗", "description": "Transportation"},
        "properties": {"emoji": "🏠", "description": "Real estate"},
        "collectibles": {"emoji": "💎", "description": "Rare collectibles"},
        "electronics": {"emoji": "💻", "description": "Tech items"},
        "luxury": {"emoji": "👑", "description": "Luxury goods"},
        "weapons": {"emoji": "⚔️", "description": "Weapons and armor"},
        "pets": {"emoji": "🐕", "description": "Pets and companions"}
    }
    SHOP_ITEMS = [
        ("cookie", 50, "A delicious chocolate chip cookie", "🍪", "food", -1, None, 0),
        ("pizza", 150, "A hot slice of pepperoni pizza", "🍕", "food", -1, None, 0),
        ("burger", 200, "A juicy cheeseburger", "🍔", "food", -1, None, 0),
        ("sushi", 300, "Fresh salmon sushi roll", "🍣", "food", -1, None, 0),
        ("cake", 500, "A fancy birthday cake", "🎂", "food", -1, None, 0),
        ("phone", 1000, "Latest smartphone", "📱", "electronics", -1, None, 0),
        ("laptop", 5000, "High-performance laptop", "💻", "electronics", -1, None, 5),
        ("gaming_pc", 15000, "Ultimate gaming setup", "🖥️", "electronics", -1, None, 10),
        ("smartwatch", 2500, "Fitness smartwatch", "⌚", "electronics", -1, None, 3),
        ("bicycle", 500, "A reliable bicycle", "🚲", "vehicles", -1, None, 0),
        ("motorcycle", 10000, "Speedy motorcycle", "🏍️", "vehicles", -1, None, 5),
        ("car", 50000, "Luxury sedan", "🚗", "vehicles", -1, None, 10),
        ("sports_car", 150000, "High-end sports car", "🏎️", "vehicles", 10, None, 20),
        ("yacht", 1000000, "Private yacht", "🛥️", "vehicles", 3, None, 50),
        ("apartment", 100000, "Downtown apartment", "🏢", "properties", -1, None, 15),
        ("house", 500000, "Suburban house", "🏠", "properties", -1, None, 25),
        ("mansion", 2000000, "Luxury mansion", "🏰", "properties", 5, None, 40),
        ("island", 10000000, "Private island", "🏝️", "properties", 1, None, 75),
        ("trophy", 10000, "Golden trophy", "🏆", "collectibles", -1, None, 5),
        ("gem", 25000, "Rare gemstone", "💎", "collectibles", -1, None, 10),
        ("painting", 50000, "Famous artwork", "🖼️", "collectibles", 20, None, 15),
        ("antique", 100000, "Ancient artifact", "🏺", "collectibles", 10, None, 20),
        ("crown", 100000, "Royal crown", "👑", "luxury", 5, None, 30),
        ("ring", 75000, "Diamond ring", "💍", "luxury", -1, None, 20),
        ("watch", 150000, "Luxury timepiece", "⌚", "luxury", 15, None, 25),
        ("sword", 5000, "Steel sword", "⚔️", "weapons", -1, None, 8),
        ("shield", 3000, "Protective shield", "🛡️", "weapons", -1, None, 8),
        ("dog", 2000, "Loyal companion", "🐕", "pets", -1, None, 5),
        ("cat", 1500, "Independent feline", "🐈", "pets", -1, None, 5),
        ("parrot", 5000, "Talking parrot", "🦜", "pets", -1, None, 10),
        ("dragon", 500000, "Legendary dragon", "🐉", "pets", 2, None, 50),
    ]
    SELL_PRICE_MULTIPLIER = 0.70
    SELL_PRICE_MULTIPLIER_VIP = 0.85
    ALLOW_ITEM_TRADING = True
    ALLOW_GIFTING = True
    REQUIRE_ROLE_FOR_PREMIUM_ITEMS = False
    
    # ========== GAMBLING SETTINGS ==========
    COINFLIP_MIN_BET = 10
    COINFLIP_MAX_BET = 100000
    COINFLIP_MULTIPLIER = 2.0
    SLOTS_MIN_BET = 50
    SLOTS_MAX_BET = 50000
    SLOTS_MULTIPLIERS = {"three_match": 5.0, "diamond": 10.0, "seven": 7.0, "two_match": 2.0}
    DICE_MIN_BET = 10
    DICE_MAX_BET = 25000
    DICE_MULTIPLIER = 6.0
    BLACKJACK_MIN_BET = 100
    BLACKJACK_MAX_BET = 100000
    BLACKJACK_MULTIPLIER = 2.0
    
    # ========== LEVELING SYSTEM ==========
    LEVELING_ENABLED = True
    XP_PER_MESSAGE = 5
    XP_PER_COMMAND = 10
    XP_PER_WORK = 15
    XP_PER_DAILY = 25
    LEVEL_UP_REWARDS = {5: 1000, 10: 5000, 25: 25000, 50: 100000, 75: 500000, 100: 2000000}
    
    # ========== MODERATION SETTINGS ==========
    MAX_COMMANDS_PER_MINUTE = 30
    TRANSACTION_LOG_CHANNEL = None
    ECONOMY_LOG_CHANNEL = None
    
    # ========== PREMIUM/VIP SETTINGS ==========
    VIP_ROLE_ID = None
    VIP_BENEFITS = {"daily_multiplier": 1.5, "work_multiplier": 1.25, "sell_bonus": 0.15, "no_transaction_tax": True, "exclusive_items": True}
    
    DOUBLE_XP_EVENT = False
    DOUBLE_MONEY_EVENT = False
    SHOP_SALE_EVENT = False
    
    ENABLE_RATE_LIMITING = True
    MAX_TRANSACTION_AMOUNT = 10000000
    MAX_GIFT_AMOUNT = 100000
    REQUIRE_ADMIN_APPROVAL_ABOVE = 5000000

# ============================================
# BOT CLASS
# ============================================

class EconomyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix=Config.BOT_PREFIX, intents=intents, help_command=None)
        self.config = Config
        self.setup_logging()
        self.stats = {"commands_executed": 0, "transactions_processed": 0, "total_money_circulated": 0}
    def setup_logging(self):
        logging.basicConfig(level=Config.LOG_LEVEL, format='%(asctime)s | %(levelname)s | %(name)s | %(message)s', handlers=[logging.FileHandler('bot.log', encoding='utf-8'), logging.StreamHandler()])
        self.logger = logging.getLogger('EconomyBot')
    async def setup_hook(self):
        cogs = ['cogs.economy', 'cogs.shop', 'cogs.gambling', 'cogs.admin', 'cogs.trading', 'cogs.levels']
        for cog in cogs:
            try:
                await self.load_extension(cog)
                self.logger.info(f"✅ Loaded {cog}")
            except Exception as e:
                self.logger.error(f"❌ Failed to load {cog}: {e}")
        self.logger.info("⏳ Syncing slash commands...")
        try:
            await self.tree.sync()
            self.logger.info("✅ Slash commands synced!")
        except Exception as e:
            self.logger.error(f"❌ Failed to sync commands: {e}")
    async def on_ready(self):
        self.logger.info("="*60)
        self.logger.info(f"✅ Bot Ready: {self.user} (ID: {self.user.id})")
        self.logger.info(f"📊 Servers: {len(self.guilds)}")
        self.logger.info(f"👥 Users: {len(self.users)}")
        self.logger.info("="*60)
        await self.change_presence(activity=discord.Activity(type=Config.STATUS_TYPE, name=Config.STATUS_MESSAGE), status=discord.Status.online)
    async def on_message(self, message):
        pass
    async def on_command(self, ctx):
        pass
async def main():
    print("🚀 Enterprise Economy Bot Starting...")
    print("="*60)
    if Config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or not Config.BOT_TOKEN:
        print("❌ ERROR: Bot token not configured!")
        print("⚠️  Edit main.py and set BOT_TOKEN in the Config class")
        print("🔑 Get token from: https://discord.com/developers/applications")
        return
    bot = EconomyBot()
    try:
        async with bot:
            await bot.start(Config.BOT_TOKEN)
    except discord.LoginFailure:
        print("❌ ERROR: Invalid bot token!")
    except Exception as e:
        print(f"❌ ERROR: {e}")
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
