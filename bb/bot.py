import asyncio
import logging
import sys
import sqlite3
import urllib3
import asyncio
import requests
import random
import time
import json

from datetime import datetime, timedelta
from aiogram import F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, StateFilter
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.context import FSMContext
from operator import itemgetter
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup

ADMINID = [1404114574]
TOKEN = "7063341831:AAFX80TtAyeQyW4rqZpx9mwBWco1xzrAnzA"
DATABASE_FILE_GIVEAWAYS = 'giveaways.db'
DATABASE_FILE_USERS = 'users.db'

dp = Dispatcher(storage=MemoryStorage())
users_display_modes = {}
users_sort_modes = {}
max_retries = 1
retry_delay = 5

class MyForm(StatesGroup):
    message = State()
    media = State() 

def format_date_for_query(date_str):
    date_obj = datetime.strptime(date_str, "%d.%m.%Y")
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")

def get_channels_by_date(target_date):
    connection = sqlite3.connect(DATABASE_FILE_GIVEAWAYS)
    cursor = connection.cursor()

    formatted_date = format_date_for_query(target_date)

    cursor.execute('''
        SELECT title, username, quantity, months, until_date, postid, subscribe, joke1, joke2, joke3, joke4, joke5, joke6, joke7, joke8, joke9, joke10
        FROM giveaways
        WHERE SUBSTR(until_date, 1, 10) = ? AND username IS NOT NULL
        ORDER BY quantity DESC
    ''', (formatted_date[:10],))

    channels_for_date = cursor.fetchall()
    channels_for_date = [(name, username, quantity, months, datetime.strptime(until_date, "%Y-%m-%d %H:%M:%S"), postid, subscribe, joke1, joke2, joke3, joke4, joke5, joke6, joke7, joke8, joke9, joke10)
                         for name, username, quantity, months, until_date, postid, subscribe, joke1, joke2, joke3, joke4, joke5, joke6, joke7, joke8, joke9, joke10 in channels_for_date]

    connection.close()
    return channels_for_date

async def save_user_to_database(user_id, username, full_name):
    connection = sqlite3.connect(DATABASE_FILE_USERS)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT
        )
    ''')

    cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        cursor.execute('''
            INSERT INTO users (id, username, full_name)
            VALUES (?, ?, ?)
        ''', (user_id, username, full_name))
    else:
        cursor.execute('''
            UPDATE users
            SET username = ?, full_name = ?
            WHERE id = ?
        ''', (username, full_name, user_id))

    connection.commit()
    connection.close()

def startmenu():
    kb = [
        [
            types.KeyboardButton(text="🔎 На сегодня"),
            types.KeyboardButton(text="🔍 На завтра"),
        ],
        [
            types.KeyboardButton(text="🔄 Отображение"),
            types.KeyboardButton(text="🔄 Сортировка"),
        ],
        [
            types.KeyboardButton(text="📊 ТОП дни"),
            types.KeyboardButton(text="📊 ТОП каналы")

        ],
        [   types.KeyboardButton(text="🛍 Кэшбек"),
            types.KeyboardButton(text="❓ FAQ / Помощь")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    return keyboard

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = f"{message.from_user.first_name} {message.from_user.last_name}"

    await save_user_to_database(user_id, username, full_name)

    connection_users = sqlite3.connect(DATABASE_FILE_USERS)
    cursor_users = connection_users.cursor()
    cursor_users.execute("SELECT COUNT(*) FROM users")
    user_count = cursor_users.fetchone()[0]
    connection_users.close()

    connection_giveaways = sqlite3.connect(DATABASE_FILE_GIVEAWAYS)
    cursor_giveaways = connection_giveaways.cursor()
    cursor_giveaways.execute("SELECT COUNT(DISTINCT username) FROM giveaways WHERE username IS NOT NULL")
    unique_channels_count = cursor_giveaways.fetchone()[0]
    cursor_giveaways.execute("SELECT COUNT(*) FROM giveaways WHERE username IS NOT NULL")
    giveaways_count = cursor_giveaways.fetchone()[0]
    cursor_giveaways.execute("SELECT SUM(quantity) FROM giveaways WHERE username IS NOT NULL")
    total_quantity = cursor_giveaways.fetchone()[0] or 0
    connection_giveaways.close()

    greetings = [
    "اخبارك اي يا, {name} ✌🏻",
    "مرحبًا, {name} 😁",
    "كيف حالك, {name} 🚀",
    "شخبارك, {name} 🤙🏻"
    ]

    selected_greeting = random.choice(greetings)

    formatted_greeting = selected_greeting.format(name=message.from_user.full_name)

    await message.answer(f"""
{formatted_greeting}
Я - твой <b>личный помощник в поиске розыгрышей премиум-подписок</b> по Телеграм каналам. 🎉

    <b>📊 إحصائيات البوت:</b>
عدد المستخدمين: <code>{user_count}</code>
Уникальных каналов: <code>{unique_channels_count}</code>
Проведено розыгрышей: <code>{giveaways_count}</code>
Всего тгп подарено: <code>{total_quantity}</code>

Выбери дату <b>с помощью кнопок ниже</b>, чтобы узнать, где <b>сегодня или завтра</b> проходят розыгрыши

Не упусти шанс выиграть премиум и следи за актуальными розыгрышами! 🌟""", reply_markup=startmenu())

def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="👑 Сотрудничество/Предложения", url="https://t.me/LztBab")
        ],
        [
            types.InlineKeyboardButton(text="🧾 Информационный канал", url="https://t.me/gifttelegrampremiums")
        ],
        [
            types.InlineKeyboardButton(text="🛍 Кэшбек", url="https://t.me/GetHalyava")
        ]
        ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

@dp.message(F.text == '🛍 Кэшбек')
async def quick_buttons_handler(message: types.Message):
    await message.answer(f'👥 {message.from_user.full_name}, нашли для тебя канал с скидками в телеграмм\n\n'
                         f'💯Всегда актуальные скидки\n'
                         f'➡️Максимальная экономия \n'
                         f'ℹ️Удобный поиск товаров и многое другое!\n\n'
                         f'Скорее подписывайся и делись нашим каналом со своими друзьями! \n\n'
                         f'🚀 @GetHalyava - нажми чтобы зайти',disable_web_page_preview=True)
    
@dp.message(F.text == '👤 Профиль')
async def quick_buttons_handler(message: types.Message):
    await message.answer(f'<b>👥 {message.from_user.full_name}, твой профиль:</b>\n\n'
                         f'🔖 Твой ID: <code>{message.from_user.id}</code>\n'
                         f'🤝 Твои рефераллы: <code>0</code>\n\n'
                         f'<b>🔗 Твоя персональная реферальная ссылка:\n'
                         f'<code>https://t.me/gifttelegrampremiums_bot?start={message.from_user.id}</code>\n\n'
                         f'<i>Приглашайте своих друзей и знакомых, и получайте шанс выиграть Telegram Premium каждые 7 дней</i>',disable_web_page_preview=True)

@dp.message(F.text == '❓ FAQ / Помощь')
async def quick_buttons_handler(message: types.Message):
    await message.answer(f"""
<b>❓ Для чего этот бот?</b>

<b>GTP BOT 🌟</b> — бот, позволяющий тебе через приятный интерфейс осуществлять <b>легкий поиск</b> Telegram каналов, которые в ближайшие дни разыграют <b>Telegram premium</b>

♻️Бот <b>автоматически</b> наполняется каналами и <b>обновляет</b> уже имеющие

                         
    <b>🔄 Отображение</b> - Настройка отображения списка каналов
                         
<i>1️⃣ Только username, отображает только username канала + доп.каналлов если они есть
2️⃣ Только ссылка на розыгрыш, отображает только ссылку на розыгрыш из основного канала
3️⃣ Подробный,отображение название канала, username канала + доп.каналлов, кол-во призов и время окончания розыгрыша, ссылку на розыгрыш
4️⃣ Основной, отображает username основного канала, кол-во призов и время окончания розыгрыша</i>
                   
    <b>🔄 Сортировка</b> - Настройка сортировки списка каналов

<i>1️⃣ По количеству призов, сортирует каналы по колличеству призов от большего к меньшему, сверху вниз
2️⃣ По времени, сортирует каналы по дате окончания розыгрыша от раннего к позднему, сверху вниз</i>

                         
<b>📊 ТОП дни</b> - <i>выдаст ТОП3 дня по колличеству разыгранных тгп</i>
<b>📊 ТОП каналы</b> - <i>выдаст ТОП3 канала по колличеству разыгранных тгп</i>""",disable_web_page_preview=True, reply_markup=get_keyboard())

@dp.message(F.text == '🔄 Отображение')
async def display_settings_handler(message: types.Message):
    kb = [
            [
                types.KeyboardButton(text="1️⃣ Только username"),
                types.KeyboardButton(text="2️⃣ Только ссылка на розыгрыш"),
            ],
            [
                types.KeyboardButton(text="3️⃣ Подробный"),
                types.KeyboardButton(text="4️⃣ Основной")
            ]
        ]
    keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
    input_field_placeholder="Выберите способ подачи"
    )
    await message.answer("<b>Выберите режим отображения 👀</b>", reply_markup=keyboard)

@dp.message(F.text == '1️⃣ Только username')
@dp.message(F.text == '2️⃣ Только ссылка на розыгрыш')
@dp.message(F.text == '3️⃣ Подробный')
@dp.message(F.text == '4️⃣ Основной')
async def display_mode_handler(message: types.Message):
    display_mode = message.text
    user_id = message.from_user.id
    users_display_modes[user_id] = display_mode

    await message.answer(f"<b>♻️ Режим отображения изменен на:</b> <code>{display_mode}</code>", reply_markup=startmenu())

@dp.message(F.text == '🔎 На сегодня')
@dp.message(F.text == '🔍 На завтра')
@dp.message(F.text == '🔄 Отображение')
@dp.message(F.text == '🔄 Сортировка')
async def quick_buttons_handler(message: types.Message):
    if message.text == '🔄 Сортировка':
        user_id = message.from_user.id
        current_sort_mode = users_sort_modes.get(user_id, 'По времени')
        new_sort_mode = 'По количеству призов' if current_sort_mode == 'По времени' else 'По времени'
        users_sort_modes[user_id] = new_sort_mode

        await message.answer(f"ℹ️ <b>Режим сортировки изменен на:</b> <code>{new_sort_mode}</code>")
        return

    user_id = message.from_user.id
    display_mode = users_display_modes.get(user_id, 'Полный')
    sort_mode = users_sort_modes.get(user_id, 'По времени')

    for attempt in range(max_retries):
        try:
            today = datetime.now().strftime("%d.%m.%Y")
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")

            selected_date = today if message.text == '🔎 На сегодня' else tomorrow
            channels_for_date = get_channels_by_date(selected_date)

            if not channels_for_date:
                await message.answer(f"🚫 На {selected_date} нет розыгрышей в базе данных.")
                break

            user_id = message.from_user.id
            sort_mode = users_sort_modes.get(user_id, 'По времени')

            if sort_mode == 'По времени':
                channels_for_date.sort(key=itemgetter(4))
            elif sort_mode == 'По количеству призов':
                channels_for_date.sort(key=itemgetter(2))
                channels_for_date.reverse()
            else:
                pass

            current_time = datetime.now()
            result_message = ""
            count_with_username = 0
            user_id = message.from_user.id
            display_mode = users_display_modes.get(user_id, '4️⃣ Основной')

            total_quantity = sum(channel[2] for channel in channels_for_date)

            result_message = ""
            count_with_username = 1

            for i, (name, username, quantity, months, end_time, postid, subscribe, joke1, joke2, joke3, joke4, joke5, joke6, joke7, joke8, joke9, joke10) in enumerate(channels_for_date):
                if not username or (isinstance(subscribe, str) and subscribe.lower() == 'hidden'):
                    continue

                if end_time <= current_time - timedelta(minutes=5):
                    continue

                if display_mode == '3️⃣ Подробный':
                    display_text = f"<b>{count_with_username}</b>. {name} | @{username} {' '.join([f'@{joke}' for joke in [joke1, joke2, joke3, joke4, joke5, joke6, joke7, joke8, joke9, joke10] if joke and subscribe])} | <code>{quantity}</code>тгп(<code>{months}мес.</code>) в <code>{end_time.strftime('%H:%M')}</code>" + (f" | t.me/{username}/{postid}\n" if postid else "\n")
                elif display_mode == '1️⃣ Только username':
                    display_text = f"<b>{count_with_username}</b>. @{username} {' '.join([f'@{joke}' for joke in [joke1, joke2, joke3, joke4, joke5, joke6, joke7, joke8, joke9, joke10] if joke and subscribe])}\n"
                elif display_mode == '2️⃣ Только ссылка на розыгрыш':
                    display_text = f"<b>{count_with_username}</b>. t.me/{username}/{postid}\n"
                elif display_mode == '4️⃣ Основной':
                    display_text = f"<b>{count_with_username}</b>. @{username} | <code>{quantity}тгп</code>(<code>{months}мес.</code>) в <code>{end_time.strftime('%H:%M')}</code>\n"
                else:
                    pass

                result_message += display_text
                count_with_username += 1 if username else 0

            if not result_message.strip():
                await message.answer(f"🚫 <b>На</b> <code>{selected_date}</code> <b>розыгрыши закончились.</b>")
                break

            total_message = f"<b>🎁 Общее кол-во призов:</b> <code>{total_quantity}</code><b>тгп</b>\n\n"
            await message.answer(f"<b>🎉 Розыгрыши на</b> <code>{selected_date}</code>\n{total_message}{result_message}", disable_web_page_preview=True)
            break
        except (requests.exceptions.ConnectionError, urllib3.exceptions.ProtocolError) as e:
            await asyncio.sleep(retry_delay)

@dp.message(F.text == '📊 ТОП дни')
@dp.message(Command("top3days"))
async def top_5_days_handler(message: types.Message):
    connection_giveaways = sqlite3.connect(DATABASE_FILE_GIVEAWAYS)
    cursor_giveaways = connection_giveaways.cursor()
    cursor_giveaways.execute('''
        SELECT SUBSTR(until_date, 9, 2) || '.' || SUBSTR(until_date, 6, 2) || '.' || SUBSTR(until_date, 3, 2) AS formatted_date, SUM(quantity) AS total_quantity
        FROM giveaways
        WHERE username IS NOT NULL
        GROUP BY SUBSTR(until_date, 1, 10)
        ORDER BY total_quantity DESC
        LIMIT 3
    ''')
    top_5_days = cursor_giveaways.fetchall()
    connection_giveaways.close()

    if not top_5_days:
        await message.answer("<b>🚫 Информация о розыгрышах отстутсвует.</b>")
        return

    response = "<b>📊 Топ 3 дня по розыгрышам:</b>\n\n"
    for index, (date, total_quantity) in enumerate(top_5_days, start=1):
        if index == 1:
            response += f"🥇 <b>{date}</b> | <code>{total_quantity}🌟</code>\n"
        elif index == 2:
            response += f"🥈 <b>{date}</b> | <code>{total_quantity}🌟</code>\n"
        elif index == 3:
            response += f"🥉 <b>{date}</b> | <code>{total_quantity}🌟</code>\n"

    await message.answer(response, parse_mode=ParseMode.HTML)

@dp.message(F.text == '📊 ТОП каналы')
@dp.message(Command("top3channels"))
async def top_3_channels_handler(message: types.Message):
    connection_giveaways = sqlite3.connect(DATABASE_FILE_GIVEAWAYS)
    cursor_giveaways = connection_giveaways.cursor()
    cursor_giveaways.execute('''
        SELECT title, username, SUM(quantity) AS total_quantity
        FROM giveaways
        WHERE username IS NOT NULL
        GROUP BY title
        ORDER BY total_quantity DESC
        LIMIT 3
    ''')
    top_3_channels = cursor_giveaways.fetchall()
    connection_giveaways.close()

    if not top_3_channels:
        await message.answer("<b>🚫 Нет данных о розыгрышах.</b>")
        return

    response = "<b>📊 Топ 3 канала по количеству розыгрышей:</b>\n\n"
    for index, (title, username, total_quantity) in enumerate(top_3_channels, start=1):
        if index == 1:
            response += f"🥇 <a href='t.me/{username}'><b>{title}</b></a> | <code>{total_quantity}🌟</code>\n"
        elif index == 2:
            response += f"🥈 <a href='t.me/{username}'><b>{title}</b></a> | <code>{total_quantity}🌟</code>\n"
        elif index == 3:
            response += f"🥉 <a href='t.me/{username}'><b>{title}</b></a> | <code>{total_quantity}🌟</code>\n"

    await message.answer(response, disable_web_page_preview=True)

@dp.message(Command("send_all"))
async def admin_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if str(user_id) == str(ADMINID):
        await message.answer('✏️ Напиши сообщение для рассылки')
        await state.set_state(MyForm.message)

@dp.message(MyForm.message)
async def input_message(message: types.Message, state: FSMContext):
    text_to_send = message.text
    await state.update_data(message_text=text_to_send)

    await message.answer('📸 Пришли медиа для рассылки или введите "пропустить"')
    await state.set_state(MyForm.media)

@dp.message(MyForm.media)
async def input_media(message: types.Message, state: FSMContext, bot=Bot):
    if message.text == 'пропустить':
        photo_to_send = None
    elif message.photo:
        photo_to_send = message.photo[-1].file_id
    else:
        await message.answer('🚫 Некорректный формат медиа. Пришли изображение или введи "<code>пропустить</code>".')
        return

    data = await state.get_data()
    text_to_send = data.get('message_text')

    connection_users = sqlite3.connect(DATABASE_FILE_USERS)
    cursor_users = connection_users.cursor()
    cursor_users.execute("SELECT id FROM users")
    users = cursor_users.fetchall()
    connection_users.close()
    successful_count = 0
    failed_count = 0

    for user_id in users:
        try:
            if photo_to_send:
                await bot.send_photo(user_id[0], photo_to_send, caption=text_to_send, parse_mode=ParseMode.HTML)
            else:
                await bot.send_message(user_id[0], text_to_send, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

            successful_count += 1
            await asyncio.sleep(0.05)
        except Exception as e:
            print(f"Failed to send message to user {user_id}: {e}")
            failed_count += 1

    report_message = f"✅ Рассылка завершена.\n\n📥 Успешно отправлено: {successful_count}\n🗑 Неудачно: {failed_count}"
    await message.answer(report_message)
    await state.clear()

@dp.message(F.text, lambda message: True)
async def unknown_message_handler(message: types.Message):
    await message.answer("<b>Я вас не понимаю, пропишите</b> /start")

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())