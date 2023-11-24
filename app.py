"""
Flask app entry point
"""

from flask import Flask
from blueprints.health.blueprint import health_blueprint
from db.Connection import Connection

app = Flask(__name__)

conn = Connection()
app.conn = conn


# registers the blueprints
app.register_blueprint(health_blueprint)


if __name__ == "__main__":
    app.run(debug=True)
