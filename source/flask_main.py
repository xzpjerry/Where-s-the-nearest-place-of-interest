"""
Flask web site with vocabulary matching game
(identify vocabulary words that can be made 
from a scrambled string)
"""

import flask
import logging
from os import path
import sys
sys.path.insert(0, './../Config_data/')

# my modules

import config

###
# Globals
###
app = flask.Flask(__name__)

CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY  # Should allow using session variables
data_file = CONFIG.DATAFILE
PLACE_OF_INTERESTS = config.get_place_of_interest(data_file)
#
# One shared 'Vocab' object, read-only after initialization,
# shared by all threads and instances.  Otherwise we would have to
# store it in the browser and transmit it on each request/response cycle,
# or else read it from the file on each request/responce cycle,
# neither of which would be suitable for responding keystroke by keystroke.



###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    """The main page of the application"""
    return flask.render_template('main.html')


###############
# AJAX request handlers
#   These return JSON, rather than rendering pages.
###############

@app.route("/_places")
def get_places():
    rslt = {'len':len(PLACE_OF_INTERESTS), 'places': PLACE_OF_INTERESTS}
    return flask.jsonify(result=rslt)

@app.route("/_token")
def get_token_with_address():
    """
    Example ajax request handler
    """
    app.logger.debug("Got a JSON request: " + CONFIG.ADDRESS + CONFIG.TOKEN)
    rslt = {"maprequest": CONFIG.ADDRESS + CONFIG.TOKEN}
    return flask.jsonify(result=rslt)


#################
# Functions used within the templates
#################

@app.template_filter('filt')
def format_filt(something):
    """
    Example of a filter that can be used within
    the Jinja2 code
    """
    return "Not what you asked for"

###################
#   Error handlers
###################


@app.errorhandler(404)
def error_404(e):
    app.logger.warning("++ 404 error: {}".format(e))
    return flask.render_template('404.html'), 404


@app.errorhandler(500)
def error_500(e):
    app.logger.warning("++ 500 error: {}".format(e))
    assert not True  # I want to invoke the debugger
    return flask.render_template('500.html'), 500


@app.errorhandler(403)
def error_403(e):
    app.logger.warning("++ 403 error: {}".format(e))
    return flask.render_template('403.html'), 403


####

if __name__ == "__main__":
    if CONFIG.DEBUG:
        app.debug = True
        app.logger.setLevel(logging.DEBUG)
        app.logger.info(
            "Opening for global access on port {}".format(CONFIG.PORT))
        app.run(port=CONFIG.PORT, host="0.0.0.0")
