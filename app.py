from flask import Flask, redirect, request
from flask_httpauth import HTTPBasicAuth
from dotenv import load_dotenv
from os import getenv
import re
from utils import gen_path, test_valid, statusify, check_password
from db import add_url, get_url, check_path, init_db, get_all_and_jsonify, delete_path
from models import db

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
HOME_URL = "https://blog.neilhommes.xyz"
URL = getenv("URL", "http://localhost:5000/")
gen_url = lambda path: f'{URL}{path}'

load_dotenv()

USER = {
    getenv("NAME"): getenv("AUTH_TOKEN")
}

@app.route("/")
def home():
    return redirect(HOME_URL)

@app.route("/<path:path_name>")
def link(path_name):
    link = get_url(path_name)
    if link is not None:
        return redirect(link.url)
    return redirect(HOME_URL)

@app.route("/create")
@auth.login_required
def create():
    url = request.args.get('url', None)
    if url == None or re.match(r"https?:\/\/[^\s/$.?#].[^\s]*", url) == None or len(url) > 499 or not test_valid(url):
        return statusify("Invalid Url", False)
    
    possible = check_path(url)
    if possible is not None:
        return statusify(gen_url(possible.path), True)

    path = gen_path()
    add_url(url, path)
    return statusify(gen_url(path), True)

@app.route("/all")
@auth.login_required
def all():
    return statusify(get_all_and_jsonify(), True)

@app.route("/delete")
@auth.login_required
def delete():
    path = request.args.get('path', None)
    if path == None:
        return statusify("Invalid or nonexistent path", False)
    return statusify(delete_path(path), True)
    


@auth.verify_password
def verify(username, password):
    try:
        return username if USER[username] and check_password(password, getenv("AUTH_TOKEN").encode()) else None
    except KeyError:
        return None

db.init_app(app)
init_db(app)