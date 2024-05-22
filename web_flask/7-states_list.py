#!/usr/bin/python3
"""Script that starts a Flask web application"""
from flask import Flask, render_template

from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """The states_list page."""
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(exc):
    """The Flask app/request context end event listener."""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
