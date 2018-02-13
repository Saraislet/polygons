from random import random
from math import sqrt
from sqlalchemy import func
from progress.bar import Bar
from model import (Poly, Vertex, db, connect_to_db)


def make_triangle(poly_id, initial_vertex_id):

    db.session.add(Poly(poly_id=poly_id))
    db.session.commit()

    x2 = random()
    y2 = random()
    next_id = None
    vertex_id = initial_vertex_id

    for i in range(3):
        x1 = random()
        y1 = random()

        vertex = Vertex(vertex_id=vertex_id,
                        poly_id=poly_id,
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2,
                        next_id=next_id)
        db.session.add(vertex)
        db.session.commit()

        x2 = x1
        y2 = y1
        next_id = vertex_id
        vertex_id += 1


def make_triangles(num):
    poly_id = 1 + db.session.query(func.max(Poly.poly_id)).first()[0]
    vertex_id = 1 + db.session.query(func.max(Vertex.vertex_id)).first()[0]

    for i in range(num):
        make_triangle(poly_id, vertex_id)
        poly_id += 1
        vertex_id += 3


def calculate_poly_lengths(poly_id):
    query = ("SELECT x1, y1, x2, y2 FROM vertices WHERE poly_id=:poly_id")
    vertices = db.session.execute(query, {"poly_id": poly_id}).fetchall()

    lengths = []

    for (x1, y1, x2, y2) in vertices:
        length = sqrt( (x2-x1)**2 + (y2-y1)**2 )
        lengths.append(length)


def calculate_poly_lengths_alt(poly_id):
    query = """SELECT a.x1, a.y1, b.x1, b.y1
               FROM vertices a
               JOIN vertices b ON (a.next_id = b.vertex_id)
               WHERE a.poly_id=:poly_id"""
    vertices = db.session.execute(query, {"poly_id": poly_id}).fetchall()

    lengths = []

    for (x1, y1, x2, y2) in vertices:
        length = sqrt( (x2-x1)**2 + (y2-y1)**2 )
        lengths.append(length)


def calculate_lengths(num):
    count_polys = Poly.query.count()
    num_polys = min(num, count_polys)

    query = ("SELECT poly_id FROM polygons")
    poly_ids = db.session.execute(query).fetchmany(num_polys)
    poly_ids = [poly_id[0] for poly_id in poly_ids]

    msg = "Calculating {} lengths: ".format(num_polys)
    suffix = "avg %(avg)1.4f s each, %(elapsed)1.2f seconds elapsed."
    bar1 = Bar(msg, max=num_polys, suffix=suffix)

    for poly_id in poly_ids:
        calculate_poly_lengths(poly_id)
        bar1.next()
    bar1.finish()

    bar2 = Bar(msg, max=num_polys, suffix=suffix)

    for poly_id in poly_ids:
        calculate_poly_lengths_alt(poly_id)
        bar2.next()
    bar2.finish()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")
