import asyncio
from telebot.async_telebot import AsyncTeleBot
import zipfile
import os
import tempfile
import shutil

from PromptEngine import PEngine

# Config для подключения к ЯЗ модели
model_api = '<Yout input>'
api_key = "<Yout input>"

# Замените 'YOUR_TOKEN' на токен вашего бота
API_TOKEN = '<Yout input>'
bot = AsyncTeleBot(API_TOKEN)

propmt_engine = PEngine(model_api, api_key,)

@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    text= "Привет! Я EvrazGPT! Я могу ответить на различные вопросы ). Также я умею делать Code Review проекта на python. Просто отправте мне фаил .zip проекта и отвечу, где у вас ошибки"
    await bot.reply_to(message=message, text=text, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
async def handle_text(message):
    wait_text = "⏳ Подождите...  💭 Что-бот *EvraszGPT* генерирует ответ на ваш запрос..."
    sent_message = await bot.send_message(chat_id=message.chat.id, text=wait_text, parse_mode='Markdown')
    try:
        content = propmt_engine.custom_query(message.text)
        await bot.delete_message(message.chat.id, sent_message.message_id)
        await bot.send_message(chat_id=message.chat.id, text=content, parse_mode='Markdown')
    except Exception as e:
        await bot.send_message(message.chat.id, f"(1) Произошла ошибка: *{e}*. Попробуйте снова.", "Markdown")


async def unzip_file(zip_filepath, extract_dir):
    with zipfile.ZipFile(zip_filepath, 'r') as zf:
        zf.extractall(extract_dir)


# async def walk_directory(directory: str):
#     """Рекурсивно обходит дерево директорий и возвращает его в виде словаря."""
#     tree = {}
#     for root, dirs, files in os.walk(directory):
#         # Определяем текущий узел в дереве
#         current_node = tree
#         path_parts = root[len(directory):].strip(os.sep).split(os.sep)
#         for part in path_parts:
#             if part not in current_node:
#                 current_node[part] = {}
#             current_node = current_node[part]
#         # Добавляем файлы в текущий узел
#         current_node["files"] = files
#     return tree

async def walk_directory(directory: str, indent=0):
    """Возвращает структуру проекта по заданному пути в виде текста."""
    structure = ""
    
    try:
        # Получаем список файлов и папок в указанном каталоге
        items = os.listdir(directory)
        
        # Сортируем элементы для более удобного отображения
        items.sort()
        
        for item in items:
            # Формируем полный путь к элементу
            full_path = os.path.join(directory, item)
            
            # Добавляем имя элемента с отступами в структуру
            structure += ' ' * indent + '|-- ' + item + '\n'
            
            # Если это папка, рекурсивно вызываем функцию
            if os.path.isdir(full_path):
                structure += await walk_directory(full_path, indent + 4)
    except PermissionError:
        structure += ' ' * indent + '|-- [Permission Denied]\n'
    except FileNotFoundError:
        structure += ' ' * indent + '|-- [File Not Found]\n'
    
    return structure


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
    sent_message = await bot.send_message(chat_id=message.chat.id, text=wait_text, parse_mode='Markdown')

    if not is_zip_file(file_name):
        await bot.delete_message(message.chat.id, sent_message.message_id)
        await bot.reply_to(message, "Простите, это не *.zip* файл")
        await shutil.rmtree(temp_dir, ignore_errors=True) 
    else:
        try:
            if sent_message.reply_to_message:
                await bot.delete_message(message.chat.id, sent_message.message_id)

            await unzip_file(file_path, temp_dir)
            os.remove(file_path)
            project_file = os.path.join(temp_dir, os.listdir(temp_dir)[0])
            tree = await walk_directory(project_file)
        
            content = propmt_engine.check_main_structure_dir(tree)
            await bot.delete_message(message.chat.id, sent_message.message_id)
            await bot.send_message(chat_id=message.chat.id, text=content, parse_mode='Markdown')
        except Exception as e:
            await bot.send_message(message.chat.id, f"(2) Произошла ошибка: *{e}*. Попробуйте снова.", 'Markdown')

        shutil.rmtree(temp_dir, ignore_errors=True) 


if __name__ == '__main__':
    print("Бот запущен...")
    asyncio.run(bot.polling(none_stop=True))
