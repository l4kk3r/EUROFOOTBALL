from telegram import ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
import sqlite3

class BotMainFunctions:
    def __init__(self):
        self.main_keyboard = ReplyKeyboardMarkup([['🛒Купить', '💰Продать'], ['📜Мои объявления'], ['👤Мой профиль', '🌟Оценить пользователя'], ['✉️Тех-поддержка']], one_time_keyboard=False, resize_keyboard=True)

    def any_text(self, update, context):
        update.message.reply_text("Для управления используй клавиатуру!", reply_markup=self.main_keyboard)
    
    def send_contacts(self, update, context):
        update.message.reply_text("Тех-поддержка: @tim_vaulin (с 10:00 до 24:00 по мск)", reply_markup=self.main_keyboard)

    def start_command(self, update, context):
        with sqlite3.connect('bot.db') as db_connection:
            cursor = db_connection.cursor()
            if self.check_user_in_db_by_id(update, context):
                 update.message.reply_text("Привет! Я создан, чтобы облегчить покупку/продажу билетов на Евро2020", reply_markup=self.main_keyboard)
                 return
            command = '''INSERT INTO users (user_id, user_nickname, user_firstname, user_lastname, trust, trust_numbers, trusted_users, verification_status) VALUES (?, ?, ?, ?, 0, 0, "{}", "NONE")'''
            if not update.message.from_user.username:
                username = 'none'
            else:
                username = update.message.from_user.username.lower()
            cursor.execute(command, (update.message.chat_id, username, update.message.from_user.first_name, update.message.from_user.last_name))
            db_connection.commit()
            update.message.reply_text("Привет! Я создан, чтобы облегчить покупку/продажу билетов на Евро2020", reply_markup=self.main_keyboard)
            cursor.close()
    
    def check_user_in_db_by_id(self, update, context):
        with sqlite3.connect('bot.db') as db_connection:
            cursor = db_connection.cursor()
            command = f'''SELECT * FROM users WHERE user_id = ?'''
            r = cursor.execute( command, (update.message.chat_id,) ).fetchall()
            if len(r) > 0:
                return True
            return False

    def check_user_in_db_by_nickname(self, nickname):
        with sqlite3.connect('bot.db') as db_connection:
            cursor = db_connection.cursor()
            command = f'''SELECT * FROM users WHERE user_nickname = ?'''
            r = cursor.execute( command, (nickname.lower(),) ).fetchone()
            return r
    
    def stop_conversation_with_text(self, update, context):
        update.message.reply_text('Выход в главное меню', reply_markup=self.main_keyboard)
        return ConversationHandler.END 

    def stop_conversation(self, update, context):
        return ConversationHandler.END 