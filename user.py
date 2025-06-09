from flask import Blueprint, jsonify, request
from src.models.user import Player, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = Player.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users', methods=['POST'])
def create_user():
    
    data = request.json
    user = Player(telegram_id=data['telegram_id'], username=data.get('username'))
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Player.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = Player.query.get_or_404(user_id)
    data = request.json
    user.username = data.get('username', user.username)
    user.telegram_id = data.get('telegram_id', user.telegram_id)
    db.session.commit()
    return jsonify(user.to_dict())

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Player.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
