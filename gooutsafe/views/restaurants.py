import requests
from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from gooutsafe import app
from gooutsafe.forms.add_measure import MeasureForm
from gooutsafe.forms.add_stay_time import StayTimeForm
from gooutsafe.forms.add_table import TableForm
from gooutsafe.forms.add_times import TimesForm
from gooutsafe.forms.restaurant import RestaurantForm

restaurants = Blueprint('restaurants', __name__)
RESTA_MS_URL = app.config['RESTA_MS_URL']

@restaurants.route('/my_restaurant', methods=['GET'])
@login_required
def my_restaurant():
    """Given the operator, this method allows him to see the details of his restaurant

    Returns:
        Returns the page of the restaurant's details
    """

    return details(current_user.id)


@restaurants.route('/restaurants/<restaurant_id>')
@login_required
def restaurant_sheet(restaurant_id):
    """This method returns the single page for a restaurant

    Args:
        restaurant_id (int): univocal identifier of the restaurant
    """
    url = "%s/restaurants/%s" % (RESTA_MS_URL, restaurant_id)
    res = requests.get(url)
    json_data = res.json()

    if res.status_code != 200:
        print(json_data['message'])
        return abort(404)

    restaurant_sheet = json_data['restaurant_sheet']
    
    return render_template("restaurantsheet.html",
                           restaurant=restaurant_sheet['restaurant'], list_measures=restaurant_sheet['list_measures'],
                           average_rate=restaurant_sheet['average_rate'], max_rate=restaurant_sheet['max_rate'],
                           is_open=restaurant_sheet['is_open']
                           )


@restaurants.route('/restaurants/like/<restaurant_id>')
@login_required
def like_toggle(restaurant_id):
    """Updates the like count

    Args:
        restaurant_id (int): univocal identifier of the restaurant

    Returns:
        Redirects to the single page for a restaurant
    """
    url = "%s/restaurants/like/%s" % (RESTA_MS_URL, restaurant_id)
    res = requests.post(url, json={'user_id': current_user.id})
    json_data = res.json()
    if res.status_code != 200:
        print(json_data['message'])
        flash('Unable to toggle like')
    return restaurant_sheet(restaurant_id)


@restaurants.route('/restaurants/add/<int:id_op>', methods=['GET', 'POST'])
@login_required
def add(id_op):
    """Given an operator, this method allows him to add a restaurant

    Args:
        id_op (int): univocal identifier for the customer

    Returns:
        Redirects the view to the operator's page
    """
    form = RestaurantForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.data['name']
            address = form.data['address']
            city = form.data['city']
            phone = form.data['phone']
            menu_type = form.data['menu_type']
            json_data_to_send = {
                'name': name,
                'address': address,
                'city': city,
                'phone': phone,
                'menu_type': menu_type}
            url = "%s/restaurants/add/%d" % (RESTA_MS_URL, id_op)
            res = requests.post(url, json=json_data_to_send)
            if res.status_code != 200:
                print(res.json()['message'])
                flash('Something went wrong with the creation of the restaurant, sorry!')
            else:
                return redirect(url_for('auth.operator', op_id=id_op))
    return render_template('create_restaurant.html', form=form)


@restaurants.route('/restaurants/details/<int:id_op>', methods=['GET', 'POST'])
@login_required
def details(id_op):
    """Given an operator, this method allows him to see the details of his restaurant

    Args:
        id_op (int): univocal identifier of the operator

    Returns:
        Returns the page of the restaurant's details
    """
    table_form = TableForm()
    time_form = TimesForm()
    measure_form = MeasureForm()
    avg_time_form = StayTimeForm()

    url = "%s/restaurants/details/%s" % (RESTA_MS_URL, id_op)
    res = requests.get(url)
    payload = res.json()
    json_data = payload['details']
    list_measures = json_data['list_measure'].split(',')[1:]

    if res.status_code != 200:
        print(payload['message'])
        return add(current_user.id)

    return render_template('add_restaurant_details.html',
                           restaurant=json_data['restaurant'], tables=json_data['tables'],
                           table_form=table_form, time_form=time_form,
                           times=json_data['times'], measure_form=measure_form,
                           avg_time_form=avg_time_form, avg_stay=json_data['avg_stay'],
                           list_measure=list_measures)


@restaurants.route('/restaurants/save/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
@login_required
def save_details(id_op, rest_id):
    """This method gives the operator the possibility to add tables to his restaurant

    Args:
        id_op (int): univocal identifier of the operator
        rest_id (int): univocal identifier of the restaurant

    Returns:
        Returns the page of the restaurant's details
    """
    table_form = TableForm()

    if request.method == "POST":
        if table_form.is_submitted():
            num_tables = table_form.data['number']
            capacity = table_form.data['max_capacity']
            url = "%s/restaurants/add_tables/%d/%d" % (RESTA_MS_URL, id_op, rest_id)
            res = requests.post(url, json={'number': num_tables, 'max_capacity': capacity})
            if res.status_code != 200:
                print(res.json()['message'])
                flash('Error in saving the tables')

    return redirect(url_for('restaurants.details', id_op=id_op))


@restaurants.route('/restaurants/savetime/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
@login_required
def save_time(id_op, rest_id):
    """This method gives the operator the possibility to add opening hours to his restaurant

    Args:
        id_op (int): univocal identifier of the operator
        rest_id (int): univocal identifier of the restaurant

    Returns:
        Returns the page of the restaurant's details
    """
    time_form = TimesForm()
    if request.method == "POST":
        if time_form.is_submitted():
            day = time_form.data['day']
            start_time = time_form.data['start_time']
            end_time = time_form.data['end_time']
            json_data_to_send = {'day': day,
                                    'start_time': str(start_time),
                                    'end_time': str(end_time)}
            url = "%s/restaurants/add_time/%d/%d" % (RESTA_MS_URL, id_op, rest_id)
            res = requests.post(url, json=json_data_to_send)
            if res.status_code != 200:
                print(res.json()['message'])
                flash('Error in saving the availability')

    return redirect(url_for('restaurants.details', id_op=id_op))


@restaurants.route('/restaurants/savemeasure/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
@login_required
def save_measure(id_op, rest_id):
    """This method gives the operator the possibility to add precaution meausures 
    to his restaurant

    Args:
        id_op (int): univocal identifier of the operator
        rest_id (int): univocal identifier of the restaurant

    Returns:
        Returns the page of the restaurant's details
    """
    measure_form = MeasureForm()

    if request.method == "POST":
        if measure_form.is_submitted():
            measure = measure_form.data['measure']
            json_data_to_send = {'measure': measure}
            url = "%s/restaurants/add_measure/%d/%d" % (RESTA_MS_URL, id_op, rest_id)
            res = requests.post(url, json=json_data_to_send)
            if res.status_code != 200:
                print(res.json()['message'])
                flash('Error in saving the measure')
    return redirect(url_for('restaurants.details', id_op=id_op))


@restaurants.route('/restaurants/avgstay/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
@login_required
def save_avg_stay(id_op, rest_id):
    avg_time_form = StayTimeForm()

    if request.method == "POST":
        if avg_time_form.validate_on_submit():
            hours = avg_time_form.data['hours']
            minute = avg_time_form.data['minutes']
            json_data_to_send = {'hours': hours,
                                    'minutes': minute}
            url = "%s/restaurants/add_avg_stay/%d/%d" % (RESTA_MS_URL, id_op, rest_id)
            res = requests.post(url, json=json_data_to_send)
            if res.status_code != 200:
                print(res.json()['message'])
                flash('Error in saving the average stay time')

    return redirect(url_for('restaurants.details', id_op=id_op))


@restaurants.route('/edit_restaurant/<int:id_op>/<int:rest_id>', methods=['GET', 'POST'])
@login_required
def edit_restaurant(id_op, rest_id):
    """This method allows the operator to edit the information about his restaurant

    Args:
        id_op (int): univocal identifier of the operator
        rest_id (int): univocal identifier of the restaurant

    Returns:
        Returns the page of the restaurant's details
    """
    form = RestaurantForm()
    if request.method == "POST":
        if form.is_submitted():
            name = form.data['name']
            address = form.data['address']
            city = form.data['city']
            phone = form.data['phone']
            menu_type = form.data['menu_type']
            json_data_to_send = {'name': name,
                                    'address': address,
                                    'city': city,
                                    'phone': phone,
                                    'menu_type': menu_type}
            url = "%s/edit_restaurant/%d/%d" % (RESTA_MS_URL, id_op, rest_id)
            res = requests.post(url, json=json_data_to_send)
            if res.status_code != 200:
                print(res.json()['message'])
                flash('Error in saving the average stay time')
            else:
                return redirect(url_for('auth.operator', op_id=id_op))

    return render_template('update_restaurant.html', form=form)
