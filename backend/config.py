"""Adam Cohen Hillel 2022, All Rights Reserved
"""


class APIProdConfig:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/adamcohenhillel/Desktop/projects/deeper/test.db'
    JWT_SECRET_KEY = 'super-secret-change-me'  # TODO: Change this!


class APITestConfig:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/adamcohenhillel/Desktop/projects/deeper/test.db'
    JWT_SECRET_KEY = 'super-secret-change-me'  # TODO: Change this!
