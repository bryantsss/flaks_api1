from flask import Flask, jsonify, render_template, request
import requests
import logging
import os

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

POKEAPI_BASE_URL = os.environ.get('POKEAPI_BASE_URL', 'https://pokeapi.co/api/v2')

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/pokemon-info', methods=['GET'])
def get_pokemon_info():
    name = request.args.get('pokemon-name')
    logging.debug(f'Received request for Pokemon: {name}')
    url = f'{POKEAPI_BASE_URL}/pokemon/{name.lower()}'
    response = requests.get(url)
    if response.status_code == 200:
        pokemon_data = response.json()
        return render_template('pokemon_info.html', 
                               name=pokemon_data['name'],
                               id=pokemon_data['id'],
                               types=[t['type']['name'] for t in pokemon_data['types']],
                               abilities=[a['ability']['name'] for a in pokemon_data['abilities']])
    else:
        logging.error(f'Error fetching Pokemon info: {response.status_code}, Response: {response.content}')
        return jsonify({'error': 'Pokemon not found'}), 404

@app.route('/ability-info', methods=['GET'])
def get_ability_info():
    name = request.args.get('ability-name')
    logging.debug(f'Received request for Ability: {name}')
    url = f'{POKEAPI_BASE_URL}/ability/{name.lower()}'
    response = requests.get(url)
    if response.status_code == 200:
        ability_data = response.json()
        return render_template('ability_info.html', 
                               name=ability_data['name'],
                               effect=ability_data['effect_entries'][0]['effect'])
    else:
        logging.error(f'Error fetching ability info: {response.status_code}, Response: {response.content}')
        return jsonify({'error': 'Ability not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

# Lambda handler
def lambda_handler(event, context):
    from aws_lambda_wsgi import response
    return response(app, event, context)
