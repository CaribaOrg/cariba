#!/usr/bin/python3

from datetime import datetime
from flask import jsonify, request
from api import api_restx
from models import strg
from models.user import User
from models.notification import Message as MessageModel
from flask_restx import Resource, fields

message_model = api_restx.model('Message', {
    'send_all': fields.Boolean(required=True, description='Send To all'),
    'author': fields.String(required=True, description='Author Username'),
    'recipient': fields.String(required=True, description='Recipient Username'),
    'title': fields.String(required=True, description='Message Title'),
    'body': fields.String(required=True, description='Message Body'),
    'label': fields.String(required=True, description='Message Label'),
})

class Message(Resource):
    @api_restx.response(200, 'Successful operation')
    def get(self, user_id, message_label="all"):
        user = strg.session.query(User).filter_by(id=user_id).first()
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
                    "id": mesg.id,
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
                        "id": mesg.id,
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
    def post(self):
        data = request.get_json()
        send_to_all = False
        if not data:
            return {'error': 'Invalid request format Error 5051'}, 400

        if 'author' not in data or 'title' not in data or 'body' not in data or 'label' not in data or 'send_all'not in data or 'recipient'not in data:
            return {'error': 'Invalid request format Error 5052'}, 404
        send_to_all = data.get("send_all")
        author_username = data.get("author")
        title = data.get("title")
        body = data.get("body")
        label = data.get("label")
        recipient_username = data.get("recipient")
        
        if not send_to_all:
            recipient = strg.session.query(User).filter_by(username=recipient_username).first()
            if not recipient:
                return {'error': 'Invalid request format Error 5053'}, 400
        author = strg.session.query(User).filter_by(username=author_username).first()
        if not author:
            return {'error': 'Invalid request format Error 5054'}, 400
        
        if send_to_all:
            for one_user in User.query.all():
                MessageModel(author=author, recipient=one_user, body=body, title=title, message_label=label)
                strg.save()
                one_user.add_notification('unread_message_count',
                            one_user.unread_message_count())
                strg.save()
        else:
            MessageModel(author=author, recipient=recipient, body=body, title=title, message_label=label)
            strg.save()
            recipient.add_notification('unread_message_count',
                                recipient.unread_message_count())
            strg.save()
    
        return jsonify({'success': 'Valid request format, Message sent'})

class SentMessage(Resource):
    @api_restx.response(200, 'Successful operation')
    def get(self, user_id):
        user = strg.session.query(User).filter_by(id=user_id).first()
        if not user:
            return 'None found', 404
        
        messages = []
        all_messages = user.messages_sent
        for mesg in all_messages:
            n = {
                "id": mesg.id,
                "author": mesg.author.username,
                "title": mesg.title,
                "body": mesg.body,
                "created": mesg.updated_at.ctime(),
                "label": mesg.message_label}      
            messages.append(n)
        print(messages)
        
        return jsonify(messages)

api_restx.add_resource(Message, '/messages/<user_id>/<message_label>')
api_restx.add_resource(SendMessage, '/send_messages')
api_restx.add_resource(SentMessage, '/sent_messages/<user_id>')
