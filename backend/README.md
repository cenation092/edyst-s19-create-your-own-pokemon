This repo contains a **database-backed API** which allows you to **CREATE, READ, UPDATE** and **DELETE** pokemon cards.

## How to set up the project environemnt

* [Clone](https://github.com/cenation092/edyst-s19-create-your-own-pokemon.git) this repo in your local machine.
* [Install](https://blog.ruanbekker.com/blog/2018/11/27/python-flask-tutorial-series-create-a-hello-world-app-p1/) python3. 
* cd ⁨`edyst-s19-create-your-own-pokemon/backend`
* setup [virtual environment](https://blog.ruanbekker.com/blog/2018/12/09/python-flask-tutorial-series-setup-a-python-virtual-environment-p2/) in it.
* Install all required packages mentioned in `requirement.txt`.

## How to run the project
    
* Open terminal then `cd edyst-s19-create-your-own-pokemon/backend` 
* Run command `python app.py` in your terminal then database will create named `pokemon`.
![database](https://user-images.githubusercontent.com/21224753/56923091-55252c80-6ae7-11e9-900b-8ad22bbea42c.png)

#### Create a single pokémon card
* Hit following API http://127.0.0.1:8006/api/pokemon/ in postman then write JSON file of this type
```
    {
        "pokemon": {
            "name": "charmander",
            "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
            "cardColours": {
                "fg": "#eeeeee",
                "bg": "#3e3e3e",
                "desc": "#111111"
            }
        }
    }
```
This will return a JSON file with pokemon `id` in this format.

```
    {
        "pokemon": {
            "name": "charmander_new_name",
            "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
            "cardColours": {
                "fg": "#eeeeee",
                "bg": "#3e3e3e",
                "desc": "#111111"
            }
        }
    }
```
![create](https://user-images.githubusercontent.com/21224753/56923284-cd8bed80-6ae7-11e9-9980-1681c91ccc00.png)
