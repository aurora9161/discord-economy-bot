import discord
from discord import app_commands
from discord.ext import commands
from utils.database import db
import random

class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="coinflip", description="Flip a coin and bet money")
    @app_commands.describe(bet="Amount to bet", choice="Heads or Tails")
    @app_commands.choices(choice=[
        app_commands.Choice(name="Heads", value="heads"),
        app_commands.Choice(name="Tails", value="tails")
    ])
    async def coinflip(self, interaction: discord.Interaction, bet: int, choice: app_commands.Choice[str]):
        """Coinflip gambling"""
        if bet <= 0:
            await interaction.response.send_message("❌ Bet must be positive!", ephemeral=True)
            return
        
        user_data = await db.get_user(interaction.user.id)
        wallet = user_data[1]
        
        if bet > wallet:
            await interaction.response.send_message(f"❌ You only have **${wallet:,}**!", ephemeral=True)
            return
        
        # Flip coin
        result = random.choice(["heads", "tails"])
        won = result == choice.value
        
        if won:
            winnings = bet
            await db.update_balance(interaction.user.id, winnings)
            
            embed = discord.Embed(
                title="🪙 Coinflip - You Won!",
                description=f"The coin landed on **{result.upper()}**!\nYou won **${winnings:,}**!",
                color=discord.Color.green()
            )
        else:
            await db.update_balance(interaction.user.id, -bet)
            
            embed = discord.Embed(
                title="🪙 Coinflip - You Lost!",
                description=f"The coin landed on **{result.upper()}**!\nYou lost **${bet:,}**!",
                color=discord.Color.red()
            )
        
        embed.set_footer(text=f"You chose {choice.value}")
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="slots", description="Play the slot machine")
    async def slots(self, interaction: discord.Interaction, bet: int):
        """Slot machine"""
        if bet <= 0:
            await interaction.response.send_message("❌ Bet must be positive!", ephemeral=True)
            return
        
        user_data = await db.get_user(interaction.user.id)
        wallet = user_data[1]
        
        if bet > wallet:
            await interaction.response.send_message(f"❌ You only have **${wallet:,}**!", ephemeral=True)
            return
        
        # Slot symbols
        symbols = ["🍒", "🍋", "🍊", "🍇", "🔔", "💎", "7️⃣"]
        
        # Spin slots
        result = [random.choice(symbols) for _ in range(3)]
        
        # Calculate winnings
        if result[0] == result[1] == result[2]:
            if result[0] == "💎":
                multiplier = 10
            elif result[0] == "7️⃣":
                multiplier = 7
            else:
                multiplier = 5
            
            winnings = bet * multiplier
            await db.update_balance(interaction.user.id, winnings - bet)
            
            embed = discord.Embed(
                title="🎰 JACKPOT!",
                description=f"{result[0]} {result[1]} {result[2]}\n\nYou won **${winnings:,}**! ({multiplier}x)",
                color=discord.Color.gold()
            )
        elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
            winnings = bet * 2
            await db.update_balance(interaction.user.id, winnings - bet)
            
            embed = discord.Embed(
                title="🎰 You Won!",
                description=f"{result[0]} {result[1]} {result[2]}\n\nYou won **${winnings:,}**! (2x)",
                color=discord.Color.green()
            )
        else:
            await db.update_balance(interaction.user.id, -bet)
            
            embed = discord.Embed(
                title="🎰 You Lost!",
                description=f"{result[0]} {result[1]} {result[2]}\n\nYou lost **${bet:,}**!",
                color=discord.Color.red()
            )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="dice", description="Roll dice and bet on the outcome")
    async def dice(self, interaction: discord.Interaction, bet: int, guess: int):
        """Dice gambling"""
        if bet <= 0:
            await interaction.response.send_message("❌ Bet must be positive!", ephemeral=True)
            return
        
        if guess < 1 or guess > 6:
            await interaction.response.send_message("❌ Guess must be between 1 and 6!", ephemeral=True)
            return
        
        user_data = await db.get_user(interaction.user.id)
        wallet = user_data[1]
        
        if bet > wallet:
            await interaction.response.send_message(f"❌ You only have **${wallet:,}**!", ephemeral=True)
            return
        
        # Roll dice
        result = random.randint(1, 6)
        
        dice_emoji = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
        
        if result == guess:
            winnings = bet * 6
            await db.update_balance(interaction.user.id, winnings - bet)
            
            embed = discord.Embed(
                title="🎲 Perfect Guess!",
                description=f"The dice rolled **{dice_emoji[result-1]}**!\nYou won **${winnings:,}**! (6x)",
                color=discord.Color.gold()
            )
        else:
            await db.update_balance(interaction.user.id, -bet)
            
            embed = discord.Embed(
                title="🎲 Wrong Guess!",
                description=f"The dice rolled **{dice_emoji[result-1]}**!\nYou guessed {dice_emoji[guess-1]}\nYou lost **${bet:,}**!",
                color=discord.Color.red()
            )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="blackjack", description="Play a game of blackjack")
    async def blackjack(self, interaction: discord.Interaction, bet: int):
        """Simple blackjack game"""
        if bet <= 0:
            await interaction.response.send_message("❌ Bet must be positive!", ephemeral=True)
            return
        
        user_data = await db.get_user(interaction.user.id)
        wallet = user_data[1]
        
        if bet > wallet:
            await interaction.response.send_message(f"❌ You only have **${wallet:,}**!", ephemeral=True)
            return
        
        # Deal cards
        player_hand = random.randint(15, 21)
        dealer_hand = random.randint(15, 21)
        
        if player_hand > 21:
            await db.update_balance(interaction.user.id, -bet)
            embed = discord.Embed(
                title="🎴 Blackjack - Bust!",
                description=f"Your hand: **{player_hand}**\nDealer's hand: **{dealer_hand}**\n\nYou busted! Lost **${bet:,}**!",
                color=discord.Color.red()
            )
        elif dealer_hand > 21 or player_hand > dealer_hand:
            winnings = bet * 2
            await db.update_balance(interaction.user.id, winnings - bet)
            embed = discord.Embed(
                title="🎴 Blackjack - You Won!",
                description=f"Your hand: **{player_hand}**\nDealer's hand: **{dealer_hand}**\n\nYou won **${winnings:,}**!",
                color=discord.Color.green()
            )
        elif player_hand == dealer_hand:
            embed = discord.Embed(
                title="🎴 Blackjack - Push!",
                description=f"Your hand: **{player_hand}**\nDealer's hand: **{dealer_hand}**\n\nIt's a tie! Your bet is returned.",
                color=discord.Color.blue()
            )
        else:
            await db.update_balance(interaction.user.id, -bet)
            embed = discord.Embed(
                title="🎴 Blackjack - You Lost!",
                description=f"Your hand: **{player_hand}**\nDealer's hand: **{dealer_hand}**\n\nYou lost **${bet:,}**!",
                color=discord.Color.red()
            )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Gambling(bot))
