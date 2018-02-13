"""Models and database functions for polygons db."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db_uri = "postgres:///polygons"


class Poly(db.Model):
    """Polygon model."""

    __tablename__ = "polygons"

    poly_id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Vertex(db.Model):
    """Vertex model."""

    __tablename__ = "vertices"

    vertex_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    poly_id = db.Column(db.Integer, db.ForeignKey("polygons.poly_id"))
    x1 = db.Column(db.Float)
    y1 = db.Column(db.Float)
    x2 = db.Column(db.Float)
    y2 = db.Column(db.Float)
    next_id = db.Column(db.Integer, db.ForeignKey("vertices.vertex_id"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Vertex {} Polygon {} (x1, y1)=({}, {}) (x2, y2)=({}, {})>"
                .format(self.vertex_id,
                        self.poly_id,
                        self.x1,
                        self.y1,
                        self.x2,
                        self.y2))


def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")


def connect_to_db(app, uri=db_uri):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")
