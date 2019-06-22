from flask import Flask, render_template, flash, url_for
from .modules import *

# Import SQLAlchemy
#from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)
app.config.from_object('config')

from app.modules.mongotoexcel import mongotoexcel
from app.modules.parserxml import parserxml
from app.modules.loggersetup import loggersetup


app.register_blueprint(mongotoexcel, url_prefix="/mongotoexcel")
app.register_blueprint(parserxml, url_prefix="/parserxml")

@app.errorhandler(404)
def not_found(error):
    print(app.config)
    return "Oopsie daisy" , 404

@app.route("/")
@app.route("/index.html")
def main_page():
    pagelinks = [{'href': url_for('main_page'), 'text': 'Home'},
                 {'href': url_for('mongotoexcel.mongotoexcel_main'), 'text': 'Export from MongoDB'},
                 {'href': url_for('parserxml.parserxml_main'), 'text': 'Parse input File'}]

    flash("A request for main page is received. Thanks.")
    logger = loggersetup.LoggerSetup("XML_PARSER_" + app.config["APPVERSION"] , 20 * 1024 * 1024, 10)
    logger = logger.run()
    logger.info("This is a test message")

    return render_template("index.html", title='Main', pagelinks = pagelinks), 200