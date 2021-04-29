from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__,template_folder='template')
baseDir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, 'filestorage.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
mar = Marshmallow(app)

class FileContents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    data = db.Column(db.LargeBinary)
    # username = db.Column(db.String(100))


class UploadSchema(mar.Schema):
    class Meta:
        fields = ('id', 'name', 'data' )

upload_schema = UploadSchema(many=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    # username = request.json['username']

    newFile = FileContents(name=file.filename, data=file.read() )
    db.session.add(newFile)
    db.session.commit()

    return 'Saved ' + file.filename + ' to the database!!'



@app.route('/upload', methods=['GET'])
def getUploads():
    allUploads = FileContents.query.all()
    result = upload_schema.dump(allUploads)
    return jsonify(result.data)


if __name__ == '__main__':
    app.run(debug=True)