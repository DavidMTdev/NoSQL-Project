from flask import Flask
from app.settings.config import Config
# Import routes
from app.controllers.movie import movie
from app.controllers.company import company
from app.controllers.genre import genre


app = Flask(__name__)
app.config.from_object(Config)

# route
app.register_blueprint(movie)
app.register_blueprint(company)
app.register_blueprint(genre)

