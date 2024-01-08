# /fcc/__init__.py

import logging
import re

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config_all.py')
    if app.config['DEBUG']:
        app.config.from_pyfile('config_dev.py')
    else:
        app.config.from_pyfile('config_prod.py')

    _config_logging()

    #
    # Database
    #

    from fcc.models import db
    db.init_app(app)

    #
    # Blueprints
    #

    from fcc.blues.routes import bp as routes_bp  # TO DO: change to 'pages'
    app.register_blueprint(routes_bp)
    from fcc.blues.cli import bp as cli_bp
    app.register_blueprint(cli_bp)

    #
    # Template Filters
    #

    @app.template_filter('strip_http')
    def strip_http(url):
        return re.sub(r'^https?://', '', url)

    return app


def _config_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'    
    )

    # (Maybe one day I'll do something more sophisticated here...)