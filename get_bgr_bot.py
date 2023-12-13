"""Бот с использованием библиотеки pyTelegramBotAPI"""
import shutil
import telebot
from config import TOKEN, ID_ADMIN
import os

from rmv_bgrnd import rmv_bgrnd
from work_sqlite import rec_id_in_base, get_users_info

# регистрация бота
bot = telebot.TeleBot(TOKEN, parse_mode=None)


# Обработка комманд старт и хелп
@bot.message_handler(commands=['start', 'help'])
def start(message):
    # Получаем id пользователя и имя из сообщения
    user_id_telegram = message.from_user.id
    user_name = message.from_user.username

    # Вызываем функцию записи в базу
    rec_id_in_base(user_id_telegram, user_name)

    bot.send_message(message.chat.id, 'Привет! Я бот, который убирает фон с фотографий. '
                                      'Отправьте мне фотку или несколько. Только не отправляте много, иначе я буду долго думать')


@bot.message_handler(commands=['admin_info'])
def admin_bd_info(message):
    if message.from_user.id == ID_ADMIN:
        # Получаем информацию о пользователях
        users_info = get_users_info()

        # Отправляем список пользователей
        if users_info:
            user_list = "\n".join(f"{index + 1}. id - {user[1]} - {user[2]}" for index, user in enumerate(users_info))
            bot.send_message(message.chat.id, f"Список пользователей:\n{user_list}")
        else:
            bot.send_message(message.chat.id, "База данных пользователей пуста.")

    else:
        bot.send_message(message.chat.id, "Кажется, вы не мой хозяин")


# Прием картинок в сообщении
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.reply_to(message, "Приняли фото, обрабатываем")

    # Получаем информацию о фотографии
    file_info = bot.get_file(message.photo[-1].file_id)
    file_path = file_info.file_path  # создаем объект фотографию

    # Скачиваем фотографию
    downloaded_file = bot.download_file(file_path)

    # Сохраняем фотографию в папку "pictures" с уникальным именем
    photo_path = os.path.join('pictures', f'{message.photo[-1].file_id}.jpg')  # создаем адрес ссылки на фотку
    with open(photo_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Путь для сохранения измененной фотографии
    output_path = os.path.join('output_pictures', f'{message.photo[-1].file_id}_output.jpg')

    # Вызываем вашу функцию для удаления фона
    rmv_bgrnd(photo_path, output_path)

    bot.send_message(message.chat.id, "готово")
    # Отправляем обработанную фотку
    bot.send_document(chat_id=message.chat.id, document=open(output_path, 'rb'))

    # Удаляем оригинальные и измененные фотографии после отправки
    shutil.rmtree('pictures')
    shutil.rmtree('output_pictures')

    # Пересоздаем папки
    os.makedirs('pictures')
    os.makedirs('output_pictures')


# Обработчик всех других текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    # Отвечаем на любые текстовые сообщения
    bot.reply_to(message, "Отправьте фотографию")


# Обработчик всех других медиа-сообщений
@bot.message_handler(content_types=['video', 'audio', 'document', 'sticker', 'voice', 'video_note', 'location', 'contact', 'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message', 'game'])
def handle_other_media(message):
    # Отвечаем на все другие типы медиа-сообщений
    bot.reply_to(message, "Извините, но бот принимает только фотографии. Отправьте, пожалуйста, фотографию.")


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
