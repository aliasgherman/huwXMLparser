from flask import Blueprint
from .xmldownloader import XMLDownloader

xmldownloader = Blueprint('xmldownloader', __name__)
#from .xmldownloader import XMLDownloader