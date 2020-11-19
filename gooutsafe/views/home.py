import json

import requests
from flask import Blueprint, flash, render_template, request
from flask_login import current_user
from gooutsafe import app
from gooutsafe.forms.restaurant_search import RestaurantSearchForm

RESTA_MS_URL = app.config['RESTA_MS_URL']
home = Blueprint('home', __name__)


@home.route('/', methods=['GET', 'POST'])
def index():
    """General route for the index page
    """
    return render_template("index.html")


@home.route('/search', methods=['GET'])
def search():
    """This method allows customers to search restaurants, using a search bar.
    It's possible to retrieve restaurants based on their name, city or cuisine's type.

    """
    form = RestaurantSearchForm()

    keyword = request.args.get('keyword', default=None, type=str)
    filters = request.args.get('filters', default=None, type=str)

    keyword = None if keyword is None or len(keyword) == 0 else keyword
    json_list = []
    restaurants = []
    try:
        if keyword is not None and filters is None:
            restaurants = search_by(keyword, form.DEFAULT_SEARCH_FILTER)
        elif keyword is not None and filters is not None:
            restaurants = search_by(keyword, filters)
        else:
            res = requests.get('%s/restaurants/get_all' % RESTA_MS_URL)
            json_data = res.json()
            if res.status_code != 200:
                flash('Error in getting all the restaurants')
            else:
                restaurants = json_data['restaurants']
                for r in restaurants:
                    json_list.append({"name": r['name'], "lat": r['lat'], "lon": r['lon'] })
            json_list = json.dumps(json_list)
    except Exception as e:
        print(str(e))
        flash('Search error')

    return render_template('explore.html', search_form=form, restaurants=restaurants, json_res=json_list)


def search_by(search_filter, search_field):
    """Implements the research of the restaurants

    Args:
        search_field (string)
        search_filter (string)

    """
    url = "%s/restaurants/search_by/%s/%s" % (RESTA_MS_URL, search_filter, search_field)
    res = requests.get(url)
    json_data = res.json()
    if res.status_code != 200:
        raise ValueError
    else:
        restaurants = json_data['restaurants']

    return restaurants
