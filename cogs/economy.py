import discord
from discord import app_commands
from discord.ext import commands
from utils.database import db
from datetime import datetime, timedelta
import random

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="balance", description="Check your balance or another user's balance")
    async def balance(self, interaction: discord.Interaction, user: discord.Member = None):
        """Check balance"""
        target = user or interaction.user
        user_data = await db.get_user(target.id)
        
        wallet = user_data[1]
        bank = user_data[2]
        bank_limit = user_data[3]
        total = wallet + bank
        
        embed = discord.Embed(
            title=f"💰 {target.display_name}'s Balance",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="👛 Wallet", value=f"**${wallet:,}**", inline=True)
        embed.add_field(name="🏦 Bank", value=f"**${bank:,}** / ${bank_limit:,}", inline=True)
        embed.add_field(name="💎 Total", value=f"**${total:,}**", inline=True)
        
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.set_footer(text=f"Requested by {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="daily", description="Claim your daily reward")
    async def daily(self, interaction: discord.Interaction):
        """Daily reward"""
        user_data = await db.get_user(interaction.user.id)
        last_daily = user_data[5]
        streak = user_data[4]
        
        now = datetime.utcnow()
        
        if last_daily:
            last_daily_dt = datetime.fromisoformat(last_daily)
            time_since = now - last_daily_dt
            
            if time_since < timedelta(days=1):
                time_left = timedelta(days=1) - time_since
                hours = int(time_left.total_seconds() // 3600)
                minutes = int((time_left.total_seconds() % 3600) // 60)
                
                embed = discord.Embed(
                    title="⏰ Daily Reward Cooldown",
                    description=f"You already claimed your daily reward!\nCome back in **{hours}h {minutes}m**",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            # Check if streak continues
            if time_since < timedelta(days=2):
                streak += 1
            else:
                streak = 1
        else:
            streak = 1
        
        # Calculate reward with streak bonus
        base_reward = 500
        streak_bonus = min(streak * 50, 1000)  # Max 1000 bonus
        total_reward = base_reward + streak_bonus
        
        await db.update_balance(interaction.user.id, total_reward)
        await db.db.execute(
            "UPDATE users SET daily_streak = ?, last_daily = ?, total_earned = total_earned + ? WHERE user_id = ?",
            (streak, now.isoformat(), total_reward, interaction.user.id)
        )
        await db.db.commit()
        
        embed = discord.Embed(
            title="🎁 Daily Reward Claimed!",
            description=f"You received **${total_reward:,}**!",
            color=discord.Color.gold()
        )
        
        embed.add_field(name="🔥 Streak", value=f"**{streak}** day(s)", inline=True)
        embed.add_field(name="💰 Bonus", value=f"**${streak_bonus:,}**", inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="work", description="Work for money")
    async def work(self, interaction: discord.Interaction):
        """Work command"""
        user_data = await db.get_user(interaction.user.id)
        last_work = user_data[6]
        
        now = datetime.utcnow()
        
        if last_work:
            last_work_dt = datetime.fromisoformat(last_work)
            time_since = now - last_work_dt
            
            if time_since < timedelta(hours=1):
                time_left = timedelta(hours=1) - time_since
                minutes = int(time_left.total_seconds() // 60)
                seconds = int(time_left.total_seconds() % 60)
                
                embed = discord.Embed(
                    title="⏰ Work Cooldown",
                    description=f"You're tired! Rest for **{minutes}m {seconds}s**",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        
        # Random work scenarios
        jobs = [
            ("delivered pizzas", 150, 300),
            ("fixed computers", 200, 400),
            ("walked dogs", 100, 250),
            ("washed cars", 120, 280),
            ("tutored students", 180, 350),
            ("cleaned houses", 140, 320),
            ("mowed lawns", 110, 270),
            ("coded a website", 250, 500),
            ("made coffee", 90, 200),
            ("delivered packages", 160, 340)
        ]
        
        job = random.choice(jobs)
        earnings = random.randint(job[1], job[2])
        
        await db.update_balance(interaction.user.id, earnings)
        await db.db.execute(
            "UPDATE users SET last_work = ?, total_earned = total_earned + ? WHERE user_id = ?",
            (now.isoformat(), earnings, interaction.user.id)
        )
        await db.db.commit()
        
        embed = discord.Embed(
            title="💼 Work Complete!",
            description=f"You {job[0]} and earned **${earnings:,}**!",
            color=discord.Color.blue()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="deposit", description="Deposit money to your bank")
    async def deposit(self, interaction: discord.Interaction, amount: str):
        """Deposit money"""
        user_data = await db.get_user(interaction.user.id)
        wallet = user_data[1]
        bank = user_data[2]
        bank_limit = user_data[3]
        
        # Handle 'all' or 'max'
        if amount.lower() in ['all', 'max']:
            amount = min(wallet, bank_limit - bank)
        else:
            try:
                amount = int(amount)
            except ValueError:
                await interaction.response.send_message("❌ Invalid amount!", ephemeral=True)
                return
        
        if amount <= 0:
            await interaction.response.send_message("❌ Amount must be positive!", ephemeral=True)
            return
        
        if amount > wallet:
            await interaction.response.send_message("❌ You don't have enough money in your wallet!", ephemeral=True)
            return
        
        if bank + amount > bank_limit:
            await interaction.response.send_message(f"❌ Your bank limit is ${bank_limit:,}! You can only deposit ${bank_limit - bank:,} more.", ephemeral=True)
            return
        
        await db.update_balance(interaction.user.id, -amount, "balance")
        await db.update_balance(interaction.user.id, amount, "bank")
        
        embed = discord.Embed(
            title="🏦 Deposit Successful",
            description=f"Deposited **${amount:,}** to your bank!",
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="withdraw", description="Withdraw money from your bank")
    async def withdraw(self, interaction: discord.Interaction, amount: str):
        """Withdraw money"""
        user_data = await db.get_user(interaction.user.id)
        bank = user_data[2]
        
        # Handle 'all' or 'max'
        if amount.lower() in ['all', 'max']:
            amount = bank
        else:
            try:
                amount = int(amount)
            except ValueError:
                await interaction.response.send_message("❌ Invalid amount!", ephemeral=True)
                return
        
        if amount <= 0:
            await interaction.response.send_message("❌ Amount must be positive!", ephemeral=True)
            return
        
        if amount > bank:
            await interaction.response.send_message("❌ You don't have enough money in your bank!", ephemeral=True)
            return
        
        await db.update_balance(interaction.user.id, amount, "balance")
        await db.update_balance(interaction.user.id, -amount, "bank")
        
        embed = discord.Embed(
            title="💰 Withdrawal Successful",
            description=f"Withdrew **${amount:,}** from your bank!",
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="leaderboard", description="View the richest users")
    async def leaderboard(self, interaction: discord.Interaction):
        """Leaderboard"""
        top_users = await db.get_leaderboard(10)
        
        embed = discord.Embed(
            title="🏆 Economy Leaderboard",
            description="Top 10 richest users",
            color=discord.Color.gold(),
            timestamp=datetime.utcnow()
        )
        
        leaderboard_text = ""
        for idx, (user_id, total) in enumerate(top_users, 1):
            user = self.bot.get_user(user_id)
            name = user.display_name if user else "Unknown User"
            
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"`{idx}.`"
            leaderboard_text += f"{medal} **{name}** - ${total:,}\n"
        
        embed.description = leaderboard_text or "No users yet!"
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))
    await db.connect()
