import os
import json
import unittest
import requests

from app import app, db

TEST_DB = 'test.sqlite'

class PokemonCRUDTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
    
    @classmethod
    def tearDownClass(self):
        db.drop_all()
    
    def test_create_pokemon(self):
        print("=============================== testing create pokemon API ====================================")

        pokemon_request_data = { "pokemon": { "name": "charmander", "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png", "cardColours": {"fg":"#eeeeee", "bg": "#3e3e3e", "desc": "#111111" } } }
        
        expected_pokemon_response_data = { "pokemon": { "id": 1, "name": "charmander", "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png", "cardColours": {"fg":"#eeeeee", "bg": "#3e3e3e", "desc": "#111111" } } }
        
        actual_pokemon_reponse = self.app.post("http://127.0.0.1:8006/api/pokemon/", data = json.dumps(pokemon_request_data), content_type='application/json')
        actual_pokemon_reponse_data = json.loads(actual_pokemon_reponse.data)

        self.assertEqual(expected_pokemon_response_data, actual_pokemon_reponse_data)
        self.assertEqual(actual_pokemon_reponse.status_code, 200)
    
        print("=============================== Create pokemon API test pass ====================================")
    
    def test_get_pokemon(self):
        print("=============================== testing get pokemon API ====================================")
        
        expected_pokemon_response_data = { "pokemon": { "id": 1, "name": "charmander", "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png", "cardColours": {"fg":"#eeeeee", "bg": "#3e3e3e", "desc": "#111111" } } }

        actual_pokemon_reponse = self.app.get("http://127.0.0.1:8006/api/pokemon/1")
        actual_pokemon_reponse_data = json.loads(actual_pokemon_reponse.data)

        self.assertEqual(expected_pokemon_response_data, actual_pokemon_reponse_data)
        self.assertEqual(actual_pokemon_reponse.status_code, 200)
    
        print("=============================== Get pokemon API test pass ====================================")

    
    def test_update_pokemon(self):
        print("=============================== testing update pokemon API ====================================")
        
        pokemon_request_data_to_update = { "pokemon": { "name": "updated_charmander", "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png", "cardColours": {"fg":"#eeeeee", "bg": "#3e3e3e", "desc": "#111111" } } }

        updated_expected_pokemon_response_data = { "pokemon": { "id": 1, "name": "updated_charmander", "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png", "cardColours": {"fg":"#eeeeee", "bg": "#3e3e3e", "desc": "#111111" } } }

        updated_actual_pokemon_reponse = self.app.put("http://127.0.0.1:8006/api/pokemon/1", data = json.dumps(pokemon_request_data_to_update), content_type='application/json')
        updated_actual_pokemon_reponse_data = json.loads(updated_actual_pokemon_reponse.data)

        self.assertEqual(updated_expected_pokemon_response_data, updated_actual_pokemon_reponse_data)
        self.assertEqual(updated_actual_pokemon_reponse.status_code, 200)

        print("=============================== Update pokemon API test pass ====================================")


    def test_zdelete_pokemon(self):
        print("=============================== testing delete pokemon API ======================================")
        
        expected_pokemon_response_data = { "pokemon": { "id": 1, "name": "updated_charmander", "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png", "cardColours": {"fg":"#eeeeee", "bg": "#3e3e3e", "desc": "#111111" } } }

        actual_pokemon_reponse = self.app.delete("http://127.0.0.1:8006/api/pokemon/1")
        actual_pokemon_reponse_data = json.loads(actual_pokemon_reponse.data)

        self.assertEqual(expected_pokemon_response_data, actual_pokemon_reponse_data)
        self.assertEqual(actual_pokemon_reponse.status_code, 200)

        print("=============================== Delete pokemon API test pass ====================================")


if __name__ == "__main__":
    unittest.main()
