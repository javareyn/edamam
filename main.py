import requests, os
import pandas as pd
import json
import sqlalchemy
from sqlalchemy import create_engine
import matplotlib
import matplotlib.pyplot as plt


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
    return f'{BASE_URL}{endpoint}' \
           f'?app_id={NUTRITION_APP_ID}' \
           f'&app_key={NUTRITION_APP_KEY}'


def fetch_response():
    while (user_input := input(MENU_PROMPT)) != '3':
        if user_input == '1':
            headers = {
                'Content-Type': 'application/json'
            }

            recipe = {
                'title': input('What is the title of your dish? '),
                'ingr': [
                    item for item in
                    input('Please enter your items separated by a comma: ')
                    .split(',')
                ]
            }

            post_response = requests.post(
                create_url(NUTRITION_POST_ENDPOINT),
                headers=headers,
                json=recipe
            )

            nut_facts = post_response.json()

            print(json.dumps(nut_facts, indent=4))
            print(nut_facts.keys())
            print(json.dumps(nut_facts['totalNutrients']['SUGAR'], indent=4))
            return nut_facts
        elif user_input == '2':
            food = \
                input('Which food would you like nutritional analysis for: ')
            url = f'{create_url(NUTRITION_GET_ENDPOINT)}' \
                  f'&nutrition-type=logging&ingr={food}'
            response = requests.get(url)
            print(response.json())
            return response.json()
        else:
            print('Invalid, input. Please choose a number in the menu!')


nut_facts = fetch_response()

macro_data = {
    'FATS': [
        nut_facts['totalNutrients']['FAT']['quantity'],
        nut_facts['totalNutrients']['FAT']['unit']
    ],
    'CARBS': [
        nut_facts['totalNutrients']['CHOCDF']['quantity'],
        nut_facts['totalNutrients']['CHOCDF']['unit']
    ],
    'PROTEINS': [
        nut_facts['totalNutrients']['PROCNT']['quantity'],
        nut_facts['totalNutrients']['PROCNT']['unit']
    ]
}

macro_df = pd.DataFrame.from_dict(macro_data)


# Transport to CSV in directory
def transport_df_to_csv():
    file_name = input('Name your .csv file: ')
    macro_df.to_csv(f'{file_name}.csv')
    return f'{file_name}.csv'


transport_df_to_csv()


############################
#                          #
#    Generalized methods   #
#    for migrating data    #
#                          #
############################


def save_sql_to_file(filename, database_name):
    os.system('mysqldump -user root -password password --host localhost --port 3306 ' + database_name + ' > ' + filename)


def load_sql_from_file(filename, database_name):
    # create database if it does not exist
    os.system('mysql -user root -password password --host localhost --port 3306 -e "CREATE DATABASE IF NOT EXISTS ' + database_name + ';"')
    os.system("mysql -user root -password password --host localhost --port 3306 " + database_name + " < " + filename)


def create_the_engine(database_name):
    return create_engine('mysql://root:password@localhost/' + database_name + '?charset=utf8', encoding='utf-8')


def update_dataset(database_name, table_name, filename):
    load_sql_from_file(filename, database_name)
    df = pd.read_sql_table(table_name, con=create_the_engine(database_name))
    return df


def save_dataset_to_file(database_name, table_name, filename, dataframe):
    dataframe.to_sql(table_name, con=create_the_engine(database_name), if_exists='replace', index=False)
    save_sql_to_file(filename, database_name)


database_name = 'edamam'
table_name = 'macros'
filename = 'data-dump.sql'

save_dataset_to_file(database_name, table_name, filename, macro_df)


# TODO: Refactor because this looks horrible
# TODO: try-except
# TODO: simple route - requirements.txt with all modules installed, then users can do a pip install -r requirements.txt
# or TODO: recommended use setup.py
