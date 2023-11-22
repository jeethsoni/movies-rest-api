"""
Flask app entry point
"""

from flask import Flask
from blueprints.health.blueprint import health_blueprint

app = Flask(__name__)

# registers the blueprints
app.register_blueprint(health_blueprint)


if __name__ == "__main__":
    app.run(debug=True)
