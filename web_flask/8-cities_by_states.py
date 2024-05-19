#!/usr/bin/python3
"""script that starts a Flask web application"""
from flask import Flask, render_template

from models.state import State
from models import storage


app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
all_states = list(storage.all(State).values())
    all_states.sort(key=lambda x: x.name)
    for state in all_states:
        state.cities.sort(key=lambda x: x.name)
    ctxt = {
        'states': all_states
    }
    return render_template('8-cities_by_states.html', **ctxt)


@app.teardown_appcontext
def teardown(exc):
    """The Flask app/request context end event listener."""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
