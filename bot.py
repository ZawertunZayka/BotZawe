#!/usr/bin/env python3
"""
Простой Telegram-бот для запуска мини-игры казино WebApp
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ВАЖНО: Замените на ваш токен бота от @BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# URL вашего WebApp (замените на реальный URL после развертывания)
WEBAPP_URL = "https://your-webapp-url.com"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    
    # Создаем кнопку для запуска WebApp
    keyboard = [
        [InlineKeyboardButton(
            "🎰 Играть в казино", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = f"""
🎰 Добро пожаловать в мини-казино, {user.first_name}!

🎲 Испытайте удачу в нашей увлекательной игре!
💰 Начальный баланс: 100 монет
🎯 Ставка: 10 монет за игру

Возможные выигрыши:
🎯 +20 монет (30% шанс)
💎 +50 монет (20% шанс)  
🏆 +100 монет (10% шанс)
💸 Проигрыш (40% шанс)

Нажмите кнопку ниже, чтобы начать играть!
    """
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = """
🎰 Команды бота:

/start - Запустить игру
/help - Показать эту справку
/game - Открыть игру

🎮 Как играть:
1. Нажмите кнопку "Играть в казино"
2. В открывшемся WebApp нажмите "Играть"
3. Ваш баланс автоматически сохраняется
4. Удачи в игре! 🍀
    """
    
    await update.message.reply_text(help_text)

async def game_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /game - альтернативный способ запуска игры"""
    keyboard = [
        [InlineKeyboardButton(
            "🎰 Открыть казино", 
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎲 Готовы испытать удачу? Нажмите кнопку ниже!",
        reply_markup=reply_markup
    )

def main() -> None:
    """Основная функция запуска бота"""
    
    # Проверяем, что токен установлен
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ОШИБКА: Необходимо установить токен бота!")
        print("1. Получите токен у @BotFather в Telegram")
        print("2. Замените YOUR_BOT_TOKEN_HERE на ваш токен в файле bot.py")
        print("3. Замените WEBAPP_URL на URL вашего развернутого WebApp")
        return
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("game", game_command))
    
    # Запускаем бота
    print("🤖 Бот запущен! Нажмите Ctrl+C для остановки.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

