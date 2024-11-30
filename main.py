import telebot
import asyncio
from telebot.async_telebot import AsyncTeleBot
import requests
import json
import glob
import zipfile
import os
import tempfile
import shutil

from PromptEngine import PEngine


# https://habr.com/ru/companies/skillfactory/articles/837366/


# Config для подключения к ЯЗ модели
model_api = '<Your url>'
api_key = "<Your api key>"

# Замените 'YOUR_TOKEN' на токен вашего бота
API_TOKEN = '<Your token>'
bot = AsyncTeleBot(API_TOKEN)

propmt_engine = PEngine(model_api, api_key,)


@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    text= "Привет! Отправь мне текстовый файл, и я его проанализирую."
    await bot.reply_to(message=message, text=text, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
async def handle_text(message):
    

    wait_text = "⏳ Подождите...  💭 Что-бот *EvraszGPT* генерирует ответ на ваш запрос..."
    await bot.send_message(chat_id=message.chat.id, text=wait_text, parse_mode='Markdown')

    try:
        content = propmt_engine.custom_query(message.text)

        await bot.delete_message(message.chat.id, message.message_id+1)
        await bot.send_message(chat_id=message.chat.id, text=content, parse_mode='Markdown')
    except Exception:
        await bot.delete_message(message.chat.id, message.message_id+1)
        await bot.send_message(message.chat.id, "Простите. Произошла ошибка, попробуйте снова.")


async def unzip_file(zip_filepath, extract_dir):
    with zipfile.ZipFile(zip_filepath, 'r') as zf:
        zf.extractall(extract_dir)


async def walk_directory(directory: str):
    """Рекурсивно обходит дерево директорий и возвращает его в виде словаря."""
    tree = {}
    for root, dirs, files in os.walk(directory):
        # Определяем текущий узел в дереве
        current_node = tree
        path_parts = root[len(directory):].strip(os.sep).split(os.sep)
        for part in path_parts:
            if part not in current_node:
                current_node[part] = {}
            current_node = current_node[part]
        # Добавляем файлы в текущий узел
        current_node["files"] = files
    return tree


def is_zip_file(filename):
    if filename[-3:] == 'zip':
        return True
    return False

@bot.message_handler(content_types=['document'])
async def handle_codes(message):
    file_name = message.document.file_name
    file_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    # Сохраняем файл во временной директории
    temp_dir = tempfile.mkdtemp(dir='FILES/')
    file_path = os.path.join(temp_dir, file_name)
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)
    
    wait_text = "⏳ Подождите...  💭 Что-бот *EvraszGPT* генерирует ответ на ваш запрос..."
    await bot.send_message(chat_id=message.chat.id, text=wait_text, parse_mode='Markdown')

    if not is_zip_file(file_name):
        await bot.delete_message(message.chat.id, message.message_id+1)

        await bot.reply_to(message, "Простите, это не *.zip* файл")
        await shutil.rmtree(temp_dir, ignore_errors=True) 
    else:
        await bot.delete_message(message.chat.id, message.message_id+1)

        await unzip_file(file_path, temp_dir)
        os.remove(file_path)
        project_file = os.path.join(temp_dir, os.listdir(temp_dir)[0])
        tree = await walk_directory(project_file)
        await bot.reply_to(message, tree)


if __name__ == '__main__':
    print("Бот запущен...")
    asyncio.run(bot.polling(none_stop=True))
