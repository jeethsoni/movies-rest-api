"""
Flask app entry point
"""

from flask import Flask
from blueprints.health.blueprint import health_blueprint
from blueprints.movie.blueprint import movie_blueprint
from db.Connection import Connection
from logger import logger


app = Flask(__name__)
logger = logger.configure_logger("default", "logs/flask.log")

# pushes the application context
ctx = app.app_context()
ctx.push()

app.logger = logger

# creates a Connection instance stores it in app.conn
conn = Connection()
app.conn = conn


# registers the blueprints
app.register_blueprint(health_blueprint)
app.register_blueprint(movie_blueprint)


if __name__ == "__main__":
    app.run(debug=True)
