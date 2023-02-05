# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
import pandas as pd
import math

df = pd.read_csv('RAW_recipes.csv')
USER_ING = {'bananas', 'white bread', 'mayonnaise',
            'vanilla ice cream', 'peanut butter', 'milk', 'spinach'}


def str_to_set(row):
    ing_str = row['ingredients'].replace("'", '')
    ing_str = ing_str[1:-1]
    ing_lst = ing_str.split(sep=', ')
    return set(ing_lst)


def str_to_lst(row):
    rec_str = row['steps'].replace("'", '')
    rec_str = rec_str[1:-1]
    rec_lst = rec_str.split(sep=', ')
    return rec_lst


def remove_name_spaces(row):
    name_str = str(row['name'])
    return " ".join(name_str.split())


def calc_dissim_score(row):
    r_ing = row['ingredients']
    score = 1 - abs(len(USER_ING & r_ing))/abs(len(USER_ING | r_ing))
    return score


df1 = pd.DataFrame.from_dict({'name': df.apply(remove_name_spaces, axis=1), 'ingredients': df.apply(
    str_to_set, axis=1), 'steps': df.apply(str_to_lst, axis=1)})
df1['minutes'] = df['minutes']
df1.astype({'minutes': 'int'})
df1['dissim_score'] = df1.apply(calc_dissim_score, axis=1)
df1.dropna(axis=0, how='any')
df1.sort_values(by=['dissim_score'], axis=0, inplace=True)
df_out = df1.head(100)
dict_out = df_out.to_dict('records')

for post in dict_out:
    ingred_str = ""
    for ingredient in post["ingredients"]:
        ingred_str += ingredient + ", "
    post["ingredients"] = ingred_str[:-2]


# -- Initialization section --
app = Flask(__name__)


# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/createaccount', methods=['POST', 'GET'])
def createaccount():
    return render_template('CreateAnAccount.html')


@app.route('/profileset', methods=['POST', 'GET'])
def profileset():
    return render_template('ProfileSet-Dairy.html')


@app.route('/recipes', methods=['POST', 'GET'])
def recipes():
    return render_template('homepage.html', dict_out=dict_out)
