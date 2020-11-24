import json

import requests
from flask import Blueprint, flash, render_template, request
from flask_login import current_user
from gooutsafe import app
from gooutsafe.forms.restaurant_search import RestaurantSearchForm
from gooutsafe.rao.restaurant_manager import RestaurantManager 

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
    filters = request.args.get('filters', default=None, type=str) or form.DEFAULT_SEARCH_FILTER
    print('keyword')
    print(keyword)
    print('filter')
    print(filters)

    keyword = None if keyword is None or len(keyword) == 0 else keyword
    json_list = []
    restaurants = []
    try:
        if keyword is not None:
            restaurants = search_by(keyword, filters)
        else:      
            restaurants = RestaurantManager.get_get_all()
            if not restaurants:
                flash('Error in getting all the restaurants')
            else:
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
    restaurants = RestaurantManager.get_search_by(search_filter, search_field)
    if restaurants is None:
        raise ValueError
    return restaurants
