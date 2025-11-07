import discord
from discord import app_commands
from discord.ext import commands
from utils.database import db

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="addmoney", description="[ADMIN] Add money to a user")
    @app_commands.checks.has_permissions(administrator=True)
    async def addmoney(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        """Add money to user"""
        if amount <= 0:
            await interaction.response.send_message("❌ Amount must be positive!", ephemeral=True)
            return
        
        await db.update_balance(user.id, amount)
        
        embed = discord.Embed(
            title="💰 Money Added",
            description=f"Added **${amount:,}** to {user.mention}'s wallet!",
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="removemoney", description="[ADMIN] Remove money from a user")
    @app_commands.checks.has_permissions(administrator=True)
    async def removemoney(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        """Remove money from user"""
        if amount <= 0:
            await interaction.response.send_message("❌ Amount must be positive!", ephemeral=True)
            return
        
        user_data = await db.get_user(user.id)
        wallet = user_data[1]
        
        if amount > wallet:
            await interaction.response.send_message(
                f"❌ {user.mention} only has **${wallet:,}** in their wallet!",
                ephemeral=True
            )
            return
        
        await db.update_balance(user.id, -amount)
        
        embed = discord.Embed(
            title="💸 Money Removed",
            description=f"Removed **${amount:,}** from {user.mention}'s wallet!",
            color=discord.Color.red()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="resetuser", description="[ADMIN] Reset a user's economy data")
    @app_commands.checks.has_permissions(administrator=True)
    async def resetuser(self, interaction: discord.Interaction, user: discord.Member):
        """Reset user economy"""
        await db.db.execute("DELETE FROM users WHERE user_id = ?", (user.id,))
        await db.db.execute("DELETE FROM inventory WHERE user_id = ?", (user.id,))
        await db.db.commit()
        
        embed = discord.Embed(
            title="🔄 User Reset",
            description=f"Reset all economy data for {user.mention}!",
            color=discord.Color.orange()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="setbank", description="[ADMIN] Set a user's bank limit")
    @app_commands.checks.has_permissions(administrator=True)
    async def setbank(self, interaction: discord.Interaction, user: discord.Member, limit: int):
        """Set bank limit"""
        if limit < 0:
            await interaction.response.send_message("❌ Limit cannot be negative!", ephemeral=True)
            return
        
        await db.get_user(user.id)  # Ensure user exists
        await db.db.execute(
            "UPDATE users SET bank_limit = ? WHERE user_id = ?",
            (limit, user.id)
        )
        await db.db.commit()
        
        embed = discord.Embed(
            title="🏦 Bank Limit Updated",
            description=f"Set {user.mention}'s bank limit to **${limit:,}**!",
            color=discord.Color.blue()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="econostats", description="[ADMIN] View economy statistics")
    @app_commands.checks.has_permissions(administrator=True)
    async def econostats(self, interaction: discord.Interaction):
        """Economy stats"""
        async with db.db.execute("SELECT COUNT(*), SUM(balance + bank), AVG(balance + bank) FROM users") as cursor:
            stats = await cursor.fetchone()
        
        total_users = stats[0]
        total_money = stats[1] or 0
        avg_money = stats[2] or 0
        
        embed = discord.Embed(
            title="📊 Economy Statistics",
            color=discord.Color.purple()
        )
        
        embed.add_field(name="👥 Total Users", value=f"**{total_users:,}**", inline=True)
        embed.add_field(name="💰 Total Money", value=f"**${total_money:,}**", inline=True)
        embed.add_field(name="📈 Average Wealth", value=f"**${int(avg_money):,}**", inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="help", description="View all available commands")
    async def help(self, interaction: discord.Interaction):
        """Help command"""
        embed = discord.Embed(
            title="📚 Economy Bot Commands",
            description="Here are all available commands:",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="💰 Economy",
            value=(
                "`/balance` - Check your balance\n"
                "`/daily` - Claim daily reward\n"
                "`/work` - Work for money\n"
                "`/deposit` - Deposit to bank\n"
                "`/withdraw` - Withdraw from bank\n"
                "`/leaderboard` - View top users"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🏪 Shop",
            value=(
                "`/shop` - View the shop\n"
                "`/buy` - Buy an item\n"
                "`/sell` - Sell an item\n"
                "`/inventory` - View inventory"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🎰 Gambling",
            value=(
                "`/coinflip` - Flip a coin\n"
                "`/slots` - Play slots\n"
                "`/dice` - Roll dice\n"
                "`/blackjack` - Play blackjack"
            ),
            inline=False
        )
        
        embed.add_field(
            name="⚙️ Admin",
            value=(
                "`/addmoney` - Add money to user\n"
                "`/removemoney` - Remove money from user\n"
                "`/resetuser` - Reset user data\n"
                "`/setbank` - Set bank limit\n"
                "`/econostats` - Economy statistics"
            ),
            inline=False
        )
        
        embed.set_footer(text="Use /help to view this message again")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))
