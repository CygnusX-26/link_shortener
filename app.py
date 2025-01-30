from flask import Flask, redirect, request
from flask_httpauth import HTTPBasicAuth
from models import db, Link
from dotenv import load_dotenv
from os import getenv
import re
from utils import gen_path, test_valid
from db import add_url, get_url, check_path

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
HOME_URL = "https://blog.neilhommes.xyz"
URL = getenv("URL", "http://localhost:5000/")
gen_url = lambda path: f'{URL}{path}'

load_dotenv()

USER = {
    "admin": getenv("ADMIN_AUTH")
}

def init_db():
    db.init_app(app)
    with app.app_context():
        db.create_all()

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
        return "Invalid Url"
    
    possible = check_path(url)
    if possible is not None:
        return gen_url(possible.path)

    path = gen_path()
    add_url(url, path)
    return gen_url(path)

@auth.verify_password
def verify(username, password):
    try:
        return username if USER[username] == password else None
    except KeyError:
        return None


if __name__ == '__main__':
    init_db()
    app.run('0.0.0.0', 5000, debug=False, load_dotenv=True)