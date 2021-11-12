"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, FavPeople, FavPlanet

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))
    return jsonify(all_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_n(people_id):
    person = People.query.get(people_id)
    return jsonify(person.serialize())

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))
    return jsonify(all_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_n(planet_id):
    myplanet = Planet.query.get(planet_id)
    return jsonify(myplanet.serialize()), 200

@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))
    return jsonify(all_users), 200

@app.route('/users/favorites', methods=['GET'])
def get_favorites_user():
    activ_user = User.query.filter_by(is_active=True).first()
    if activ_user is None:
        return jsonify({"msg": "No user active"}), 401
    else:
        fav_people = FavPeople.query.filter_by(idUser=activ_user.id)
        all_fav = []
        for fav in fav_people:
            p = People.query.filter_by(id=fav.idPeople).first()
            all_fav.append(p.serialize())
        fav_planet = FavPlanet.query.filter_by(idUser=activ_user.id)
        for fav in fav_planet:
            p = Planet.query.filter_by(id=fav.idPlanet).first()
            all_fav.append(p.serialize())

        return jsonify(all_fav), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST','DELETE'])
def add_favplanet_user(planet_id):
    activ_user = User.query.filter_by(is_active=True).first()
    if activ_user is None:
        return jsonify({"msg": "No user active"}), 401
    else:
        if request.method == 'POST':
            favplanet = FavPlanet(idUser=activ_user.id, idPlanet=planet_id)
            db.session.add(favplanet)
            db.session.commit()
            return jsonify({"favorite planet added": activ_user.email+" - "+str(planet_id)})
        else:
            favplanet = FavPlanet.query.filter_by(idUser=activ_user.id, idPlanet=planet_id).first()
            if favplanet is None:
                return jsonify({"error":"favorite not exists"}), 401
            else:
                db.session.delete(favplanet)
                db.session.commit()
                return jsonify({"favorite planet deleted": activ_user.email+" - "+str(planet_id)})
        
@app.route('/favorite/people/<int:people_id>', methods=['POST','DELETE'])
def add_favpeople_user(people_id):
    activ_user = User.query.filter_by(is_active=True).first()
    if activ_user is None:
        return jsonify({"msg": "No user active"}), 401
    else:
        if request.method == 'POST':
            favpeople = FavPeople(idUser=activ_user.id, idPeople=people_id)
            db.session.add(favpeople)
            db.session.commit()
            return jsonify({"favorite people added":activ_user.email+" - "+str(people_id)})
        else:
            favpeople = FavPeople.query.filter_by(idUser=activ_user.id, idPeople=people_id).first()
            if favpeople is None:
                return jsonify({"error":"favorite not exists"}), 401
            else:
                db.session.delete(favpeople)
                db.session.commit()
                return jsonify({"favorite people deleted": activ_user.email+" - "+str(people_id)})

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
