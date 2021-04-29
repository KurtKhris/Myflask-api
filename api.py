from flask import Flask, request, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Initialize app
app = Flask(__name__,template_folder='template')
baseDir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialize db
db = SQLAlchemy(app)

#initialize Marshmallow
mar = Marshmallow(app)

#Users Class/Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    faculty = db.Column(db.String(200))
    department = db.Column(db.String(200))
    programme = db.Column(db.String(200))
    year = db.Column(db.String(100))
    image = db.Column(db.String(100))

    def __init__(self, name, faculty,department,programme,year,image):
        self.name = name
        self.faculty = faculty
        self.department = department
        self.programme = programme
        self.year = year
        self.image = image

#User Schema
class UserSchema(mar.Schema):
    class Meta:
        fields = ('id', 'name', 'faculty', 'department', 'programme', 'year', 'image' )


#initialize schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)



#Create a user
@app.route('/api/v1/user', methods=['POST'])
def addUser():
    name = request.json['name']
    faculty = request.json['faculty']
    department = request.json['department']
    programme = request.json['programme']
    year = request.json['year']
    image = request.json['image']

    newUser = Users(name, faculty, department, programme, year, image)

    db.session.add(newUser)
    db.session.commit()
    return user_schema.jsonify(newUser)


#Get all Users
@app.route('/api/v1/users/all', methods=['GET'])
def getUsers():
    allUsers = Users.query.all()
    result = users_schema.dump(allUsers)
    return jsonify(result)


#Get a single User
@app.route('/api/v1/user/<id>', methods=['GET'])
def getUser(id):
    user = Users.query.get(id)
    return user_schema.jsonify(user)


#Update user details
@app.route('/api/v1/user/<id>', methods=['PUT'])
def updateUser(id):
    user = Users.query.get(id)
    name = request.json['name']
    faculty = request.json['faculty']
    department = request.json['department']
    programme = request.json['programme']
    year = request.json['year']
    image = request.json['image']

    user.name = name
    user.faculty = faculty
    user.department = department
    user.programme = programme
    user.year = year
    user.image = image

    db.session.commit()

    return user_schema.jsonify(user)


#Delete a user
@app.route('/api/v1/user/<id>', methods=['DELETE'])
def deleteUser(id):
    user = Users.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

#Run Server
if __name__ == '__main__':
    app.run(debug=True)