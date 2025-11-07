import aiosqlite
import os

class Database:
    def __init__(self, db_name="economy.db"):
        self.db_name = db_name
    
    async def connect(self):
        """Connect to database and create tables"""
        self.db = await aiosqlite.connect(self.db_name)
        await self.create_tables()
    
    async def create_tables(self):
        """Create necessary tables"""
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 0,
                bank INTEGER DEFAULT 0,
                bank_limit INTEGER DEFAULT 5000,
                daily_streak INTEGER DEFAULT 0,
                last_daily TEXT,
                last_work TEXT,
                total_earned INTEGER DEFAULT 0,
                total_spent INTEGER DEFAULT 0
            )
        """)
        
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                user_id INTEGER,
                item_name TEXT,
                quantity INTEGER DEFAULT 1,
                PRIMARY KEY (user_id, item_name)
            )
        """)
        
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS shop_items (
                item_name TEXT PRIMARY KEY,
                price INTEGER,
                description TEXT,
                emoji TEXT
            )
        """)
        
        await self.db.commit()
    
    async def get_user(self, user_id):
        """Get user data, create if doesn't exist"""
        async with self.db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            user = await cursor.fetchone()
            
            if not user:
                await self.db.execute(
                    "INSERT INTO users (user_id) VALUES (?)", (user_id,)
                )
                await self.db.commit()
                return await self.get_user(user_id)
            
            return user
    
    async def update_balance(self, user_id, amount, balance_type="balance"):
        """Update user balance (wallet or bank)"""
        user = await self.get_user(user_id)
        
        if balance_type == "balance":
            new_amount = user[1] + amount
            await self.db.execute(
                "UPDATE users SET balance = ? WHERE user_id = ?",
                (new_amount, user_id)
            )
        elif balance_type == "bank":
            new_amount = user[2] + amount
            await self.db.execute(
                "UPDATE users SET bank = ? WHERE user_id = ?",
                (new_amount, user_id)
            )
        
        await self.db.commit()
        return new_amount
    
    async def add_item(self, user_id, item_name, quantity=1):
        """Add item to user inventory"""
        async with self.db.execute(
            "SELECT quantity FROM inventory WHERE user_id = ? AND item_name = ?",
            (user_id, item_name)
        ) as cursor:
            result = await cursor.fetchone()
            
            if result:
                new_quantity = result[0] + quantity
                await self.db.execute(
                    "UPDATE inventory SET quantity = ? WHERE user_id = ? AND item_name = ?",
                    (new_quantity, user_id, item_name)
                )
            else:
                await self.db.execute(
                    "INSERT INTO inventory (user_id, item_name, quantity) VALUES (?, ?, ?)",
                    (user_id, item_name, quantity)
                )
        
        await self.db.commit()
    
    async def remove_item(self, user_id, item_name, quantity=1):
        """Remove item from user inventory"""
        async with self.db.execute(
            "SELECT quantity FROM inventory WHERE user_id = ? AND item_name = ?",
            (user_id, item_name)
        ) as cursor:
            result = await cursor.fetchone()
            
            if not result or result[0] < quantity:
                return False
            
            new_quantity = result[0] - quantity
            
            if new_quantity <= 0:
                await self.db.execute(
                    "DELETE FROM inventory WHERE user_id = ? AND item_name = ?",
                    (user_id, item_name)
                )
            else:
                await self.db.execute(
                    "UPDATE inventory SET quantity = ? WHERE user_id = ? AND item_name = ?",
                    (new_quantity, user_id, item_name)
                )
            
            await self.db.commit()
            return True
    
    async def get_inventory(self, user_id):
        """Get user inventory"""
        async with self.db.execute(
            "SELECT item_name, quantity FROM inventory WHERE user_id = ?",
            (user_id,)
        ) as cursor:
            return await cursor.fetchall()
    
    async def get_leaderboard(self, limit=10):
        """Get top users by total wealth"""
        async with self.db.execute(
            "SELECT user_id, balance + bank as total FROM users ORDER BY total DESC LIMIT ?",
            (limit,)
        ) as cursor:
            return await cursor.fetchall()
    
    async def close(self):
        """Close database connection"""
        await self.db.close()

# Global database instance
db = Database()
