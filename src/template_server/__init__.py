from flask import Flask

from . import config


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    config.instance_pth.mkdir(exist_ok=True)

    # 跨域支持
    from flask_cors import CORS
    CORS(app, supports_credentials=True)

    dev_db = config.instance_pth / 'dev.sqlite'
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{dev_db.absolute()}'
    )
    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile('config.py', silent=True)

    from . import models
    models.init_app(app)

    from . import home
    home.init_app(app)

    return app


app = create_app()
app.app_context().push()
