from flask import Flask
from app.settings.config import Config
# Import routes
from app.controllers.test import test

app = Flask(__name__)
app.config.from_object(Config)

# route
app.register_blueprint(test)
