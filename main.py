import telebot
import asyncio
from telebot.async_telebot import AsyncTeleBot
import requests
import json


# https://ru.stackoverflow.com/questions/988985/python-%d0%ba%d0%be%d0%b3%d0%b4%d0%b0-%d1%81%d0%bb%d0%b5%d0%b4%d1%83%d0%b5%d1%82-%d0%b8%d1%81%d0%bf%d0%be%d0%bb%d1%8c%d0%b7%d0%be%d0%b2%d0%b0%d1%82%d1%8c-async-%d0%b0-%d0%ba%d0%be%d0%b3%d0%b4%d0%b0-await/1070892#1070892
# https://mastergroosha.github.io/aiogram-3-guide/quickstart/
# https://habr.com/ru/companies/skillfactory/articles/837366/


# Config для подключения к ЯЗ модели
model_api = '<Your api>'
api_key = "<Your api key>"

# Замените 'YOUR_TOKEN' на токен вашего бота
API_TOKEN = '<Your Token bot>'
bot = AsyncTeleBot(API_TOKEN)


async def analyze_file(file_path):
    """Функция для анализа текстового файла."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        line_count = len(lines)
        word_count = sum(len(line.split()) for line in lines)
    
    return f'Количество строк: {line_count}\nКоличество слов: {word_count}'


@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    await bot.reply_to(message, "Привет! Отправь мне текстовый файл, и я его проанализирую.")


@bot.message_handler(content_types=['text'])
async def handle_text(message):
    headers = {
        "Authorization" : api_key,
        "Content-Type": "application/json; charset=utf-8"
    }

    data = {
        "model": "mistral-nemo-instruct-2407",
        "messages": [
            {
                "role": "system",
                "content": "отвечай на русском языке"
            },
            {
                "role": "user",
                "content": message.text
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.35
    }

    await bot.send_message(message.chat.id, "⏳ Подождите...  💭 Что-бот EvraszGPT генерирует ответ на ваш запрос...")

    response = requests.post(model_api, headers=headers, data=json.dumps(data)).json()
    content = response.get('choices')[0].get("message").get('content')

    await bot.delete_message(message.chat.id, message.message_id+1)
    await bot.send_message(message.chat.id, content)


@bot.message_handler(content_types=['document'])
async def handle_document(message):
    file_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    # Сохраняем файл на сервере
    file_path = 'uploaded_file.txt'
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    await process_file(file_path, message.chat.id)


async def process_file(file_path, chat_id):
    """Функция для обработки файла и отправки результата пользователю."""
    analysis_result = await analyze_file(file_path)
    await bot.send_message(chat_id, f'Результат анализа:\n{analysis_result}')


if __name__ == '__main__':
    print("Бот запущен...")
    asyncio.run(bot.polling(none_stop=True))
