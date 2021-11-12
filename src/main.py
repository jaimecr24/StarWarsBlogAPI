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

#Return all people
@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))
    return jsonify(all_people), 200

#GET, POST, PUT, DELETE one elem of People
@app.route('/people/<int:people_id>', methods=['GET','POST','DELETE','PUT'])
def get_people_n(people_id):

    person = People.query.get(people_id)
    if request.method == 'GET':
        if person is None:
            return "error: ID people not exists",400
        else:
            return jsonify(person.serialize()), 200

    elif request.method == 'POST':
        if person:
            return "Error: ID already exists",400
        body = request.get_json()
        if body is None:
            return "The request body is null",400
        elif 'name' not in body:
            return "You need to specify the name" ,400
        else:
            person = People(
                id=people_id,
                name=body.get("name"),
                gender=body.get("gender"),
                haircolor=body.get("haircolor"),
                eyescolor=body.get("eyescolor")
            )
            db.session.add(person)
            db.session.commit()
            return f"POST {person.serialize()} added ok",200

    elif request.method == 'PUT':
        if person is None:
            return "error: ID people not exists",400
        body = request.get_json()
        if body is None:
            return "The request body is null",400
        elif 'name' not in body:
            return "You need to specify the name",400
        else:
            person.name = body.get("name")
            person.gender = body.get("gender")    
            person.haircolor = body.get("haircolor")
            person.eyescolor = body.get("eyescolor")
            db.session.commit()
            return f"PUT {person.serialize()} updated ok",200

    else:
        if person is None:
            return "error: ID people not exists",400
        else:
            db.session.delete(person)
            db.session.commit()
            return f"People {people_id} deleted ok",200

#Return all planets
@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))
    return jsonify(all_planets), 200

#GET, POST, PUT, DELETE one elem of Planets
@app.route('/planet/<int:planet_id>', methods=['GET','POST','PUT','DELETE'])
def get_planet_n(planet_id):

    planet = Planet.query.get(planet_id)
    if request.method == 'GET':
        if planet is None:
            return "error: ID planet not exists",400
        else:
            return jsonify(planet.serialize()), 200

    elif request.method == 'POST':
        if planet:
            return "Error: ID already exists",400
        body = request.get_json()
        if body is None:
            return "The request body is null",400
        elif 'name' not in body:
            return "You need to specify the name" ,400
        else:
            planet = Planet(
                id=planet_id,
                name=body.get("name"),
                population=body.get("population"),
                terrain=body.get("terrain")
            )
            db.session.add(planet)
            db.session.commit()
            return f"POST {planet.serialize()} added ok",200

    elif request.method == 'PUT':
        if planet is None:
            return "error: ID planet not exists",400
        body = request.get_json()
        if body is None:
            return "The request body is null",400
        elif 'name' not in body:
            return "You need to specify the name",400
        else:
            planet.name = body.get("name")
            planet.population = body.get("population")    
            planet.terrain = body.get("terrain")
            db.session.commit()
            return f"PUT {planet.serialize()} updated ok",200

    else:
        if planet is None:
            return "error: ID planet not exists",400
        else:
            db.session.delete(planet)
            db.session.commit()
            return f"People {planet_id} deleted ok",200

#Return all users
@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))
    return jsonify(all_users), 200

#Return favorite people and planets of active user
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

#Add/Delete the planet to favorites of active user
@app.route('/favorite/planet/<int:planet_id>', methods=['POST','DELETE'])
def add_favplanet_user(planet_id):
    activ_user = User.query.filter_by(is_active=True).first()
    if activ_user is None:
        return jsonify({"msg": "No user active"}), 401
    else:
        planet = Planet.query.get(planet_id)
        if planet is None:
            return "Error: Id planet not exists",400
        if request.method == 'POST':
            favplanet = FavPlanet.query.filter_by(idUser=activ_user.id, idPlanet=planet_id).first()
            if favplanet:
                return f"Error: Planet {planet_id} already exists in favorite planets of user {activ_user.id}",400
            favplanet = FavPlanet(idUser=activ_user.id, idPlanet=planet_id)
            db.session.add(favplanet)
            db.session.commit()
            return jsonify({"favorite planet added": activ_user.email+" - "+str(planet_id)}), 200
        else:
            favplanet = FavPlanet.query.filter_by(idUser=activ_user.id, idPlanet=planet_id).first()
            if favplanet is None:
                return jsonify({"error":"favorite not exists"}), 401
            else:
                db.session.delete(favplanet)
                db.session.commit()
                return jsonify({"favorite planet deleted": activ_user.email+" - "+str(planet_id)}), 200

#Add/Delete the people to favorites of active user    
@app.route('/favorite/people/<int:people_id>', methods=['POST','DELETE'])
def add_favpeople_user(people_id):
    activ_user = User.query.filter_by(is_active=True).first()
    if activ_user is None:
        return jsonify({"msg": "No user active"}), 401
    else:
        people = People.query.get(people_id)
        if people is None:
            return "Error: Id people not exists",400
        if request.method == 'POST':
            favpeople = FavPeople.query.filter_by(idUser=activ_user.id, idPeople=people_id).first()
            if favpeople:
                return f"Error: People {people_id} already exists in favorite people of user {activ_user.id}",400
            favpeople = FavPeople(idUser=activ_user.id, idPeople=people_id)
            db.session.add(favpeople)
            db.session.commit()
            return jsonify({"favorite people added":activ_user.email+" - "+str(people_id)}), 200
        else:
            favpeople = FavPeople.query.filter_by(idUser=activ_user.id, idPeople=people_id).first()
            if favpeople is None:
                return jsonify({"error":"favorite not exists"}), 401
            else:
                db.session.delete(favpeople)
                db.session.commit()
                return jsonify({"favorite people deleted": activ_user.email+" - "+str(people_id)}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
