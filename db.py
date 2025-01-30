from models import db, Link

def add_url(url:str, path:str) -> None:
    link = Link(url=url, path=path)
    db.session.add(link)
    db.session.commit()

def check_path(url: str) -> Link:
    return next((link for link in Link.query.all() if link.url == url), None)

def get_url(url: str) -> Link:
    return next((link for link in Link.query.all() if link.path == url), None)