from flask import Blueprint, render_template, abort, request
import threading
import shutil
from jinja2 import TemplateNotFound
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from zipfile import ZipFile
from .parserxml import  ParserXML

UPLOAD_FOLDER = 'uploadedfiles' #this is the folder where we will copy our uploaded files
ZIP_EXTRACT_FOLDER = 'zipextract' #this is the folder where we will extract our zip files
ALLOWED_EXTENSIONS = {'zip'} #this is set literal. to remove any duplicates by mistake
FILEFIELD = 'inputxml'

PARSERTHREADNAME = "parserxml0x1942"
FORM_DATEFILTER_SWITCH = "datefiltercustom"
FORM_DATE_CUSTOM = "customdate"
FORM_EXPORT_AS_DB_SWITCH = "exportasdb"
FORM_IMPORT_TO_MONGO_SWITCH = "inserttomongo"

parserxml = Blueprint('parserxml', __name__, template_folder='templates')

#def __init__(self, logger, CUSTOM_DATE_FILTER="",
#                 EXPORT_DB=True, INSERT_MONGO=False,
#                 DUMPDIR="/home/aamhabiby/Desktop/resources/TEST/",
#                 EXPORT_DIR="/home/aamhabiby/Desktop/resources/"):


@parserxml.route('/', defaults={'page': 'index'})
@parserxml.route('/<page>')
def parserxml_main(page):
    pagelinks = [{'href': url_for('main_page'), 'text': 'Home'},
                 {'href': url_for('mongotoexcel.mongotoexcel_main'), 'text': 'Export from MongoDB'},
                 {'href': url_for('parserxml.parserxml_main'), 'text': 'Parse input File'}]

    for x in threading.enumerate():
        if PARSERTHREADNAME in x.name:
            if x.is_alive() == True:
                st_int, st_str, st_log, st_config = x.status()
                return redirect(url_for("parserxml.parserxml_status"), 302)
    try:
        return render_template("parserxml/index.html", title='Main', pagelinks=pagelinks), 200
    except TemplateNotFound:
        abort(404)

@parserxml.route('/status')
def parserxml_status():
    pagelinks = [{'href': url_for('main_page'), 'text': 'Home'},
                 {'href': url_for('mongotoexcel.mongotoexcel_main'), 'text': 'Export from MongoDB'},
                 {'href': url_for('parserxml.parserxml_main'), 'text': 'Parse input File'}]

    for x in threading.enumerate():
        print(x)
        if PARSERTHREADNAME in x.name:
            if x.is_alive() == True:
                st_int, st_str, st_log, st_config = x.status()
                return render_template("parserxml/status.html", title="ParserXML", parserstatus=st_str,
                                       parserlogs=st_log, pagelinks=pagelinks, parserconfig=st_config,
                                       parserprogress=st_int)

    return render_template("parserxml/status.html", title="ParserXML", parserstatus="NOT RUNNING",
                                       parserlogs="No logs available",
                           pagelinks=pagelinks,
                           parserconfig="Parser not running",
                           parserprogress=100)


@parserxml.route("/submitparams", methods=['POST'])
def submittedForm():
    pagelinks = [{'href': url_for('main_page'), 'text': 'Home'},
                 {'href': url_for('mongotoexcel.mongotoexcel_main'), 'text': 'Export from MongoDB'},
                 {'href': url_for('parserxml.parserxml_main'), 'text': 'Parse input File'}]
    if request.method == "POST":
        print(request.form)
        #print("I m here post")
        if FILEFIELD not in request.files:
            print("File field not found in request.", request.files)
            return redirect(request.url)
        file = request.files[FILEFIELD]
        retPath = getUploadedFile(file)
        if retPath == -1:

            return '''<title>No File Uploaded</title><body>Please upload a file to continue</body>''',200
        elif retPath == -2:
            return '''<title>Error Uploading File</title><body>An error ocurred while trying to upload the file</body>''', 403
        else:
            param_DATEFILTER = ""
            param_EXPORTASDB = True
            param_INSERTMONGO = False
            if FORM_DATEFILTER_SWITCH not in request.form:
                if FORM_DATE_CUSTOM in request.form:
                    try:
                        dVal = int(request.form[FORM_DATE_CUSTOM])
                        param_DATEFILTER = str(dVal)
                    except:
                        param_DATEFILTER = ""
                else:
                    param_DATEFILTER = ""
            else:
                param_DATEFILTER = "" ## Bad coding here. Please improve



            if FORM_EXPORT_AS_DB_SWITCH not in request.form:
                param_EXPORTASDB = False
            elif request.form[FORM_EXPORT_AS_DB_SWITCH].lower() == "on":
                param_EXPORTASDB = True
            else:
                param_EXPORTASDB = False
            if FORM_IMPORT_TO_MONGO_SWITCH not in request.form:
                param_INSERTMONGO = False
            elif request.form[FORM_IMPORT_TO_MONGO_SWITCH].lower() == "on":
                param_INSERTMONGO = True
            else:
                param_INSERTMONGO = False
            if (param_INSERTMONGO == True) or (param_EXPORTASDB == True):
                parser = ParserXML(logger=None, name=PARSERTHREADNAME, CUSTOM_DATE_FILTER=param_DATEFILTER,
                                   DUMPDIR=str(retPath), EXPORT_DIR=ZIP_EXTRACT_FOLDER,
                                   EXPORT_DB=param_EXPORTASDB, INSERT_MONGO=param_INSERTMONGO, isZip=True)
                parser.start()
                for x in threading.enumerate():
                    if PARSERTHREADNAME in x.name:
                        if x.is_alive() == True:
                            st_int, st_str, st_log, st_config = x.status()
                            return redirect(url_for("parserxml.parserxml_status"), 302)
    return redirect(url_for("parserxml.parserxml_status"), 302)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getUploadedFile(file):
    if file.filename == "":
        return -1
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            if os.path.exists(UPLOAD_FOLDER):
                shutil.rmtree(
                    UPLOAD_FOLDER)  # this is to make sure we delete earlier uploaded files to not process any old files
            try:
                os.makedirs(UPLOAD_FOLDER)
            except:
                print("Error creating upload folder.")
                return -2

            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
        except Exception as e:
            return -2
        return filepath
    return -2
