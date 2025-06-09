#!/usr/bin/env python3
"""
Продакшен версия Telegram-бота для мини-игры казино
Использует переменные окружения для безопасности
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем настройки из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://your-webapp-url.com')

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

Ваш баланс автоматически сохраняется!
Нажмите кнопку ниже, чтобы начать играть! 🍀
    """
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup
    )
    
    logger.info(f"Пользователь {user.id} ({user.first_name}) запустил бота")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = """
🎰 Команды бота:

/start - Запустить игру
/help - Показать эту справку
/game - Открыть игру
/stats - Статистика (скоро)

🎮 Как играть:
1. Нажмите кнопку "Играть в казино"
2. В открывшемся WebApp нажмите "Играть"
3. Ваш баланс автоматически сохраняется по Telegram ID
4. Возвращайтесь в любое время - прогресс не потеряется!

💡 Особенности:
• Красивый интерфейс в чёрно-бирюзовых тонах
• Плавные анимации и эффекты
• Мгновенное сохранение прогресса
• Работает прямо в Telegram

Удачи в игре! 🍀
    """
    
    await update.message.reply_text(help_text)

async def game_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /game"""
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

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /stats (заглушка для будущего функционала)"""
    await update.message.reply_text(
        "📊 Статистика игроков скоро будет доступна!\n"
        "Пока что просто наслаждайтесь игрой 🎰"
    )

def main() -> None:
    """Основная функция запуска бота"""
    
    # Проверяем, что токен установлен
    if not BOT_TOKEN:
        print("❌ ОШИБКА: Токен бота не найден!")
        print("Установите переменную окружения BOT_TOKEN:")
        print("export BOT_TOKEN='ваш_токен_от_botfather'")
        print("export WEBAPP_URL='https://ваш-webapp-url.com'")
        return
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("game", game_command))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Запускаем бота
    print("🤖 Бот запущен!")
    print(f"📱 WebApp URL: {WEBAPP_URL}")
    print("Нажмите Ctrl+C для остановки.")
    
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

if __name__ == '__main__':
    main()

