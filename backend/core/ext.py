"""Adam Cohen Hillel 2022, All Rights Reserved
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager

Base = declarative_base()
db = SQLAlchemy(model_class=Base)
jwt = JWTManager()