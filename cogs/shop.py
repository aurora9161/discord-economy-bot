import discord
from discord import app_commands
from discord.ext import commands
from utils.database import db
from datetime import datetime

# Default shop items
DEFAULT_ITEMS = [
    ("cookie", 50, "A delicious cookie 🍪", "🍪"),
    ("pizza", 150, "A hot slice of pizza 🍕", "🍕"),
    ("laptop", 5000, "A powerful laptop 💻", "💻"),
    ("car", 50000, "A fancy car 🚗", "🚗"),
    ("house", 500000, "Your dream house 🏠", "🏠"),
    ("trophy", 10000, "A shiny trophy 🏆", "🏆"),
    ("gem", 25000, "A rare gemstone 💎", "💎"),
    ("crown", 100000, "A royal crown 👑", "👑"),
]

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def cog_load(self):
        """Initialize shop with default items"""
        for item in DEFAULT_ITEMS:
            await db.db.execute(
                "INSERT OR IGNORE INTO shop_items (item_name, price, description, emoji) VALUES (?, ?, ?, ?)",
                item
            )
        await db.db.commit()
    
    @app_commands.command(name="shop", description="View the shop")
    async def shop(self, interaction: discord.Interaction):
        """Display shop"""
        async with db.db.execute("SELECT * FROM shop_items ORDER BY price") as cursor:
            items = await cursor.fetchall()
        
        embed = discord.Embed(
            title="🏪 Shop",
            description="Buy items with your hard-earned money!",
            color=discord.Color.purple(),
            timestamp=datetime.utcnow()
        )
        
        for item in items:
            name, price, description, emoji = item
            embed.add_field(
                name=f"{emoji} {name.title()}",
                value=f"{description}\n**Price:** ${price:,}",
                inline=True
            )
        
        embed.set_footer(text="Use /buy <item> to purchase")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="buy", description="Buy an item from the shop")
    async def buy(self, interaction: discord.Interaction, item: str, quantity: int = 1):
        """Buy item"""
        if quantity <= 0:
            await interaction.response.send_message("❌ Quantity must be positive!", ephemeral=True)
            return
        
        # Get item from shop
        async with db.db.execute(
            "SELECT * FROM shop_items WHERE LOWER(item_name) = LOWER(?)",
            (item,)
        ) as cursor:
            shop_item = await cursor.fetchone()
        
        if not shop_item:
            await interaction.response.send_message(f"❌ Item **{item}** not found in shop!", ephemeral=True)
            return
        
        item_name, price, description, emoji = shop_item
        total_cost = price * quantity
        
        # Check user balance
        user_data = await db.get_user(interaction.user.id)
        wallet = user_data[1]
        
        if wallet < total_cost:
            await interaction.response.send_message(
                f"❌ You need **${total_cost:,}** but only have **${wallet:,}**!",
                ephemeral=True
            )
            return
        
        # Process purchase
        await db.update_balance(interaction.user.id, -total_cost)
        await db.add_item(interaction.user.id, item_name, quantity)
        
        # Update stats
        await db.db.execute(
            "UPDATE users SET total_spent = total_spent + ? WHERE user_id = ?",
            (total_cost, interaction.user.id)
        )
        await db.db.commit()
        
        embed = discord.Embed(
            title="✅ Purchase Successful!",
            description=f"You bought **{quantity}x {emoji} {item_name.title()}** for **${total_cost:,}**!",
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="sell", description="Sell an item from your inventory")
    async def sell(self, interaction: discord.Interaction, item: str, quantity: int = 1):
        """Sell item"""
        if quantity <= 0:
            await interaction.response.send_message("❌ Quantity must be positive!", ephemeral=True)
            return
        
        # Get item from shop (to get price)
        async with db.db.execute(
            "SELECT * FROM shop_items WHERE LOWER(item_name) = LOWER(?)",
            (item,)
        ) as cursor:
            shop_item = await cursor.fetchone()
        
        if not shop_item:
            await interaction.response.send_message(f"❌ Item **{item}** doesn't exist!", ephemeral=True)
            return
        
        item_name, price, description, emoji = shop_item
        sell_price = int(price * 0.7)  # Sell for 70% of buy price
        total_earnings = sell_price * quantity
        
        # Remove from inventory
        success = await db.remove_item(interaction.user.id, item_name, quantity)
        
        if not success:
            await interaction.response.send_message(
                f"❌ You don't have **{quantity}x {item_name}** in your inventory!",
                ephemeral=True
            )
            return
        
        # Add money
        await db.update_balance(interaction.user.id, total_earnings)
        
        embed = discord.Embed(
            title="✅ Sale Successful!",
            description=f"You sold **{quantity}x {emoji} {item_name.title()}** for **${total_earnings:,}**!",
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="inventory", description="View your inventory or another user's")
    async def inventory(self, interaction: discord.Interaction, user: discord.Member = None):
        """View inventory"""
        target = user or interaction.user
        items = await db.get_inventory(target.id)
        
        embed = discord.Embed(
            title=f"🎒 {target.display_name}'s Inventory",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        if not items:
            embed.description = "Empty inventory!"
        else:
            inventory_text = ""
            for item_name, quantity in items:
                # Get emoji from shop
                async with db.db.execute(
                    "SELECT emoji FROM shop_items WHERE item_name = ?",
                    (item_name,)
                ) as cursor:
                    result = await cursor.fetchone()
                    emoji = result[0] if result else "📦"
                
                inventory_text += f"{emoji} **{item_name.title()}** x{quantity}\n"
            
            embed.description = inventory_text
        
        embed.set_thumbnail(url=target.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Shop(bot))
