import json
import os

import flask
from flask import Flask, render_template, request, url_for, redirect, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"mysql://root:{os.getenv('MYSQL_PASSWORD')}@localhost:3306/db_bookinder"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

