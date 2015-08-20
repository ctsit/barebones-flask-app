"""
Goal: Load settings, configure logging, load application routing

@authors:
    Andrei Sura             <sura.andrei@gmail.com>
    Ruchi Vivek Desai       <ruchivdesai@gmail.com>
    Sanath Pasumarthy       <sanath@ufl.edu>
    Nicholas Rejack         <nrejack@ufl.edu>
"""

import os
import sys
import ssl
import logging
from logging import Formatter
import config


def _load_confidential_settings(app):
    """ Read the confidential settings such as db passwords... """

    if 'CONFIDENTIAL_SETTINGS_FILE' not in app.config:
        err = "The default config should specify: CONFIDENTIAL_SETTINGS_FILE"
        app.logger.error(err)
        sys.exit(err)

    confidential_file = app.config['CONFIDENTIAL_SETTINGS_FILE']

    if not os.path.isabs(confidential_file):
        err = "The CONFIDENTIAL_SETTINGS_FILE should be specified" \
            "using an absolute path"
        app.logger.error(err)
        sys.exit(err)

    if os.access(confidential_file, os.R_OK):
        app.config.from_pyfile(confidential_file)
        # app.logger.debug("Loaded config from: {}" .format(confidential_file))
    else:
        err = "The confidential_file: [{}] is not readable. "\
            .format(confidential_file)
        app.logger.error(err)
        sys.exit(err)


def _check_config(app):
    """
    @TODO: add more extensive checks
    """
    upload_dirs = ['/dir1', '/dir2']

    for directory in upload_dirs:
        if not os.access(directory, os.R_OK):
            sys.exit(
                "Please check if '{}' dir exists and it is accessible"
                .format(directory))


def do_init(app, mode=config.MODE_PROD, extra_settings={}):
    """
    Initialize the app.

    :rtype Flask
    :return the initialized application object
    """

    if mode == config.MODE_PROD:
        app.config.from_object(config.DefaultConfig)
        print("Loaded default config")
    elif mode == config.MODE_TEST:
        app.config.from_object(config.TestConfig)
        # print("Loaded test config")
    elif mode == config.MODE_DEBUG:
        app.config.from_object(config.DebugConfig)
        # print("Loaded debug config")

    _configure_logging(app)
    _load_confidential_settings(app)
    # _check_config(app)

    # When running unit tests we use in-memory sqlite
    if mode == config.MODE_TEST:
        DATABASE_PATH = os.path.abspath('tests.db')

        # If we want to inspect the results we can use a file instead of memory
        run_fast = True
        if run_fast:
            SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        else:
            SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
    else:
        SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}' \
            .format(app.config['DB_USER'],
                    app.config['DB_PASS'],
                    app.config['DB_HOST'],
                    app.config['DB_NAME'])

    # After we read the confidential settings we can build the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    # app.logger.debug("get_config_summary: {}".format(get_config_summary(app)))

    if len(extra_settings):
        # Override with special settings (example: tests/conftest.py)
        app.logger.info("Load extra config params using do_init()")
        app.config.update(extra_settings)

    # load routes
    from app.routes import pages
    from app.routes import users
    from app.routes import api

    if app.debug and app.config['DEBUG_TB_ENABLED'] and not app.testing:
        # When runing tests there is no need for the debugtoolbar
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)
    return app


def _configure_logging(app):
    """
    Set the log location and formatting
    @see http://flask.pocoo.org/docs/0.10/errorhandling/
    """
    debug_level = app.config['LOG_LEVEL']
    handler = logging.StreamHandler()
    fmt = Formatter('%(asctime)s %(levelname)s: '
                    '%(message)s [%(filename)s +%(lineno)d]')
    handler.setFormatter(fmt)
    handler.setLevel(debug_level)
    # print("_configure_logging() set debug level to: {}".format(debug_level))
    app.logger.addHandler(handler)


def get_config_summary(app):
    """ Helper method for debugging configuration """

    database_url = ''
    if app.debug:
        database_url = "{}" .format(app.config['SQLALCHEMY_DATABASE_URI'])

    data = {
        "Debug mode": app.debug,
        "Testing mode": app.testing,
        "Secret key length": len(app.config['SECRET_KEY']),
        "Database url": database_url,
    }
    return data


def get_ssl_context(app):
    """
    Get a SSL context in debug mode if the developer does not provide the
    public/private key files for the certificate.
    Note: In production mode we specify the "SSL context" by configuring Apache

    @see http://werkzeug.pocoo.org/docs/0.10/serving/#quickstart
    """
    ssl_public_key_file = app.config['SERVER_SSL_CRT_FILE']
    ssl_private_key_file = app.config['SERVER_SSL_KEY_FILE']
    ssl_context = None

    if os.path.isfile(ssl_public_key_file) and \
            os.path.isfile(ssl_private_key_file):
        try:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.load_cert_chain(ssl_public_key_file,
                                        ssl_private_key_file)
            print('Using ssl certificate {}'
                  .format(ssl_public_key_file))
        except Exception as exc:
            sys.exit("Problem loading SSL certificate: {}".format(exc))
    else:
        print("Could not read ssl cert/key: \n\t{}\n\t{}"
              .format(ssl_public_key_file, ssl_private_key_file))

        if app.debug:
            try:
                # if the pyOpenSSL is installed use the adhoc ssl context
                import OpenSSL
                ssl_context = 'adhoc'
                print("Using the adhoc ssl_context from OpenSSL {}"
                      .format(OpenSSL.__version__))
            except Exception as exc:
                print("Please execute 'pip install pyOpenSSL'"
                      "to test and adhoc ssl context. {}".format(exc))
        else:
            sys.exit('Please run in debug mode if you want to test an adhoc'
                     ' certificate.')

    return ssl_context
