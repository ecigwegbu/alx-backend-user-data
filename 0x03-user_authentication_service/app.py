#!/usr/bin/env python3
"""
Basic Flask app that returns a BienVenue message
"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def root_route() -> str:
    """ GET Home Page of the app
    Return:
        - Welcome Page
    """
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
