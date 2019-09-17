from flask import Flask, render_template, url_for, request, redirect, flash, session,g
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key="BIRSINGH"
db = SQLAlchemy(app)