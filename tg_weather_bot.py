import requests
from config import token, tg_bot
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Введите город: ')

@dp.message_handler()
async def get_weather(message: types.Message):
    code_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstom': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }
    try:
        r = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={token}&units=metric'
        )
        data = r.json()
        city = data['name']
        current_weather = data['main']['temp']
        weather_description = data['weather'][0]['main']
        if weather_description in code_smile:
            wd = code_smile[weather_description]
        else:
            wd = 'Посмотри в окно'
        humidity = data['main']['humidity']
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
        await message.reply(f'Погода в городе: {city}\nТемпература сейчас: {current_weather} °C {wd}\n'
              f'Максимальная температура: {temp_max}°C\nМинимальная температура: {temp_min}°C\n'
              f'Влажность: {humidity}%')

    except:
        await message.reply('\U00002620 Неверное название города. \U00002620 ')

if __name__ == '__main__':
    executor.start_polling(dp)