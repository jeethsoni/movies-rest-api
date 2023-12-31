"""
Flask app entry point
"""

import emoji
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException, default_exceptions
from blueprints.health.blueprint import health_blueprint
from blueprints.movie.blueprint import movie_blueprint
from blueprints.actor.blueprint import actor_blueprint
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


@app.errorhandler(Exception)
def handle_error(err):
    """
    This function handles error
    """
    code = 500
    if isinstance(err, HTTPException):
        code = err.code
    app.logger.error(emoji.emojize(":cross_mark: => " + str(err)))
    return jsonify(error=str(err)), code


for default_exception in default_exceptions:
    app.register_error_handler(default_exception, handle_error)


# registers the blueprints
app.register_blueprint(health_blueprint)
app.register_blueprint(movie_blueprint)
app.register_blueprint(actor_blueprint)


if __name__ == "__main__":
    app.run(debug=True)
