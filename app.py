from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate, exceptions


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@localhost/lab6-db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


class Travels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, unique=False)
    name = db.Column(db.String(80), unique=False)
    producer = db.Column(db.String(80), unique=False)

    def __init__(self, price, name, producer):
        self.price = price
        self.name = name
        self.producer = producer


def get_travel_by_id(id):
    travel = Travels.query.get(id)
    if travel is None:
        return abort(404)
    return travel


@app.errorhandler(exceptions.ValidationError)
def handle_exception(e):
    return e.messages, 400


class TravelSchema(ma.Schema):
    price = fields.Float(validate=validate.Range(min=0))
    name = fields.String(validate=validate.Length(max=80))
    producer = fields.String(validate=validate.Length(max=80))


travel_schema = TravelSchema()
travels_schema = TravelSchema(many=True)


@app.route('/post', methods=['POST'])
def add_post():
    fields = travel_schema.load(request.json)
    new_travel = Travels(**fields)

    db.session.add(new_travel)
    db.session.commit()

    return travel_schema.jsonify(new_travel)


@app.route('/get', methods=['GET'])
def get_post():
    all_travels = Travels.query.all()
    result = travels_schema.dump(all_travels)

    return jsonify(result)


@app.route('/get/<id>/', methods=['GET'])
def travel_details(id):
    travel = get_travel_by_id(id)
    return travel_schema.jsonify(travel)


@app.route('/post_update/<id>', methods=['PUT'])
def post_update(id):
    post = get_travel_by_id(id)
    fields = travel_schema.load(request.json)
    post.update(**fields)

    db.session.commit()
    return travel_schema.jsonify(post)


@app.route('/post_delete/<id>', methods=['DELETE'])
def post_delete(id):
    post = get_travel_by_id(id)

    db.session.delete(post)
    db.session.commit()

    return travel_schema.jsonify(post)


if __name__ == "main":
    app.run(debug=True)