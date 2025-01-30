from models import db, Link

def init_db(app):
    with app.app_context():
        db.create_all()

def add_url(url:str, path:str) -> None:
    link = Link(url=url, path=path)
    db.session.add(link)
    db.session.commit()

def check_path(url: str) -> Link:
    return next((link for link in Link.query.all() if link.url == url), None)

def get_url(path: str) -> Link:
    return next((link for link in Link.query.all() if link.path == path), None)

def get_all_and_jsonify() -> str:
    s = {}
    for link in Link.query.all():
        s[link.path] = link.url
    return s

def delete_path(path: str) -> str:
    link_to_delete = Link.query.filter_by(path=path).first()
    if link_to_delete:
        db.session.delete(link_to_delete)
        db.session.commit()
        return f"Deleted."
    else:
        return f"Link not found"