from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import random
from src.models.user import Player, db

casino_bp = Blueprint('casino', __name__)

@casino_bp.route('/player/<telegram_id>', methods=['GET'])
@cross_origin()
def get_player(telegram_id):
    """Получить информацию об игроке по Telegram ID"""
    player = Player.query.filter_by(telegram_id=telegram_id).first()
    
    if not player:
        # Создаем нового игрока с начальным балансом 100 монет
        player = Player(telegram_id=telegram_id, balance=100)
        db.session.add(player)
        db.session.commit()
    
    return jsonify(player.to_dict())

@casino_bp.route('/player/<telegram_id>/update', methods=['POST'])
@cross_origin()
def update_player_info(telegram_id):
    """Обновить информацию об игроке (имя пользователя)"""
    data = request.json
    player = Player.query.filter_by(telegram_id=telegram_id).first()
    
    if not player:
        player = Player(telegram_id=telegram_id, balance=100)
        db.session.add(player)
    
    if 'username' in data:
        player.username = data['username']
    
    db.session.commit()
    return jsonify(player.to_dict())

@casino_bp.route('/play/<telegram_id>', methods=['POST'])
@cross_origin()
def play_game(telegram_id):
    """Сыграть в казино (ставка 10 монет)"""
    player = Player.query.filter_by(telegram_id=telegram_id).first()
    
    if not player:
        return jsonify({'error': 'Игрок не найден'}), 404
    
    if player.balance < 10:
        return jsonify({'error': 'Недостаточно монет для ставки'}), 400
    
    # Снимаем ставку
    player.balance -= 10
    
    # Определяем результат игры
    # 40% - проигрыш (0 монет)
    # 30% - выигрыш 20 монет
    # 20% - выигрыш 50 монет  
    # 10% - выигрыш 100 монет
    rand = random.random()
    
    if rand < 0.4:
        # Проигрыш
        winnings = 0
        result = 'loss'
        message = 'Увы, вы проиграли!'
    elif rand < 0.7:
        # Выигрыш 20 монет
        winnings = 20
        result = 'win'
        message = 'Поздравляем! Вы выиграли 20 монет!'
    elif rand < 0.9:
        # Выигрыш 50 монет
        winnings = 50
        result = 'win'
        message = 'Отлично! Вы выиграли 50 монет!'
    else:
        # Выигрыш 100 монет
        winnings = 100
        result = 'win'
        message = 'Джекпот! Вы выиграли 100 монет!'
    
    # Добавляем выигрыш к балансу
    player.balance += winnings
    
    db.session.commit()
    
    return jsonify({
        'result': result,
        'winnings': winnings,
        'message': message,
        'new_balance': player.balance,
        'bet_amount': 10
    })

@casino_bp.route('/leaderboard', methods=['GET'])
@cross_origin()
def get_leaderboard():
    """Получить топ игроков по балансу"""
    players = Player.query.order_by(Player.balance.desc()).limit(10).all()
    return jsonify([player.to_dict() for player in players])

