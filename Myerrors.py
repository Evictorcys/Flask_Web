# coding=utf-8
"""

jinja2.exceptions.TemplateNotFound: bootstrap/base.html
Reason:
'' in {% extends 'bootstrap/base.html' %} should be ""

name = StringField("What is your name?",validators = [Required()]) instead of 
name = StringField("What is your name?",validators = [Required])

from flask_sqlalchemy import SQLAlchemy instead of
from flask_sqlalchemy import SQLALchemy

ImportError: No module named 'MySQLdb'
Reason:python3
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://...' instead of
SQLALCHEMY_DATABASE_URI = 'mysql://...'


"""
