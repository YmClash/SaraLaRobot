from flask import Flask, render_template, request, redirect, url_for
from flask_assets import Environment,Bundle
from flask_socketio import SocketIO,emit

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"