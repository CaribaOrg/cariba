#!/usr/bin/python3

from datetime import datetime
from flask import jsonify, request
from api import api_restx
from models import strg
from models.user import User
from models.notification import Message
from flask_restx import Resource, fields

message_model = api_restx.model('Message', {
    'author': fields.String(required=True, description='Author Username'),
    'title': fields.String(required=True, description='Message Title'),
    'body': fields.String(required=True, description='Message Body'),
    'label': fields.String(required=True, description='Message Label'),
})

class Message(Resource):
    @api_restx.response(200, 'Successful operation')
    def get(self, user_id, message_label="all"):
        user = strg.search(cls=User, id=user_id)
        if not user:
            return 'None found', 404
        user.last_message_read_time = datetime.utcnow()
        user.add_notification('unread_message_count', 0)
        strg.save()
        if message_label == "all":
            messages = []
            all_messages = user.messages_received
            for mesg in all_messages:
                n = {
                    "author": mesg.author.username,
                    "title": mesg.title,
                    "body": mesg.body,
                    "created": mesg.updated_at.ctime(),
                    "label": mesg.message_label}      
                messages.append(n)
            print(messages)
        else:
            messages = []
            all_messages = user.messages_received
            for mesg in all_messages:
                if mesg.message_label == message_label:
                    n = {
                    "author": mesg.author.username,
                    "title": mesg.title,
                    "body": mesg.body,
                    "created": mesg.updated_at.ctime(),
                    "label": mesg.message_label}   
                    messages.append(n)
        return jsonify(messages)

class SendMessage(Resource):
    @api_restx.expect(message_model)
    @api_restx.response(200, 'Successful operation')
    @api_restx.response(400, 'Invalid Request Format')
    @api_restx.response(404, 'Invalid ID supplied')
    def post(self, user_id=None):
        data = request.get_json()
        send_to_all = False
        if not data:
            return {'error': 'Invalid request format Error 5051'}, 400
        if 'author' not in data or 'title' not in data or 'body' not in data or 'label' not in data:
            return {'error': 'Invalid request format Error 5052'}, 404
        
        if user_id is None:
            send_to_all = True
        else:
            recipient = strg.session.query(User).filter_by(id=user_id).first()
            if not recipient:
                return {'error': 'Invalid request format Error 5053'}, 400
        author = strg.session.query(User).filter_by(id=data.author).first()
        if not author:
            return {'error': 'Invalid request format Error 5054'}, 400
        
        if send_to_all:
            for one_user in User.query.all():
                Message(author=author, recipient=one_user,
                    body=data.body, title=data.title, label=data.label)
                strg.save()
                one_user.add_notification('unread_message_count',
                            one_user.unread_message_count())
                strg.save()
        else:
            Message(author=author, recipient=recipient,
                    body=data.body, title=data.title, label=data.label)
            strg.save()
            recipient.add_notification('unread_message_count',
                                recipient.unread_message_count())
            strg.save()
    
        return jsonify({'success': 'Valid request format, Message sent'})

api_restx.add_resource(Message, '/messages/<user_id>/<message_label>')
api_restx.add_resource(SendMessage, '/send_messages/<user_id>')
