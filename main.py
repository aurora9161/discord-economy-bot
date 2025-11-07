import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EconomyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix="!",  # Fallback prefix (slash commands are primary)
            intents=intents,
            help_command=None
        )
        
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
        
        # Sync commands with Discord
        await self.tree.sync()
        print("✅ Commands synced with Discord")
    
    async def on_ready(self):
        print(f"\n{'='*50}")
        print(f"Bot is ready! Logged in as {self.user}")
        print(f"Bot ID: {self.user.id}")
        print(f"{'='*50}\n")
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="your economy | /help"
            )
        )

async def main():
    bot = EconomyBot()
    
    # Get token from environment variable
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ Error: DISCORD_TOKEN not found in .env file!")
        return
    
    async with bot:
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
