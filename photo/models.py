from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
from passlib.apps import custom_app_context as password_context
import re



heroku = Heroku(app)

db = SQLAlchemy()
ma = Marshmallow()


class ResourceAddUpdateDelete():   
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()



class User(db.Model, ResourceAddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    creation_date = db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp(), nullable=False)

    def verify_password(self, password):
        return password_context.verify(password, self.password_hash)

    def check_password_strength_and_hash_if_ok(self, password):
        if len(password) < 8:
            return 'The password is too short. Please, specify a password with at least 8 characters.', False
        if len(password) > 32:
            return 'The password is too long. Please, specify a password with no more than 32 characters.', False

        if re.search(r'[A-Z]', password) is None:
            return 'The password must include at least one uppercase letter.', False

        if re.search(r'[a-z]', password) is None:
            return 'The password must include at least one lowercase letter.', False

        if re.search(r'\d', password) is None:
            return 'The password must include at least one number.', False

        if re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]',password) is None:
            return 'The password must include at least one symbol.', False

        self.password_hash = password_context.hash(password)
        return '', True

    def __init__(self, name,email):
        self.name = name
        self.email = email




class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True,validate=validate.Length(3))
    email = fields.String(required=True,validate=validate.Length(3))
    password = fields.String(required=True,validate=validate.Length(6))
    url = ma.URLFor('photo.userresource',id='<id>',_external=True)


class Photo(db.Model,ResourceAddUpdateDelete):
    
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(250),unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    photo_category_id = db.Column(db.Integer, db.ForeignKey('photo_category.id', ondelete='CASCADE'), nullable=False)
    photo_category = db.relationship('PhotoCategory', backref=db.backref('photos', lazy='dynamic' , order_by='Photo.link'))
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self,link, description,photo_category):
        self.link = link
        self.description = description
        self.photo_category = photo_category
        

    @classmethod
    def is_link_unique(cls,id,link):
        existing_link = cls.query.filter_by(link=link).first()
        if existing_link is None:
            return True
        else:
            if existing_link.id == id:
                return True
            else:
                return False




class PhotoCategory(db.Model,ResourceAddUpdateDelete):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable = False)

    def __init__(self,name):
        self.name = name



    @classmethod
    def is_name_exist(cls,id,name):
        existing_name = cls.query.filter_by(name=name).first()
        return existing_name 
        


class PhotoCategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(3))
    url = ma.URLFor('photo.photocategoryresource',id='<id>')
    photos = fields.Nested('PhotoSchema', 
        many=True, 
        exclude=('photo_category',))










class PhotoSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    link = fields.String(required=True, validate=validate.Length(5))
    description = fields.String(required=True, validate=validate.Length(5))
    photo_category = fields.Nested(PhotoCategorySchema, 
        only=['id', 'url', 'name'], 
        required=True)
    url = ma.URLFor('photo.photoresource',id='<id>',_external=True)
    

    @pre_load
    def process_photo_category(self, data,**kwargs):
        photo_category = data.get('photo_category')
        if photo_category:
            if isinstance(photo_category, dict):
                photo_category_name = photo_category.get('name')
            else:
                photo_category_name = photo_category
            photo_category_dict = dict(name=photo_category_name)
        else:
            photo_category_dict = {}
        data['photo_category'] = photo_category_dict
        return data


