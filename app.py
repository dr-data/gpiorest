from flask import Flask
from flask_restful import Resource, Api


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
api = Api(app)
db = SQLAlchemy(app)


class Pin(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(), unique=True)
    state = db.Column(db.Boolean(), default=False)
    pin_number = db.Column(db.Integer, unique=True)

    def __init__(self, name,pin_number):
        self.name = name
        self.pin_number = pin_number


class PiPin(Resource):

    def get(self,pin_id):
        pin = Pin.query.filter_by(id=pin_id).first()
        return {"name":pin.name,"state":pin.state,"pin_number":pin.pin_number}

    def put(self,pin_id):
        return {'hello': pin_id}


class PiPinList(Resource):

    def get(self):

        all_the_pins = {"pins":[]}
        pins = Pin.query.all()
        for pin in pins:
            all_the_pins['pins'].append({"name":pin.name,"state":pin.state,"pin_number":pin.pin_number})

        return all_the_pins


api.add_resource(PiPin, '/pins/<int:pin_id>')
api.add_resource(PiPinList, '/pins')


@app.cli.command('initdb')
def initdb_command():
    print('Initialized the database.')
    db.create_all()


@app.cli.command('setup')
def setup_command():

    for i in range(0,10):
        pin = Pin(name='pin '+str(i),pin_number=i)
        db.session.add(pin)
        db.session.commit()



if __name__ == '__main__':
    app.run(debug=True)
