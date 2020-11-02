import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine
import json

#database_name = 'capstone'
#database_path = "postgres://{}/{}".format('localhost:5432', database_name)
db = SQLAlchemy()

#def setup_db(app, database_path=database_path):
#    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
#    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#    db.app = app
#    db.init_app(app)
#    db.create_all()


class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    jobs =  db.relationship('Job', backref='client', lazy=True, passive_deletes=True)

    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
        'id': self.id,
        'name': self.name,
        'address': self.address,
        'phone': self.phone
        }

    def long(self):
        return{
        'id': self.id,
        'name': self.name,
        'address': self.address,
        'phone': self.phone
        }






class Contractor(db.Model):
    __tablename__ = 'contractor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    phone = db.Column(db.String(120))
    jobs = db.relationship('Job', backref='contractor', lazy=True, passive_deletes=True)

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
        'id': self.id,
        'name': self.name,
        'phone': self.phone
        }

    def long(self):
        return{
        'id': self.id,
        'name': self.name,
        'phone': self.phone
        }




class Job(db.Model): #New model for shows
    __tablename__= 'job'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=True)
    contractor_id = db.Column(db.Integer, db.ForeignKey('contractor.id', ondelete='CASCADE'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, contractor_id, client_id, start_time):
        self.contractor_id = contractor_id
        self.client_id = client_id
        self.start_time = start_time

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
        'id': self.id,
        'start_time': self.start_time,
        }

    def long(self):
        return{
        'id': self.id,
        'start time': self.start_time,
        'client id': self.client_id,
        'contractor id': self.contractor_id
        }
