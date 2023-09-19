import time
import inject
import logging
import datetime
from flask import Flask, g, jsonify, request
from werkzeug.utils import import_string

from config import configure_fromfile, PersonSession

logger = logging.getLogger(__name__)


def print_request_params():
    log_message = '{} - - [{}] \"{} {}\"'.format(
        request.remote_addr,
        datetime.datetime.now(),
        request.method.upper(),
        request.full_path,
    )
    logger.info(log_message)


def init_app(blueprints):
    inject.configure(configure_fromfile)
    app = Flask(__name__)

    @app.before_request
    def before_request():
        g.start = time.time()
        g.user = {}
        print_request_params()

    @app.teardown_request
    def clear_session(exception):
        del exception
        inject.instance(PersonSession).remove()

    @app.after_request
    def after_request(response):
        logger.info('{} {} Execution time: {:.5} ms'.format(
            request.method.upper(), request.path, (time.time() - g.start) * 1000))
        return response

    with app.app_context():
        for bp_name in blueprints:
            bp = import_string(bp_name)
            app.register_blueprint(bp)

    return app
