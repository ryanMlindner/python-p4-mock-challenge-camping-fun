from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    serialize_rules = ('-signups.activity','-signups.camper',)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    signups = db.relationship("Signup", cascade="all, delete-orphan", backref='activity') 
    
    
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    serialize_rules = ('-signups.camper', '-signups.activity',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    signups = db.relationship("Signup", cascade="all, delete-orphan", backref='camper')
    
    
    @validates('name', 'age')
    def validate_camper(self, key, entry):
        if key == 'name' :
            if entry == None or entry == '':
                raise ValueError("Camper must have a name")
        if key == 'age':    
            if entry < 8 or entry > 18:
                raise ValueError("Camper must be between 8 and 18")
        return entry
        
    
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    serialize_rules = ('-activity.signups', '-camper.signups')

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    
    
    @validates('time')
    def validate_time(self, key, time):
        if time < 0 or time > 23:
            raise ValueError("time must be between 0 and 23")
        return time
    
    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.
