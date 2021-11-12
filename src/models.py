from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favPeople = db.relationship('FavPeople', backref='user', lazy=True)
    favPlanet = db.relationship('FavPlanet', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=True)
    haircolor = db.Column(db.String(50), nullable=True)
    eyescolor = db.Column(db.String(50), nullable=True)
    favPeople = db.relationship('FavPeople', backref='people', lazy=True)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "haircolor": self.haircolor,
            "eyescolor": self.eyescolor
        }

class Planet(db.Model):
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    population = db.Column(db.Integer, nullable=True)
    terrain = db.Column(db.String(50), nullable=True)
    favPlanet = db.relationship('FavPlanet', backref='planet', lazy=True)
    
    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain
        }

class FavPeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('user.id'))
    idPeople = db.Column(db.Integer, db.ForeignKey('people.id'))

    def serialize(self):
        return {
            "id": self.id,
            "idUser": self.idUser,
            "idPeople": self.idPeople
        }

class FavPlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('user.id'))
    idPlanet = db.Column(db.Integer, db.ForeignKey('planet.id'))

    def serialize(self):
        return {
            "id": self.id,
            "idUser": self.idUser,
            "idPlanet": self.idPlanet
        }