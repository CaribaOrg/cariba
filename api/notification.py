#!/usr/bin/python3

from datetime import datetime
from flask import jsonify, request
from api import api_restx
from models import strg
from models.user import User
from models.notification import Message
from flask_restx import Resource, fields

message_model = api_restx.model('Message', {
    'id': fields.String(required=True, description='Message ID'),
    'author': fields.String(required=False, description='Author Username'),
    'title': fields.String(required=False, description='Message Title'),
    'data': fields.String(required=True, description='Message Body'),
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
                    "created": mesg.updated_at.ctime()}       
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
                    "created": mesg.updated_at.ctime()}   
                    messages.append(n)
        return jsonify(messages)
        

api_restx.add_resource(Message, '/messages/<user_id>/<message_label>')
