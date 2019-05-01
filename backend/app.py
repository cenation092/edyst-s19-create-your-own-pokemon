#Useful Links to read : https://medium.com/python-pandemonium/build-simple-restful-api-with-python-and-flask-part-2-724ebf04d12, https://codehandbook.org/working-with-json-in-python-flask/

#Some finding while coding :

#This:
#
#{'http://example.org/about': {'http://purl.org/dc/terms/title': [{'type': 'literal', 'value': "Anna's Homepage"}]}}
#is not JSON.
#This:
#
#{"http://example.org/about": {"http://purl.org/dc/terms/title": [{"type": "literal", "value": "Anna's Homepage"}]}}
#is JSON.
#https://stackoverflow.com/questions/39491420/python-jsonexpecting-property-name-enclosed-in-double-quotes

#=========================================================================================================================================================================

#json.loads take a string as input and returns a dictionary as output.
#json.dumps take a dictionary as input and returns a string as output.
#

#=========================================================================================================================================================================

#How to convert json to string : str(data) where data is json https://stackoverflow.com/questions/34600003/converting-json-to-string-in-python
#How to convert string to json : https://stackoverflow.com/questions/4528099/convert-string-to-json-using-python
#How to check type of variable : https://stackoverflow.com/questions/402504/how-to-determine-a-python-variables-type
#==========================================================================================================================================================================



from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import json

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)

class Pokemon(db.Model):
    # attributes of table Pokemon
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    sprite = db.Column(db.String(120))
    card_colours_data = db.Column(db.String(120))

    def __init__(self, name, sprite, card_colours_data):
        self.name = name
        self.sprite = sprite
        self.card_colours_data = card_colours_data

    #convert data into JSON format
    def toJSON(self):
        card_colours_data_dict = json.loads(self.card_colours_data)
        fg = card_colours_data_dict['fg']
        bg = card_colours_data_dict['bg']
        desc = card_colours_data_dict['desc']
        
        return {'pokemon' : {'id' : self.id, 'name' : self.name, 'sprite' : self.sprite, 'cardColours' : {'fg' : fg, 'bg' : bg, 'desc' : desc}}}

# check conditions on name
def validate_name(name):
    if not name:
        raise AssertionError('No name provided')

    if len(name) < 1 or len(name) > 50:
        raise AssertionError('name must be between 1 and 50 characters')

    return name

# check conditions on sprite
def validate_sprite(sprite):
    if not sprite:
        raise AssertionError('No sprite provided')
    
    if len(sprite) < 1 or len(sprite) > 500:
        raise AssertionError('sprite must be between 1 and 500 characters')

    return sprite

# endpoint to create new pokemon
@app.route("/api/pokemon/", methods=["POST"])
def create_pokemon():
    pokemon = request.json['pokemon']

    name = pokemon["name"]
    validate_name(name)

    sprite = pokemon["sprite"]
    validate_sprite(sprite)

    card_colours_data = str(pokemon["cardColours"])
    card_colours_data = card_colours_data.replace("\'", "\"")
    
    new_pokemon = Pokemon(name, sprite, card_colours_data)

    db.session.add(new_pokemon)
    db.session.commit()
    
    return jsonify(new_pokemon.toJSON())

# check existance of id
def check_id(id):
    if not id:
        raise AssertionError('No id provided')

    if Pokemon.query.filter(Pokemon.id == id).first():
        return id
    else:
        raise AssertionError('id not exist')


# endpoint to get poskemon details by id
@app.route("/api/pokemon/<id>", methods=["GET"])
def pokemon_detail(id):
    check_id(id)
    pokemon =  Pokemon.query.get(id)
    return jsonify(pokemon.toJSON())


# endpoint to update existing pokemon
@app.route("/api/pokemon/<id>", methods=["PUT"])
def update_pokemon(id):

    existing_pokemon = Pokemon.query.get(id)

    pokemon_request = request.json['pokemon']

    if 'name' in pokemon_request:
        name = pokemon_request['name']
        validate_name(name)
        existing_pokemon.name = name

    if 'sprite' in pokemon_request:
        sprite = pokemon_request['sprite']
        validate_sprite(sprite)
        existing_pokemon.sprite = sprite

    if 'cardColours' in pokemon_request:
        card_colours_data = str(pokemon_request['cardColours'])
        card_colours_data = card_colours_data.replace("\'", "\"")
        existing_pokemon.card_colours_data = card_colours_data

    db.session.commit()
    return jsonify(existing_pokemon.toJSON())


# endpoint to delete pokemon
@app.route("/api/pokemon/<id>", methods=["DELETE"])
def delete_pokemon(id):
    pokemon = Pokemon.query.get(id)
    db.session.delete(pokemon)
    db.session.commit()
    
    return jsonify(pokemon.toJSON())

# error handler for invalid url
@app.errorhandler(404)
def page_not_found_404(e):
    return render_template('404.html'), 404

if __name__ == '__main__':

    #app.sqlite file would be generated which acts as a sqlite db
    db.create_all()

    app.run(debug=True, port=8006)
