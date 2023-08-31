import time
import inject
from flask import Flask, g, jsonify
from werkzeug.utils import import_string

from config import configure_fromfile, PersonSession


def init_app(blueprints):
    inject.configure(configure_fromfile)
    app = Flask(__name__)

    @app.before_request
    def before_request():
        g.start = time.time()
        g.user = {}

    @app.teardown_request
    def clear_session(exception):
        del exception
        inject.instance(PersonSession).remove()

    with app.app_context():
        for bp_name in blueprints:
            bp = import_string(bp_name)
            app.register_blueprint(bp)

    return app
