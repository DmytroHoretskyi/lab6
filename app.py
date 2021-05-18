from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@localhost/lab6-db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


class Travels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, unique=False)
    name = db.Column(db.String(100))
    producer = db.Column(db.String(100))

    def __init__(self, price, name, producer):
        self.price = price
        self.name = name
        self.producer = producer


class TravelShcema(ma.Schema):
    class Meta:
        fields = ("price", "name", "producer")


travel_schema = TravelShcema()
travels_schema = TravelShcema(many=True)


@app.route('/post', methods=['POST'])
def add_post():
    price = request.json['price']
    name = request.json['name']
    producer = request.json['producer']

    my_posts = Travels(price, name, producer)
    db.session.add(my_posts)
    db.session.commit()

    return travel_schema.jsonify(my_posts)


@app.route('/get', methods=['GET'])
def get_post():
    all_travels = Travels.query.all()
    result = travels_schema.dump(all_travels)

    return jsonify(result)


@app.route('/get/<id>/', methods=['GET'])
def travel_details(id):
    travel = Travels.query.get(id)
    return travel_schema.jsonify(travel)


@app.route('/post_update/<id>', methods=['PUT'])
def post_update(id):
    post = Travels.query.get(id)

    price = request.json['price']
    name = request.json['name']
    producer = request.json['producer']

    post.price = price
    post.name = name
    post.producer = producer

    db.session.commit()
    return travel_schema.jsonify(post)


@app.route('/post_delete/<id>', methods=['DELETE'])
def post_delete(id):
    post = Travels.query.get(id)
    db.session.delete(post)
    db.session.commit()

    return travel_schema.jsonify(post)


if __name__ == "main":
    app.run(debug=True)