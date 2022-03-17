"""Adam Cohen Hillel 2022, All Rights Reserved
"""
from flask import Flask


# API Design:
#   - user
#   - matchmaker
#   - rooms
#       Where all the chatting actually is happening

def create_app():
    app = Flask(__name__)
    # app.register_blueprint(example_blueprint)
