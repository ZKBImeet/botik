# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from app import db

#db = SQLAlchemy(app)

class db_likes(db.Model):

    __tablename__ = "t_likes"

    message_id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.String(255), primary_key=True)
    choice_value = db.Column(db.String(255))

    def __init__(self, message_id, user_id, choice_value):
        #try:
        #    self = self.query.get()
        self.message_id = message_id
        self.user_id = user_id
        self.choice_value = choice_value

    #def __init_1_(self, message_id, user_id, choice_value):
    #    self.message_id = message_id
    #    self.user_id = user_id
    #    self.choice_value = choice_value

    def __repr__(self):
        return '<user message_id=%r,user_id=%r,choice_value=%r>' % (self.message_id, self.user_id, self.choice_value)
