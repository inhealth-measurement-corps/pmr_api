import os
import pymssql

from flaskr.db import get_db
from flask import Flask


def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a route that tests if db is connected
    @app.route('/hello')
    def hello():
        cursor = get_db()
        cursor.execute("SELECT mmambulation.patient_info.* FROM mmambulation.patient_info")
        print(cursor.fetchall())
        return('Connected to inHealth Database')

    #default route displays a simple message
    def index():
        return 'Hello World!'

    from . import patient
    app.register_blueprint(patient.pt)
    app.add_url_rule('/', endpoint='index', view_func=index)

    from . import unit
    app.register_blueprint(unit.ut)
    app.add_url_rule('/', endpoint='index', view_func=index)

    return app