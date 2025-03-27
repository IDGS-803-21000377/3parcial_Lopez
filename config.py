import os 
from flask import app
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import urllib


class Config(object):
    SECRET_KEY = 'Clave nuevsa'
    SECTION_COOKIE_SECURE = False

class DevelomentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI ="mysql+pymysql://root:1234@127.0.0.1/pizzeria"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

