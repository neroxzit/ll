from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import idle
from pyrogram.handlers import MessageHandler
from datetime import datetime
from colorama import Fore, Style
from pyrogram.raw.types import InputPeerSelf
from pyrogram.raw import functions, types

import sqlite3
import asyncio
import platform

def adapt_datetime(datetime_obj):
    return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

sqlite3.register_adapter(datetime, adapt_datetime)

DATABASE_FILE = 'giveaways.db'

connection = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
cursor = connection.cursor()

def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS giveaways (
            id INTEGER PRIMARY KEY,
            chat_id INTEGER,
            username TEXT,
            title TEXT,
            quantity INTEGER,
            months INTEGER,
            until_date TEXT,
            postid INTEGER,
            subscribe INTEGER,
            joke1 TEXT,
            joke2 TEXT,
            joke3 TEXT,
            joke4 TEXT,
            joke5 TEXT,
            joke6 TEXT,
            joke7 TEXT,
            joke8 TEXT,
            joke9 TEXT,
            joke10 TEXT
        )
    ''')
    connection.commit()
create_table()

connection.commit()

async def giveaway_filter(_, __, message: Message):
    is_valid_giveaway = (
        hasattr(message, 'giveaway') and
        hasattr(message.giveaway, 'quantity') and
        hasattr(message.giveaway, 'months') and
        hasattr(message.giveaway, 'until_date')
    )
    
    return is_valid_giveaway

giveaway = filters.create(giveaway_filter)

async def giveaway_handler(client: Client, message: Message):
    if message.giveaway:
        chats = message.giveaway.chats
        quantity = message.giveaway.quantity
        months = message.giveaway.months
        until_date = message.giveaway.until_date
        chid = message.chat.id
        postid = message.forward_from_message_id
        subscribe_required = len(chats) > 1
        first_username = ""
        primary_channel_username = ""  # Initialize here
        first_username = ""
        jokes = [""] * 10

        for i, chat in enumerate(chats):
            try:
                if chat.usernames and chat.usernames[0].username:
                    if not first_username:
                        first_username = chat.usernames[0].username
                    usernames = [username.username for username in chat.usernames]
                    print(f"{Fore.BLUE}{usernames}")
                elif chat.username:
                    if not first_username:
                        first_username = chat.username
                    print(f"{Fore.RED}{chat.username}")
                else:
                    print(f"{Fore.YELLOW}No username available")
            except Exception as e:
                print(f"{Fore.RED}Error: {e}")

        primary_channel_username = chats[0].username or first_username

        for i, chat in enumerate(chats):
            if i > 0 and i <= 10:
                jokes[i - 1] = chat.username or ""

        cursor.execute(f'''
            SELECT id FROM giveaways
            WHERE chat_id = ? AND until_date = ?
        ''', (chats[0].id, until_date))
        existing_record = cursor.fetchone()
        
        if not existing_record:
            jokes = [""] * 10

            if subscribe_required:
                primary_channel_username = chats[0].username or first_username
                for i, chat in enumerate(chats):
                    if i > 0 and i <= 10:
                        jokes[i - 1] = chat.username or ""

            print(f"Канал: {primary_channel_username}")

            cursor.execute('''
                INSERT INTO giveaways (chat_id, username, title, quantity, months, until_date, postid, subscribe, 
                                    joke1, joke2, joke3, joke4, joke5, joke6, joke7, joke8, joke9, joke10)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (chats[0].id, primary_channel_username, chats[0].title, quantity, months, until_date, postid,
                int(subscribe_required), *jokes))
            connection.commit()

            if subscribe_required:
                print(f"{Style.BRIGHT}{Fore.RED}Доп-каналы:{Style.RESET_ALL}")
                for i, chat in enumerate(chats):
                    if i > 0 and i <= 10:
                        print(f"{Style.BRIGHT}{Fore.RED}  - {i} @{chat.username or 'приватный канал'}{Style.RESET_ALL}")
                print(f"{Style.BRIGHT}{Fore.GREEN}Канал/Розыгрыш успешно добавлен в базу данных.{Style.RESET_ALL}")
        else:
            print(f"{Style.BRIGHT}{Fore.YELLOW}Канал/Розыгрыш уже записан в базе данных.{Style.RESET_ALL}")

async def main():
    app = Client(
        "my_account",
        api_hash="84b5095887c5e653ba785729cc53e71d",
        api_id=22190693
    )

    app.add_handler(MessageHandler(giveaway_handler, giveaway))

    await app.start()
    await idle()
    await app.stop()

if __name__ == "__main__":
    if platform.python_version_tuple() >= ("3", "11"):
        with asyncio.Runner() as runner:
            runner.get_loop().run_until_complete(main())
    else:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(main())
        connection.close()
