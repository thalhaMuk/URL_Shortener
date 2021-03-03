from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    # Since we are using flash we will be using secret_key to hide the message from other so that only the user can
    # see it
    app.secret_key = 'SomethingGibberish'  # In production have to make this something hard to guess

    from . import urlshort
    app.register_blueprint(urlshort.bp)

    return app
