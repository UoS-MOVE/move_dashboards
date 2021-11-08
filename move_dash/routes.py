"""

"""


__author__ = "Ethan Bellmer"
__version__ = "0.1"


"""Routes for parent Flask app."""
from flask import render_template
from flask import current_app as app


@app.route('/')
def home():
    """Landing page."""
    return render_template(
        'index.jinja2',
        title='MOVE Dashboard',
        description='Prototype for the MOVE Dashboard.',
        template='home-template',
        body="This is a homepage served with Flask."
    )