# /fcc/__init__.py

import re
from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    if not app.config['DEBUG']:
        app.config.from_pyfile('live_config.py')

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
    from fcc.blues.checks import bp as checks_bp
    app.register_blueprint(checks_bp)

    #
    # Template Filters
    #

    @app.template_filter('strip_http')
    def strip_http(url):
        return re.sub(r'^https?://', '', url)
    
    @app.template_filter('to_css_class')
    def to_css_class(str):
        from unidecode import unidecode
        str1 = unidecode(str).lower()
        return re.sub(r'\s+', '-', str1)
    
    #
    # Don't ask... :-}
    #

    from fcc.lib.FileCache import FileCache
    FileCache.cache_path = app.config['FILE_CACHE_DIR']

    return app