import requests
import json

NUTRITION_APP_ID = 'a409daa4'
NUTRITION_APP_KEY = 'ca9c243e5f2d70cff4d6a4997ea55d83'
BASE_URL = 'https://api.edamam.com'
NUTRITION_GET_ENDPOINT = '/api/nutrition-data'
NUTRITION_POST_ENDPOINT = '/api/nutrition-details'

MENU_PROMPT = '''
Nutritional Analysis for...

1) A recipe
2) A single food item
3) Exit

Please choose a number: '''


def create_url(endpoint):
    return f'{BASE_URL}{endpoint}?app_id={NUTRITION_APP_ID}&app_key={NUTRITION_APP_KEY}'


def fetch_response():
    while (user_input := input(MENU_PROMPT)) != '3':
        if user_input == '1':
            headers = {
                'Content-Type': 'application/json'
            }

            recipe = {
                'title': input('What is the title of your dish? '),
                'ingr': [item for item in input('Please enter your items separated by a comma: ').split(',')]
            }

            # url = f'{BASE_URL}{NUTRITION_POST_ENDPOINT}?app_id={NUTRITION_APP_ID}&app_key={NUTRITION_APP_KEY}'

            post_response = requests.post(create_url(NUTRITION_POST_ENDPOINT), headers=headers, json=recipe)

            nut_facts = post_response.json()

            print(json.dumps(nut_facts, indent=4))
            print(nut_facts.keys())
            print(json.dumps(nut_facts['totalNutrients']['SUGAR'], indent=4))
        elif user_input == '2':
            food = input('Which food would you like nutritional analysis for: ')
            url = f'{create_url(NUTRITION_GET_ENDPOINT)}&nutrition-type=logging&ingr={food}'
            response = requests.get(url)
            print(response.json())
        else:
            print('Invalid, input. Please choose a number in the menu!')


fetch_response()

# TODO: Refactor because this looks horrible
# TODO: try-except
# TODO: Structure the values in pandas
# import pandas as pd
# pd.DataFrame(nut_facts['totalNutrients'])
# pd.DataFrame(nut_facts['totalNutrients']).transpose()
# Transport to CSV in directory
# trans = pd.DataFrame(nut_facts['totalNutrients']).transpose()
# trans.to_csv('nut_facts.csv')