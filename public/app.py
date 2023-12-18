import logging
import pymysql
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor


# Set up logging
logging.basicConfig(level=logging.INFO)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = ''
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Replace with your MySQL database credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': '',
    'password': '',
    'db': '',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

# Establish a connection to the database
conn = pymysql.connect(**DB_CONFIG)
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    try:
        first_name = message.from_user.first_name
        print(message.from_user)
        print(first_name)
        await  message.reply(f'Салом {first_name},\nМан бот барои ёри расондан хангоми кофтани мошинхо аз сомонаи ENCAR')
    except Exception as e:
        logging.error(f"Error fetching brands: {e}")
        await message.reply(f"Салом {message.from_user.username}, ман бо каме хатогии техники дучор шудам!(")

# Define the /all command
@dp.message_handler(commands=['all'])
async def show_all_brands(message: types.Message):
    try:
        with conn.cursor() as cursor:
            # Fetch all brands from the 'brands' table
            cursor.execute("SELECT * FROM brands")
            brands = cursor.fetchall()

        # Create an inline keyboard with buttons for each brand
        keyboard = InlineKeyboardMarkup(row_width=1)
        for brand in brands:
            button = InlineKeyboardButton(text=brand['name'], callback_data=f"brand_{brand['id']}")
            keyboard.add(button)

        # Reply with the keyboard
        await message.reply("Маркаи мошинро интихоб кунед:", reply_markup=keyboard)

    except Exception as e:
        logging.error(f"Error fetching brands: {e}")
        await message.reply("Хангоми интихоби бренд хатоги рух дод.")

# Define a callback function for brand selection
@dp.callback_query_handler(lambda c: c.data.startswith('brand_'))
async def show_cars_by_brand(callback_query: types.CallbackQuery):
    try:
        # Extract brand ID from the callback data
        brand_id = int(callback_query.data.split('_')[1])

        with conn.cursor() as cursor:
            # Fetch cars for the selected brand from the 'cars' table
            cursor.execute("SELECT * FROM cars WHERE brand_id = %s", (brand_id,))
            cars = cursor.fetchall()

        # Create an inline keyboard with buttons for each car
        keyboard = InlineKeyboardMarkup(row_width=1)
        for car in cars:
            button = InlineKeyboardButton(text=car['name'], callback_data=f"car_{car['id']}")
            keyboard.add(button)

        # Reply with the keyboard
        await bot.send_message(callback_query.from_user.id, "Мошинаро интихоб намоед:", reply_markup=keyboard)

    except Exception as e:
        logging.error(f"Error fetching cars by brand: {e}")
        await bot.send_message(callback_query.from_user.id, "Хангоми интихоби бренд хатоги рух мошинхо..")

# Define a callback function for car selection (optional)
# ... (Previous code)

# ... (Previous code)

# Define a callback function for car selection
@dp.callback_query_handler(lambda c: c.data.startswith('car_'))
async def show_car_details(callback_query: types.CallbackQuery):
    try:
        car_id = int(callback_query.data.split('_')[1])

        with conn.cursor() as cursor:
            # Fetch details of the selected car from the 'cars' table
            cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
            car = cursor.fetchone()

        # Create inline keyboard with buttons for Tajik and Russian URLs
        keyboard = InlineKeyboardMarkup()
        tajik_button = InlineKeyboardButton(text="TJ", url=car['taj_url'])
        russian_button = InlineKeyboardButton(text="RU", url=car['rus_url'])
        keyboard.add(tajik_button, russian_button)

        # Prepare car details message
        car_details_message = f"модель: {car['name']}\n"

        # Reply with the car details and inline keyboard
        await bot.send_message(callback_query.from_user.id, car_details_message, reply_markup=keyboard)

    except Exception as e:
        logging.error(f"Error fetching car details: {e}")
        await bot.send_message(callback_query.from_user.id, "Хатогии техники лутфан каме пас боз такрор кунед.")

# ... (Rest of the code)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


