from database import db

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Book.query.all()

    @staticmethod
    def get_by_id(id):
        return Book.query.get(id)

    def update(self, title=None, author=None, year=None):
        if title is not None:
            self.title = title
        if author is not None:
            self.author = author
        if year is not None:
            self.year = year
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
