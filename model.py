from app import db

class Car(db.Model):
    __tablename__ = "cars"
    id = db.Column(db.BigInteger, primary_key=True)
    model = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

class Pet(db.Model):
    __tablename__ = "pet"
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age=db.Column(db.Integer)

class Fruits(db.Model):
    __tablename__ = "fruits"
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    number=db.Column(db.Integer)