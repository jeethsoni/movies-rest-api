"""
Flask app entry point
"""

import emoji
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException, default_exceptions
from blueprints.health.blueprint import health_blueprint
from blueprints.movie.blueprint import movie_blueprint
from blueprints.actor.blueprint import actor_blueprint
from blueprints.genre.blueprint import genre_blueprint
from blueprints.director.blueprint import director_blueprint
from blueprints.movie_actor.blueprint import movie_actor_blueprint
from blueprints.movie_genre.blueprint import movie_genre_blueprint
from blueprints.movie_director.blueprint import movie_director_blueprint
from blueprints.movie_review.blueprint import movie_review_blueprint
from db.Connection import Connection
from logger import logger
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
logger = logger.configure_logger("default", "logs/flask.log")

# pushes the application context
ctx = app.app_context()
ctx.push()

app.logger = logger

# creates a Connection instance stores it in app.conn
conn = Connection()
app.conn = conn


def register_error_handler(app):
    """
    registers error handler
    """

    # global error handler for HTTP errors
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
app.register_blueprint(director_blueprint)
app.register_blueprint(genre_blueprint)
app.register_blueprint(movie_actor_blueprint)
app.register_blueprint(movie_genre_blueprint)
app.register_blueprint(movie_director_blueprint)
app.register_blueprint(movie_review_blueprint)

# registers the error handler
register_error_handler(app)


if __name__ == "__main__":
    app.run(debug=True)
