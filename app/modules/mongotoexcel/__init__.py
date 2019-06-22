from flask import Blueprint, render_template, abort, request, url_for
from jinja2 import TemplateNotFound

mongotoexcel = Blueprint('mongotoexcel', __name__, template_folder='templates')




@mongotoexcel.route('/', defaults={'page': 'index'})
@mongotoexcel.route('/<page>')
def mongotoexcel_main(page):
    pagelinks = [{'href': url_for('main_page'), 'text': 'Home'},
                 {'href': url_for('mongotoexcel.mongotoexcel_main'), 'text': 'Export from MongoDB'},
                 {'href': url_for('parserxml.parserxml_main'), 'text': 'Parse input File'}]
    try:
        print(page)
        return render_template("mongotoexcel/index.html", title='Main', pagelinks=pagelinks), 200
    except TemplateNotFound:
        abort(404)

@mongotoexcel.route("/submitMongo", methods=['GET', 'POST'])
def submittedForm():
    print(request.form['email'])
    return "Thanks ", 200
