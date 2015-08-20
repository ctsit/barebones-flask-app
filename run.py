#!/usr/bin/env python
"""
Goal: Implement the application entry point

@authors:
    Andrei Sura             <sura.andrei@gmail.com>
    Ruchi Vivek Desai       <ruchivdesai@gmail.com>
    Sanath Pasumarthy       <sanath@ufl.edu>
    Nicholas Rejack         <nrejack@ufl.edu>
"""

import argparse
from app.main import app, mail
from app import initializer
from config import MODE_DEBUG

# Configures routes, models
app = initializer.do_init(app, mode=MODE_DEBUG)
mail.init_app(app)


if __name__ == "__main__":
    """ Entry point for command line execution """
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',
                        dest='port',
                        type=int,
                        default=5000,
                        help="Application port number")
    args = parser.parse_args()
    ssl_context = initializer.get_ssl_context(app)
    print("curl -skL https://localhost:{}".format(args.port))
    app.run(host='0.0.0.0', port=args.port, ssl_context=ssl_context)
